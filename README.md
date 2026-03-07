# Salsala — Shareable Shopping List App

A collaborative Hebrew shopping list app built with React Native (Expo) and FastAPI.
Users create named lists, add items in Hebrew, mark items as bought, share lists with others by UUID, and browse completed list history.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Client Setup](#client-setup)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Running Tests](#running-tests)
- [Known Limitations](#known-limitations)

---

## Features

- **Create named lists** — each list has a name; duplicate active names are prevented per user
- **Add items in Hebrew** — free-text Hebrew item entry
- **Mark items as bought** — checkbox with strike-through; list auto-archives when all items are bought
- **Share lists** — share a list UUID via any platform (WhatsApp, SMS, etc.); recipient joins by pasting UUID
- **Join existing lists** — enter a list UUID to join a shared list
- **History** — view all completed lists with item details
- **Reuse lists** — recreate a completed list as a new active list with one tap
- **Multi-user** — multiple users can share the same list

---

## Tech Stack

| Layer | Technology |
|---|---|
| Mobile client | React Native, Expo SDK 53 |
| State management | Zustand |
| Client validation | Zod |
| HTTP client | Axios |
| Backend | Python 3.12, FastAPI |
| Server validation | Pydantic v2 |
| Database | PostgreSQL (asyncpg) |
| ORM | SQLAlchemy async |
| Migrations | Alembic |
| Containerization | Docker, Docker Compose |
| CI | GitHub Actions |

---

## Project Structure

```
Salsala/
├── client/                      # React Native Expo app
│   ├── App.tsx                  # Entry point, user registration
│   ├── app.json                 # Expo config (API base URL)
│   ├── common/                  # Shared types and Zod schemas (client copy)
│   │   ├── types.ts
│   │   └── validation.ts
│   └── src/
│       ├── api/                 # Axios API call functions
│       │   ├── client.ts        # Configured Axios instance
│       │   ├── list.api.ts      # List CRUD + history
│       │   └── user.api.ts      # User registration
│       ├── components/          # Reusable UI components
│       │   ├── ItemCard.tsx
│       │   └── PrimaryButton.tsx
│       ├── constants/
│       │   └── theme.ts         # Colors, spacing, typography
│       ├── features/
│       │   ├── HistoryScreen/   # Completed lists view
│       │   └── ListScreen/      # Active lists + item management
│       │       ├── AddItemBar.tsx
│       │       └── CreateListModal.tsx
│       ├── logic/
│       │   └── use-list.ts      # All list operations as a hook
│       ├── navigation/
│       │   └── AppNavigator.tsx # Bottom tab navigator
│       └── store/
│           └── app-store.ts     # Zustand global store
│
├── server/                      # FastAPI backend
│   ├── entry_point.py           # App factory, router registration
│   ├── config/
│   │   └── settings.py          # Env-based config (AppSettings)
│   ├── db/
│   │   ├── client.py            # Async engine + session dependency
│   │   └── orm_models.py        # SQLAlchemy table definitions
│   ├── models/                  # Pydantic response models
│   │   ├── item.py
│   │   ├── list.py
│   │   └── user.py
│   ├── routes/                  # FastAPI routers
│   │   ├── list.py
│   │   └── user.py
│   ├── services/                # Business logic
│   │   ├── list.py
│   │   └── user.py
│   └── utils/
│       └── logger.py            # Centralised logging
│
├── common/                      # Canonical shared types (source of truth)
│   ├── types.ts
│   └── validation.ts
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── tests/
│   └── core/                    # Pytest test suite
│
└── .github/
    └── workflows/
        └── ci.yml               # GitHub Actions CI
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL 14+ (or Docker)
- Expo CLI (`npm install -g expo-cli`)

---

### Option A — Docker (recommended)

Runs both the PostgreSQL database and the FastAPI server together with a single command. No Python environment or database setup needed.

```bash
docker compose -f docker/docker-compose.yml up --build
```

The API will be available at `http://localhost:8000`.
Interactive docs at `http://localhost:8000/docs`.

What it starts:
- `db` — PostgreSQL 16 on port 5432 (with a health check)
- `api` — FastAPI server on port 8000 (waits for the DB to be healthy before starting)

Tables are created automatically on first startup. Data is persisted in a Docker volume (`postgres_data`) so it survives container restarts.

To stop:
```bash
docker compose -f docker/docker-compose.yml down
```

To wipe all data and start fresh:
```bash
docker compose -f docker/docker-compose.yml down -v
```

---

### Option B — Manual Backend Setup

**1. Clone and create a virtual environment**

```bash
git clone <repo-url>
cd Salsala
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

```bash
cp .env.example .env
# Edit .env — set DATABASE_URL, APP_SECRET_KEY
```

**4. Start PostgreSQL**

Using Docker (DB only):
```bash
docker compose -f docker/docker-compose.yml up db -d
```

Or point `DATABASE_URL` at an existing PostgreSQL instance.

**5. Run the server**

```bash
uvicorn server.entry_point:app --reload --port 8000
```

Tables are created automatically on startup via `Base.metadata.create_all`.

The API docs are available at `http://localhost:8000/docs`.

---

### Client Setup

**1. Install dependencies**

```bash
cd client
npm install
```

**2. Set the API base URL**

Edit `client/app.json`:

```json
{
  "expo": {
    "extra": {
      "apiBaseUrl": "http://<your-machine-ip>:8000"
    }
  }
}
```

Use your LAN IP (not `localhost`) when running on a physical device.
Use `http://10.0.2.2:8000` for Android emulator.

**3. Start Expo**

```bash
npx expo start --clear
```

Scan the QR code with the Expo Go app (iOS/Android).

---

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | PostgreSQL async connection string | `postgresql+asyncpg://user:pass@localhost/salsala` |
| `APP_SECRET_KEY` | Secret key for the app | `change-me-in-production` |
| `LOG_LEVEL` | Logging level | `INFO` |

---

## API Reference

All routes are prefixed. Full interactive docs at `/docs` when the server is running.

### Users — `/user`

| Method | Path | Description |
|---|---|---|
| POST | `/user/register` | Register a new user |

### Lists — `/list`

| Method | Path | Description |
|---|---|---|
| POST | `/list/create` | Create a new named list |
| GET | `/list/{list_id}` | Fetch a list by ID |
| PATCH | `/list/{list_id}` | Rename a list |
| DELETE | `/list/{list_id}` | Delete a list |
| GET | `/list/history/{user_id}` | Get completed lists for a user |
| POST | `/list/{list_id}/items` | Add an item to a list |
| DELETE | `/list/{list_id}/items/{item_id}` | Remove an item from a list |
| PATCH | `/list/{list_id}/items/{item_id}/bought` | Mark an item as bought |

### Auto-archiving

When all items in a list are marked as bought, the list is automatically marked `is_completed = true` with a `completed_at` timestamp and moves to history.

---

## Running Tests

```bash
pytest tests/ -v
```

CI runs on every push and PR to `main` via GitHub Actions (`.github/workflows/ci.yml`).

---

## Known Limitations

- **Deep links not supported in Expo Go** — sharing a list requires the recipient to manually paste the UUID into the "הצטרף" tab. A development build (`expo run:android` / `expo run:ios`) is required for `salsala://` deep link support.
- **No offline support** — all operations require an active connection to the backend.
- **Single device per user** — user identity is tied to the device (a new anonymous user is created on each fresh install).
- **Hebrew only** — item entry and UI are in Hebrew.
