# 📂 Universal Backend Architectural Standards

## 1. Structural Philosophy: The Layered Approach
We use a **Layered Architecture** to decouple logic. This ensures that the core business logic remains independent of the web framework or the database implementation.



---

## 2. Global Directory Hierarchy
All backend projects should follow this resource-based organization. Replace `[ext]` with your language's specific extension (e.g., `.py`, `.js`, `.ts`, `.go`).

* **`root/`**: Project-wide configuration, environment variables (`.env`), and dependency manifests.
* **`entry_point.[ext]`**: The main initialization file. Sets up the server, database connections, and global middleware.
* **`config/`**: Global constants, system settings, and environment variable parsing.
* **`db/`**: Database client initialization, connection pooling, and driver setup.
* **`models/`**: **Data Definitions.** Definitions of schemas, interfaces, or structs (e.g., Pydantic models, TypeScript interfaces).
* **`routes/`**: **The Entryway.** Defines API endpoints and maps them to controllers. *Rule: No business logic allowed here.*
* **`controllers/`**: **The Orchestrator.** Parses incoming requests, validates input "shape," and calls the appropriate Service. Returns HTTP responses and status codes.
* **`services/`**: **The Brain.** Contains core Business Logic and Data Access. Interacts with the database or external APIs.
* **`utils/`**: **The Toolbox.** Reusable helper functions, shared managers, and third-party wrapper classes.
* **`storage/`**: Local directory for persistent files, logs, or temporary assets (usually excluded from Git).

---

## 3. Generalized Naming Conventions

### **The Resource-First Rule**
Files should be named after the **entity** they handle. Consistency across layers is mandatory.
*Example for an "Order" resource:*
* `routes/order.[ext]`
* `controllers/order.[ext]`
* `services/order.[ext]`
* `models/order.[ext]`

### **Cross-Language Function Naming**
Functions must follow these semantic prefixes regardless of casing (snake_case vs camelCase):

| Layer | Function Prefix | Purpose |
| :--- | :--- | :--- |
| **Controller** | `handle`, `process`, `request` | Entry point from the route. |
| **Service** | `get`, `create`, `update`, `delete`, `calculate` | Core logic and DB interaction. |
| **Utils** | `format`, `parse`, `validate`, `is`, `has` | Generic helper logic. |

---

## 4. The "Separation of Concerns" Rules

1.  **Service Purity:** A **Service** must never access "Request" or "Response" objects (no headers, no cookies, no HTTP status codes). It receives raw data (objects/strings) and returns data or throws internal errors.
2.  **Controller Responsibility:** Only the **Controller** is allowed to decide the HTTP response (e.g., 200 OK, 404 Not Found, 400 Validation Error).
3.  **No Logic in Routes:** Routes should only define the path, the method (GET/POST), and the controller function to execute.
4.  **Single Source of Truth:** A specific piece of business logic (e.g., a tax calculation) must exist in exactly **one** Service function to prevent inconsistency.

---

