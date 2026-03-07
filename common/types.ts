/**
 * Shared TypeScript types — mirrors server/models/*.py.
 * These are the canonical data shapes exchanged between the mobile client
 * and the FastAPI backend over REST.
 */

// ── Primitives ───────────────────────────────────────────────────────────────

/** Non-guessable UUID string (RFC 4122). */
export type UUID = string;

// ── server/models/item.py ────────────────────────────────────────────────────

export interface Item {
  id: UUID;
  name_hebrew: string;
  default_quantity: number;
  is_bought: boolean;
}

// ── server/models/list.py ────────────────────────────────────────────────────

export interface ShoppingList {
  list_id: UUID;
  name: string;
  users: UUID[];
  items: Item[];
  is_completed: boolean;
  completed_at: string | null; // ISO 8601 datetime string or null
}

// ── server/models/user.py ────────────────────────────────────────────────────

export interface User {
  user_id: UUID;
  display_name: string;
}
