# 🏗️ Frontend Project Architecture

## 1. Structural Philosophy
We follow a **Modular Component Architecture**. Logic is separated into "dumb" UI components (visuals) and "smart" containers/hooks (logic).

## 2. Global Directory Map
* **`src/`**: The main source code.
    * **`assets/`**: Static files (images, fonts, icons, global CSS).
    * **`components/`**: Atomic UI pieces (Buttons, Inputs, Cards). *Rule: These should be reusable and logic-free.*
    * **`features/` or `screens/`**: High-level modules or pages. This houses the "smart" components that combine atomic UI.
    * **`hooks/`**: Custom reusable logic (e.g., `useAuth`, `useForm`).
    * **`services/` or `api/`**: API call definitions and data fetching logic (Axios/Fetch).
    * **`store/` or `context/`**: Global state management (Redux, Zustand, Context API).
    * **`utils/`**: Helper functions (date formatting, string manipulation).
    * **`constants/`**: Theme colors, API endpoints, and fixed configuration.
    * **`navigation/`**: Routing configuration (React Navigation or React Router).

## 3. Naming Logic
* **Components:** PascalCase (e.g., `PrimaryButton.tsx`).
* **Files:** kebab-case for utilities (e.g., `date-formatter.ts`).
* **Styles:** Scoped to the component (e.g., `PrimaryButton.styles.ts`).

---

## 4. Separation of Concerns
1. **The Container Rule:** Components should not fetch data. Data should be passed in as props or managed by a custom hook.
2. **The 100-Line Rule:** If a component file exceeds 150 lines, it must be broken down into smaller sub-components.


# Universal Frontend Architectural Standards

---

## 1. Structural Philosophy: Modular Component Architecture

The system is built on the principle of **Separation of Concerns**.  
We distinguish between:

### Presentation (Dumb Components)
Purely visual elements that receive data via props/parameters.

### Logic (Smart Containers / Hooks)
The "brains" that handle data fetching, state changes, and business rules.

---

## 2. Global Directory Map (Language-Agnostic)


src/
│
├── assets/ # Global static resources (images, fonts, icons, base styles)
├── components/ # Atomic, reusable UI elements (Buttons, Inputs, Modals)
├── features/ # Application modules, pages, or screens
│ └── (or views/)
├── logic/ # Reusable business logic, stateful behaviors
│ └── (or hooks/)
├── api/ # External communication & network configuration
│ └── (or data/)
├── store/ # Global state management systems
├── utils/ # Pure helper functions (formatting, math, strings)
├── config/ # Environment variables & immutable configuration
│ └── (or constants/)
└── router/ # Navigation and URL/view management


### Directory Rules

- **components/** → Must remain logic-free and highly generic.
- **features/views/** → Assemble atomic components into functional UI.
- **logic/hooks/** → Encapsulate reusable state and business logic.
- **api/data/** → Responsible only for communication definitions.
- **utils/** → Must contain pure, side-effect-free functions.

---

## 3. Universal Naming Logic

Consistency is key for AI and human collaboration.

### UI Entities
Use **PascalCase** for visual component files:


UserCard.[ext]
NavigationBar.[ext]


### Logic / Utility Files
Use **kebab-case** for logic-heavy files:


calculate-total.[ext]
use-auth-session.[ext]


### Styles / Configuration Files
Use suffix-based naming to group related files:


UserCard.styles.[ext]
UserCard.test.[ext]
UserCard.config.[ext]


---

## 4. General Separation of Concerns

### The Pure Component Rule
UI components must:
- ❌ Never trigger network requests
- ❌ Never perform complex data transformations directly
- ✅ Receive data from a dedicated logic layer
- ✅ Accept dependencies via props/parameters

---

### The Complexity Threshold (150-Line Rule)

If a file exceeds **150 lines of code**, it signals that:

- The component/module handles too many responsibilities.
- It must be refactored into smaller sub-modules.

This rule enforces long-term maintainability and scalability.

---

### Encapsulated Styles

- Styles must be scoped to the specific component.
- Prevent global style leaking.
- Avoid unexpected visual side effects.
- Encourage modular and predictable UI behavior.

---

## Core Architectural Principles Summary

- Modular design
- Clear responsibility boundaries
- Pure presentation layer
- Isolated business logic
- Scalable folder hierarchy
- Strict naming consistency
- Refactor early, not late
- Encapsulated styling