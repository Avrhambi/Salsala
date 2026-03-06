# Salsala (סלסלה) — Requirements

## Introduction

**Salsala (סלסלה)** is a high-intelligence shopping companion designed to navigate the Israeli grocery market by transforming static lists into dynamic, money-saving tools.

---

## Features

### 1. Smart Hebrew List Engine

**User Story:** As a user, I want to add products using natural Hebrew so that my list-making is fast and intuitive.

**The Logic:** An autocomplete and NLP (Natural Language Processing) system mapped to Israeli product databases, handling Hebrew prefixes/suffixes (e.g., ה-גבינה).

**Happy Path:** User types "חלב," selects "Tnuva 3% 1L" from the dropdown; the item is added with a default quantity of 1.

**Edge Cases:**
- User enters an item not in the database (custom text)
- User enters emojis or non-Hebrew characters

**Failure States:** Search API timeout; system must allow manual "Custom Item" entry immediately without a loading hang.

**Design Rationale:** We use a *Graceful Degradation* strategy. If the smart database is unreachable, the app reverts to a basic text-list mode to ensure the user is never blocked while standing in a store.

**Definition of Done:** User can add an item and see it rendered in the list in under **200ms**.

---

### 2. Live Collaborative Sync

**User Story:** As a household, I want to share my list with others so we can shop together in real-time.

**The Logic:** WebSocket or Push-based state synchronization across multiple User IDs attached to a single "List ID."

**Happy Path:** User A checks "Bread" on their phone; User B's phone updates "Bread" to "Bought" instantly.

**Edge Cases:**
- "Double-check" conflict (two users checking the same item at the same millisecond)
- Loss of internet while in a "dead zone" of a supermarket

**Failure States:** Data collision; system must use a *Last Write Wins* or *Conflict-Free Replicated Data Type* (CRDT) approach.

**Design Rationale:** *Optimistic UI Updates* are used here. The UI reflects the change locally before the server confirms it, making the app feel "instant" even on poor cellular data.

**Definition of Done:** Synchronization occurs across multiple devices with a latency of less than **500ms**.

---

### 3. Transactional "Mark as Bought" (Data Capture)

**User Story:** As a shopper, I want to record the price and store for items I buy to track my spending history.

**The Logic:** A state transition from `Active` → `Bought` that triggers a data entry form for `[Price]`, `[Quantity]`, and `[Store Name]`.

**Happy Path:** User taps a checkbox, enters "29.90," selects "Rami Levy," and the item is archived.

**Edge Cases:**
- User enters "0" or a negative price
- User skips the price field entirely

**Failure States:** Invalid data types (text in price field) attempting to save to the history log.

**Design Rationale:** *Fail-Fast Input Validation.* We block the "Save" action if the price is non-numeric to prevent "dirty data" from ruining future analytics.

**Definition of Done:** Data is successfully written to the local log with a verified timestamp and Store ID.

---

### 4. Price Intelligence & Comparison Engine

**User Story:** As a budget-conscious user, I want to know if the current price I'm paying is a "good deal" compared to my history.

**The Logic (Pure Logic):** A mathematical module that calculates the delta between current price ($P_c$) and historical average ($\bar{P}$).

**Happy Path:** App displays: *"You are paying 5% less than your average price for this item."*

**Edge Case:** The user changes units (e.g., buying a 500g pack instead of 1kg). Logic must normalize to "Price per Unit."

**Failure States:** Division by zero if no quantity was recorded; logic must return `N/A` rather than an error.

**Design Rationale:** By keeping this as *Pure Logic*, we can run unit tests on thousands of price scenarios without needing a database or UI.

**Definition of Done:** The engine returns a correct Trend Value (`Up` / `Down` / `Stable`) for **100%** of items with at least one historical data point.

---

### 5. Hebrew Receipt Intelligence (OCR)

**User Story:** As a user, I want to scan my physical receipt to automate my price tracking.

**The Logic:** An image processing pipeline that utilizes OCR to detect Hebrew text and parse tabular data (Item, Weight, Price).

**Happy Path:** User snaps a clear photo; the app extracts 15 items and their prices correctly into the "Bought" log.

**Edge Cases:**
- Faded thermal paper; crumpled receipts
- "Buy 2 Get 1 Free" discounts that confuse the "Price per Item" logic

**Failure States:** Low confidence scores (`< 70%`); the app must prompt the user to "Manually Verify" rather than guessing.

**Design Rationale:** *Human-in-the-Loop Verification.* Since OCR isn't 100% perfect, the user acts as the final validator to ensure financial data is accurate.

**Definition of Done:** Successful extraction of **> 90%** of line items on a standard, high-contrast Israeli receipt.

---

### 6. Crowdsourced Price Benchmarking

**User Story:** As a shopper, I want to see the average market price for an item based on other users' recent purchases.

**The Logic (Pure Logic):** An aggregation engine that filters outliers and calculates a weighted average:

$$\text{Avg} = \frac{\sum (\text{Price} \times \text{Recency})}{\sum \text{Recency}}$$

**Happy Path:** User clicks an item and sees: *"National Avg: 12.50₪."*

**Edge Cases:** Malicious or erroneous data entry (e.g., a user entering 1,000₪ for bread).

**Failure States:** Insufficient data (fewer than 3 data points); the system must hide the benchmark to avoid misleading the user.

**Design Rationale:** *Statistical Winsorization.* We automatically ignore the top and bottom 5% of price entries to ensure the average isn't skewed by mistakes.

**Definition of Done:** A benchmark is displayed only when a statistically significant number of data points exist.

---

### 7. Geographic Value Optimizer (Store Suggestions)

**User Story:** As a user, I want the app to tell me which store near me will be the cheapest for my entire list.

**The Logic:** A "Total Basket" calculator that cross-references the user's list against the most recent crowdsourced data from nearby GPS coordinates.

**Happy Path:** App recommends *"Yochananof (2km away)"* because the total list is 30₪ cheaper than *"Shufersal (500m away)."*

**Edge Cases:** Half the items on the list have no recent data for the suggested store.

**Failure States:** GPS disabled; system defaults to "Last Known Location" or prompts for a City name.

**Design Rationale:** *Basket-Centric Optimization.* We prioritize the total trip cost (Total Basket + estimated travel effort) over individual item deals.

**Definition of Done:** The app generates a **Top 3 Stores** list based on the user's current active shopping list.

---

## Security & Data Handling Baseline

| Concern | Requirement |
|---|---|
| **PII Redaction (OCR)** | The OCR engine must automatically redact credit card digits, phone numbers, and cashier IDs from receipt images before uploading to the cloud. |
| **Anonymized Crowdsourcing** | User IDs must be decoupled from price data in the global database. We store *what* was bought and *where*, but never *by whom*. |
| **Hebrew Sanitization** | All text inputs are stripped of script tags to prevent Cross-Site Scripting (XSS) in collaborative lists. |
| **Tokenized Sharing** | List sharing is handled via unique, non-guessable UUIDs rather than simple sequential IDs. |

---

## Platform Selection: Mobile App (iOS & Android)
The core value of Salsala happens inside the supermarket. A native or hybrid mobile app is essential for:

Hardware Access: You need seamless access to the Camera for high-speed Hebrew OCR scanning and GPS for real-time "Store Suggestions" based on the user's current location.

User Friction: Shoppers need to pull their phone out, check an item, and put it back. Mobile apps offer the fastest "time-to-action" compared to a mobile browser.

Push Notifications: Essential for Live Collaborative Sync (e.g., "Your partner just added Milk to the list while you're at the store").

Offline Capability: Israeli supermarkets (especially basement levels) often have poor reception. A mobile app can cache the list and sync it once the user exits the "dead zone."

---

## Strategic Rationale

Salsala is designed to solve the **"Information Asymmetry"** in the Israeli grocery market. By combining:

- **OCR Automation** — reducing the friction of data entry for the user
- **Crowdsourced Intelligence** — providing genuine market value to the user

...the system creates a self-sustaining data loop.

The focus on **Pure Logic** for math and price comparison ensures the app remains fast and fully unit-testable, while the **Fail-Fast Security** approach protects user privacy in a highly sensitive financial context.