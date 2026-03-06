# Salsala — Implementation Plan

---

## Tech Stack & Rationale

### Project Type Assessment

| Dimension | Assessment |
|---|---|
| **Architecture** | Full Stack — clear boundary between client (frontend) and server (backend) |
| **Backend Required?** | Yes — handles WebSocket state sync, OCR processing, NLP, and database management |
| **Frontend Required?** | Yes — Native or Hybrid Mobile App (iOS & Android) to leverage camera and GPS hardware |

### Frontend

**Framework:** React Native (Expo)
**State:** Zustand
**Navigation:** React Navigation v6
**API Client:** Axios + native WebSocket
**Rationale:** Expo provides camera (OCR scanning) and GPS access on both iOS and Android with a single codebase, satisfying all hardware requirements.

---

### Backend

**Language:** Python
**Framework:** FastAPI

**Rationale:** The Salsala project requires high concurrency for real-time Live Collaborative Sync alongside heavy computational tasks like the Smart Hebrew List Engine (NLP) and Receipt Intelligence (OCR). FastAPI is the 2026 industry leader for AI-integrated applications:

- Its native support for Python's `asyncio` makes it exceptionally fast for I/O-bound tasks like WebSocket interactions
- It integrates natively with **Pydantic V2**, which perfectly aligns with the "Fail-Fast Input Validation" requirement — catching data errors before they reach core business logic and reducing debugging time

**Why not alternatives?**
- **Node.js** — can bottleneck during heavy algorithmic processing without microservices
- **Go** — excellent for high-throughput microservices, but lacks Python's dominant ecosystem for NLP and OCR

---

## Folder Map

Following the Full-Stack and Universal Backend Architectural Standards, the project uses a **mono-repo structure** with a strictly layered, resource-first directory hierarchy:

```
salsala-monorepo/
│
├── .github/                    # CI/CD workflows
│   └── workflows/
│       └── ci.yml              # pytest on push
├── docker/                     # Container definitions
│   ├── Dockerfile              # FastAPI server image
│   └── docker-compose.yml      # Server + PostgreSQL/PostGIS
├── docs/                       # Architectural diagrams and guides
├── scripts/                    # DB migration scripts
├── tests/                      # Pytest test suite
│   └── core/                   # Unit tests for pure logic modules
│       ├── test_price_intelligence.py
│       ├── test_winsorization.py
│       └── test_geo_optimizer.py
├── .env.example                # Template for environment variables
├── requirements.txt            # Backend Python dependencies
├── README.md                   # Project documentation
│
├── common/                     # Shared Types/Interfaces between mobile & backend
│   ├── types.ts                # TS mirrors of shared/types.py
│   └── validation.ts           # Zod schemas mirroring Pydantic rules
│
├── client/                     # Mobile App Frontend (iOS & Android)
│   └── src/
│       ├── components/         # Atomic, logic-free UI pieces
│       ├── features/           # Smart components/screens (e.g., Scanner, List)
│       │   ├── ListScreen
│       │   ├── ScannerScreen
│       │   ├── StoreScreen
│       │   └── HistoryScreen
│       ├── logic/              # Custom hooks: useList, useSync, usePriceIntel
│       ├── api/                # Axios + WebSocket client config
│       ├── store/              # Global state (Zustand)
│       └── navigation/         # React Navigation v6 config
│
└── server/                     # FastAPI Backend
    └── src/
        ├── entry_point.py      # Server initialization, global middleware
        ├── config/             # System settings, .env parsing
        ├── db/                 # Database client, connection pooling, ORM models
        │   ├── client.py
        │   └── orm_models.py   # SQLAlchemy table definitions (7 tables)
        ├── models/             # Data Definitions (Pydantic schemas)
        │   ├── item.py
        │   ├── list.py
        │   ├── transaction.py
        │   ├── receipt.py
        │   ├── benchmark.py
        │   ├── store.py        # Store model
        │   └── user.py         # User model
        ├── routes/             # The Entryway (no business logic)
        ├── controllers/        # The Orchestrator (validates input, HTTP responses)
        ├── services/           # The Brain (business logic, DB interaction)
        ├── core/               # Pure Logic (independent of DB/Frameworks)
        │   ├── price_intelligence.py  # Math module for price delta
        │   ├── winsorization.py       # Statistical Winsorization aggregation
        │   └── geo_optimizer.py       # Total Basket calculator
        └── utils/              # Reusable helper functions
```

---

## Security Implementation

**Input Validation**  
Pydantic V2 will be used natively with FastAPI to strictly validate the shape and types of incoming data, serving as the Fail-Fast mechanism to prevent dirty data (e.g., negative prices or text in numeric fields).

**Secret Management**  
Secrets and API keys must never be hardcoded. `python-dotenv` combined with the `config/` directory will manage environment variables from `.env` files across Development, Testing, and Production environments.

**XSS & Hebrew Sanitization**  
All text inputs will be stripped of script tags to prevent Cross-Site Scripting (XSS) in collaborative lists. A dedicated utility function in `utils/` will handle this using a standard Python HTML sanitizer (e.g., `Bleach`).

**PII Redaction (OCR)**  
The OCR service will implement a Regex/NER step to automatically mask credit card digits, phone numbers, and cashier IDs before any receipt image data is saved to the cloud.

**Tokenized Sharing & Anonymization**  
The `uuid` library will generate non-guessable UUIDs for list sharing. User IDs will be completely decoupled from price data in the global database to ensure anonymized crowdsourcing.

---

## Database Layer

**Engine:** PostgreSQL + PostGIS (for geo-indexed store queries)
**ORM:** SQLAlchemy async with Alembic migrations
**Tables:** items, shopping_lists, transactions, receipts, benchmarks, stores, users

---

## Testing Strategy

- Unit tests for all `core/` modules (price_intelligence, winsorization, geo_optimizer)
- Integration tests for service layer against a test DB
- Tool: pytest + pytest-asyncio

---

## Refactoring Strategy (150-Line Limit)

To adhere to the 150-line complexity threshold, the following modules are anticipated to require splitting:

**`services/receipt.py` (OCR Pipeline)**  
Given the complexity of image processing, Hebrew text extraction, and OCR confidence scoring, this file will be split into:
- `ocr_extractor.py`
- `pii_redactor.py`
- `receipt_validator.py`

**`services/list.py` (Smart List & Sync)**  
Handling both NLP matching and WebSocket CRDTs will cause bloat. This will be split into:
- `hebrew_nlp.py`
- `live_sync.py`