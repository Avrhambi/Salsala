# Salsala — Architecture

## Overview

Salsala follows a strict client/server split. The mobile client (React Native) and the backend (FastAPI) communicate exclusively over REST. There is no shared runtime — types and validation schemas are mirrored manually between the two sides.

```
┌─────────────────────────────────┐        ┌──────────────────────────────────┐
│        React Native Client       │        │          FastAPI Backend          │
│                                 │        │                                  │
│  Screen → Hook → API → Store    │◄──────►│  Route → Service → ORM → DB      │
│                                 │  REST  │                                  │
│  Zod validates responses        │        │  Pydantic validates requests      │
└─────────────────────────────────┘        └──────────────────────────────────┘
                                                          │
                                                          ▼
                                                   PostgreSQL (asyncpg)
```

---

## Design Principles

### 1. Fail-fast at boundaries
Every function that receives external input (API response, user input) validates it immediately before any business logic runs. On the client, Zod schemas parse every API response. On the server, Pydantic models validate every request body.

### 2. Dependency direction
```
routes/ → services/ → db/
models/ → (no upward deps)
utils/  → (no upward deps)
```
Routes import services. Services import ORM models and Pydantic models. Nothing imports upward. This makes each layer independently testable.

### 3. No hardcoded config
All secrets and environment-specific values are read from environment variables via `server/config/settings.py`. The client reads its API base URL from `app.json` extra config, injected at build time via `expo-constants`.

### 4. 150-line file limit
No file exceeds 150 lines. When a file grows beyond this, logic is split into a helper module (e.g. `_build_list` helper extracted from the service layer).

---

## Client Architecture

### Layer diagram

```
App.tsx
  └── AppNavigator (React Navigation bottom tabs)
        ├── ListScreen
        │     ├── useList (hook)          ← all data operations
        │     ├── useAppStore (Zustand)   ← read state
        │     ├── CreateListModal
        │     └── AddItemBar
        └── HistoryScreen
              └── useList (hook)
```

### Data flow (create list example)

```
CreateListModal.handleCreate()
  → useList.startList(userIds, name)
    → list.api.createList()         POST /list/create
      → ShoppingListSchema.parse()  Zod validates response
    → useAppStore.upsertList()      add to lists[]
    → useAppStore.setActiveList()   open the list
  → modal closes
```

### State management (Zustand)

```
AppState {
  lists: ShoppingList[]       // active (non-completed) lists
  activeList: ShoppingList | null   // currently open list
  history: ShoppingList[]     // completed lists
  userId: UUID | null
  isLoading: boolean
  error: string | null
}
```

`isLoading` is only used by individual screens for inline spinners — it is never used as a full-screen unmount trigger to avoid destroying local modal state.

### API client

All HTTP calls go through a single Axios instance (`src/api/client.ts`) with:
- Base URL from `expo-constants`
- 15-second timeout
- Centralised error interceptor: unwraps `error.response.data.detail` so all errors surface as plain `Error` objects with a human-readable message

### Type safety boundary

`common/types.ts` defines TypeScript interfaces. `common/validation.ts` defines matching Zod schemas. Every API response is parsed through the Zod schema before being stored — invalid shapes throw and are caught by the hook's error handler.

---

## Server Architecture

### Layer diagram

```
entry_point.py          (FastAPI app factory)
  ├── routes/list.py    (HTTP boundary — parse request, call service, map errors to HTTP codes)
  ├── routes/user.py
  │
  ├── services/list.py  (business logic — orchestrates DB calls, enforces invariants)
  ├── services/user.py
  │
  ├── db/orm_models.py  (SQLAlchemy table definitions)
  ├── db/client.py      (async engine, get_db_session FastAPI dependency)
  │
  ├── models/list.py    (Pydantic response shapes)
  ├── models/item.py
  ├── models/user.py
  │
  └── utils/logger.py   (centralised logger)
```

### Request lifecycle

```
HTTP request
  → FastAPI router (routes/list.py)
    → Pydantic model validates request body (auto, by FastAPI)
    → service function called with typed args + AsyncSession
      → ORM queries execute against PostgreSQL
      → Pydantic response model constructed
    → HTTP response (JSON)
  → ValueError → 404 or 422
  → Exception  → 500
```

### Database schema

```
users
  user_id  UUID PK
  display_name  VARCHAR(120)

shopping_lists
  list_id       UUID PK
  name          VARCHAR(255)
  is_completed  BOOLEAN  default false
  completed_at  TIMESTAMPTZ nullable
  sync_timestamp TIMESTAMPTZ server_default now()

list_members  (many-to-many: users ↔ lists)
  list_id  FK → shopping_lists
  user_id  FK → users

items
  id               UUID PK
  name_hebrew      VARCHAR(255)
  default_quantity INT

list_items  (many-to-many: lists ↔ items)
  list_id   FK → shopping_lists
  item_id   FK → items
  quantity  INT
  is_bought BOOLEAN default false
```

### Auto-archiving

`_check_and_archive` is called after every `mark_item_bought`. It queries all `list_items` for the list — if every row has `is_bought = true`, the list's `is_completed` flag is set and `completed_at` is stamped. No cron job or background task is needed.

### Session management

Each request gets an independent `AsyncSession` via the `get_db_session` FastAPI dependency (async generator). The session is committed inside the service function and closed automatically when the dependency generator exits. No session is held open across requests.

---

## Shared Types

Types are defined in two places and kept in sync manually:

| File | Purpose |
|---|---|
| `common/types.ts` | TypeScript interfaces used by the client |
| `common/validation.ts` | Zod schemas that mirror those interfaces |
| `server/models/*.py` | Pydantic models that define the same shapes on the server |

When a field is added to a Pydantic model, the TypeScript interface and Zod schema must be updated to match, or the client will throw a Zod parse error on the next API response.

---

## TODO Features 

The following features were scoped out of the MVP but are preserved in git history for future implementation:

| Feature | Branch / Commit |
|---|---|
| WebSocket real-time sync | git history |
| Hebrew NLP item search | git history |
| Receipt OCR (ScannerScreen) | git history |
| Store geo-recommendations | git history |
| Price intelligence / winsorization | git history |
| Barcode scanner | git history |
| Transaction log | git history |

---

## Adding a New Feature — Checklist

1. **Server model** — add Pydantic model in `server/models/`
2. **ORM** — add table or column in `server/db/orm_models.py`
3. **Service** — add business logic in `server/services/`
4. **Route** — add endpoint in `server/routes/`, map errors to HTTP codes
5. **Register** — include router in `server/entry_point.py`
6. **Client types** — update `common/types.ts` and `common/validation.ts`
7. **API function** — add call in `client/src/api/`
8. **Hook** — expose operation via `use-list.ts` or a new hook
9. **Store** — add state slice to `app-store.ts` if new state is needed
10. **Screen/component** — wire up the UI
