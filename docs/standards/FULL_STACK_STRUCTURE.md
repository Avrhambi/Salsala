
# 📂 General Project Hierarchy

## 1. Global Mono-Repo / Full-Stack Logic
Every project should have a clear boundary between the environment, the client (frontend), and the server (backend).

## 2. Directory Hierarchy
* **`.github/`**: CI/CD workflows and automation scripts.
* **`docs/`**: Project documentation, architectural diagrams, and user guides.
* **`client/` or `frontend/`**: Contains the Frontend Architecture (see FRONTEND_ARCHITECTURE.md).
* **`server/` or `backend/`**: Contains the Backend Architecture (see BACKEND_ARCHITECTURE.md).
* **`common/` or `shared/`**: Shared code between frontend and backend (e.g., Types/Interfaces, Validation logic).
* **`scripts/`**: Automation scripts for deployment, database migrations, or data seeding.
* **`tests/`**: Global integration tests (if not colocated within features).
* **`docker/`**: Dockerfiles and container orchestration settings.
* **`.env.example`**: Template for environment variables (never commit the actual `.env`).
* **`README.md`**: The entry point for humans/AI to understand the project's purpose and setup instructions.

---

## 3. Communication Rules
1. **Independence:** The `client` and `server` should be able to run independently of each other.
2. **Standardized API:** All communication between frontend and backend must follow the JSON standard defined in the `models/` layer.
3. **Environment Isolation:** Secrets and keys must strictly live in `.env` and never be hard-coded in either the client or server folders.