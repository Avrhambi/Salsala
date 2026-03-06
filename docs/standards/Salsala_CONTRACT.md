# Salsala — Data Models & Architecture

---

## Data Models

Located in the `models/` directory, defined using **Pydantic**.

### `Item`
| Field | Type | Notes |
|---|---|---|
| `id` | `UUID` | |
| `name_hebrew` | `String` | |
| `default_quantity` | `Int` | |

### `List`
| Field | Type | Notes |
|---|---|---|
| `list_id` | `UUID` | |
| `users` | `List[UUID]` | |
| `items` | `List[Item]` | |
| `sync_timestamp` | `DateTime` | |

### `Transaction`
| Field | Type | Notes |
|---|---|---|
| `transaction_id` | `UUID` | |
| `item_id` | `UUID` | |
| `price` | `Float` | Strictly `> 0` |
| `quantity` | `Float` | |
| `store_name` | `String` | |
| `timestamp` | `DateTime` | |

### `Receipt`
| Field | Type | Notes |
|---|---|---|
| `receipt_id` | `UUID` | |
| `image_url` | `String` | |
| `confidence_score` | `Float` | |
| `requires_human_verification` | `Boolean` | |
| `parsed_items` | `List[Transaction]` | |

### `Benchmark`
| Field | Type | Notes |
|---|---|---|
| `item_id` | `UUID` | |
| `store_id` | `UUID` | |
| `national_avg` | `Float` | |
| `data_points` | `Int` | |

### `Store`
| Field | Type | Notes |
|---|---|---|
| `store_id` | `UUID` | |
| `name` | `String` | |
| `coordinates` | `GeoCoordinates` | |
| `chain` | `String` | e.g. "Shufersal", "Rami Levy" |

### `User`
| Field | Type | Notes |
|---|---|---|
| `user_id` | `UUID` | Non-guessable tokenized ID |
| `display_name` | `String` | |
| `last_known_location` | `GeoCoordinates` | Optional, for GPS fallback |

---

## Communication Rules

All interactions between the Salsala mobile client and the backend strictly adhere to the JSON standard defined in the `models/` layer:

- The API exchanges data using standardized JSON payloads mapped directly to the Pydantic models
- WebSockets transmit JSON payloads representing state changes for optimistic UI updates

---

## Resource-First Naming

Following the Resource-First rule, all layers use consistent entity naming. Function names use semantic prefixes: `handle`, `process`, `get`, `create`, `calculate`.

| Entity | Route | Controller | Service |
|---|---|---|---|
| **List** | `routes/list.py` | `controllers/list.py` → `handle_sync` | `services/list.py` → `update_list_state` |
| **Item** | `routes/item.py` | `controllers/item.py` → `handle_search` | `services/item.py` → `get_nlp_match` |
| **Transaction** | `routes/transaction.py` | `controllers/transaction.py` → `handle_purchase` | `services/transaction.py` → `create_transaction_log` |
| **Receipt** | `routes/receipt.py` | `controllers/receipt.py` → `handle_upload` | `services/receipt.py` → `process_ocr` |
| **Store / Geo** | `routes/store.py` | `controllers/store.py` → `handle_recommendation` | `services/store.py` → `get_optimal_basket` |

---

## Shared Types

Located in the `common/` or `shared/` directory to sync between frontend and backend.

**`TrendValue`** — Enum used by the Price Intelligence Engine  
Values: `UP` · `DOWN` · `STABLE` · `N/A`

**`GeoCoordinates`** — Interface used by the Geographic Value Optimizer  
Fields: `latitude`, `longitude`

**`UUID`** — Standardized string format for tokenized sharing and user identification

---

## Core Pure Logic Modules

Located in `core/` — no DB or HTTP dependencies, 100% unit-testable.

| Module | Function | Returns |
|---|---|---|
| `price_intelligence.py` | `calculate_price_trend(current, history)` | `TrendValue` |
| `winsorization.py` | `calculate_winsorized_average(prices)` | `float` |
| `geo_optimizer.py` | `calculate_optimal_basket(list_items, store_benchmarks)` | `List[StoreRank]` |

---

## Frontend API Contract

The mobile client communicates with the backend exclusively via:
- REST JSON on all 5 resource endpoints
- WebSocket on `/list/ws/{list_id}` for optimistic UI sync

TypeScript types in `common/types.ts` must mirror `shared/types.py`.

---

## Design Justification

**Language & Framework**  
Python with FastAPI was chosen because Salsala is highly reliant on AI/ML pipelines (NLP Hebrew processing, OCR). FastAPI is the top framework in 2026 for AI-integrated apps, providing the raw speed necessary for WebSocket synchronization via native `asyncio`.

**Security Libraries**  
Pydantic V2 is the best fit for input validation because its deep integration with FastAPI stops bad data at the door — directly solving Salsala's "Fail-Fast Input Validation" requirement to protect analytics. Environment variable parsers ensure secrets are fully isolated from the codebase, adhering to strict configuration management rules.

**Tight Coupling Prevention & Separation of Concerns**  
The architecture enforces strict **Directional Integrity**:

```
Interface (Routes) → Orchestrator (Controllers) → Brain (Services) → Core (Pure Logic) → Infrastructure (DB)
```

Tight coupling is prevented by isolating high-level business rules — such as the mathematical Price Intelligence Engine and Crowdsourced Statistical Winsorization — into the `core/` directory. These Pure Logic modules receive raw data and return calculations entirely independent of frameworks, UI, or databases, making them **100% unit-testable**.

Separation of Concerns is enforced by ensuring the `services/` layer handles business logic without ever accessing HTTP `Request` or `Response` objects, which are strictly managed by `controllers/`.