/**
 * Shared TypeScript types — mirrors shared/types.py and server/models/*.py.
 * These are the canonical data shapes exchanged between the mobile client
 * and the FastAPI backend over REST and WebSocket.
 */

// ── Primitives ───────────────────────────────────────────────────────────────

/** Non-guessable UUID string (RFC 4122). */
export type UUID = string;

// ── shared/types.py ──────────────────────────────────────────────────────────

/** Directional price trend returned by the Price Intelligence Engine. */
export enum TrendValue {
  UP = "UP",
  DOWN = "DOWN",
  STABLE = "STABLE",
  NA = "N/A",
}

/** Geographic coordinate pair used by the Geographic Value Optimizer. */
export interface GeoCoordinates {
  latitude: number;
  longitude: number;
}

// ── server/models/item.py ────────────────────────────────────────────────────

export interface Item {
  id: UUID;
  name_hebrew: string;
  default_quantity: number;
}

// ── server/models/list.py ────────────────────────────────────────────────────

export interface ShoppingList {
  list_id: UUID;
  users: UUID[];
  items: Item[];
  sync_timestamp: string; // ISO 8601 datetime string
}

// ── server/models/transaction.py ─────────────────────────────────────────────

export interface Transaction {
  transaction_id: UUID;
  item_id: UUID;
  price: number; // strictly > 0
  quantity: number; // strictly > 0
  store_name: string;
  timestamp: string; // ISO 8601 datetime string
}

// ── server/models/receipt.py ─────────────────────────────────────────────────

export interface Receipt {
  receipt_id: UUID;
  image_url: string;
  confidence_score: number; // 0.0 – 1.0
  requires_human_verification: boolean;
  parsed_items: Transaction[];
}

// ── server/models/benchmark.py ───────────────────────────────────────────────

export interface Benchmark {
  item_id: UUID;
  store_id: UUID;
  national_avg: number;
  data_points: number;
}

// ── server/models/store.py ───────────────────────────────────────────────────

export interface Store {
  store_id: UUID;
  name: string;
  coordinates: GeoCoordinates;
  chain: string; // e.g. "Shufersal", "Rami Levy"
}

// ── server/models/user.py ────────────────────────────────────────────────────

export interface User {
  user_id: UUID;
  display_name: string;
  last_known_location?: GeoCoordinates;
}

// ── server/core/geo_optimizer.py ─────────────────────────────────────────────

export interface StoreRank {
  store_id: UUID;
  total_basket_cost: number;
  item_count: number;
}
