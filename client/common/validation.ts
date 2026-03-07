/**
 * Zod validation schemas — mirrors all Pydantic validators in server/models/*.py.
 * Import these in the mobile client to validate API responses and user input
 * before they reach application state.
 */

import { z } from "zod";
import { TrendValue } from "./types";

// ── Primitives ───────────────────────────────────────────────────────────────

export const UUIDSchema = z.string().uuid();

// ── shared/types.py ──────────────────────────────────────────────────────────

export const TrendValueSchema = z.nativeEnum(TrendValue);

export const GeoCoordinatesSchema = z.object({
  latitude: z.number().min(-90).max(90),
  longitude: z.number().min(-180).max(180),
});

// ── server/models/item.py ────────────────────────────────────────────────────

export const ItemSchema = z.object({
  id: UUIDSchema,
  name_hebrew: z.string().trim().min(1, "name_hebrew must not be empty."),
  default_quantity: z.number().int().min(0),
  is_bought: z.boolean(),
});

// ── server/models/list.py ────────────────────────────────────────────────────

export const ShoppingListSchema = z.object({
  list_id: UUIDSchema,
  name: z.string().trim().min(1, "List name must not be empty."),
  users: z.array(UUIDSchema).min(1, "A ShoppingList must have at least one user."),
  items: z.array(ItemSchema),
  is_completed: z.boolean(),
  completed_at: z.string().nullable(),
});

// ── server/models/transaction.py ─────────────────────────────────────────────

export const TransactionSchema = z.object({
  transaction_id: UUIDSchema,
  item_id: UUIDSchema,
  price: z.number().gt(0, "Price must be strictly greater than 0."),
  quantity: z.number().gt(0, "quantity must be greater than 0."),
  store_name: z.string().trim().min(1, "store_name must not be empty."),
  timestamp: z.string().datetime(),
});

// ── server/models/receipt.py ─────────────────────────────────────────────────

export const ReceiptSchema = z.object({
  receipt_id: UUIDSchema,
  image_url: z.string().trim().min(1, "image_url must not be empty."),
  confidence_score: z.number().min(0).max(1),
  requires_human_verification: z.boolean(),
  parsed_items: z.array(TransactionSchema),
});

// ── server/models/benchmark.py ───────────────────────────────────────────────

export const BenchmarkSchema = z.object({
  item_id: UUIDSchema,
  store_id: UUIDSchema,
  national_avg: z.number().min(0),
  data_points: z.number().int().min(1),
});

// ── server/models/store.py ───────────────────────────────────────────────────

export const StoreSchema = z.object({
  store_id: UUIDSchema,
  name: z.string().trim().min(1, "Store name must not be empty."),
  coordinates: GeoCoordinatesSchema,
  chain: z.string().trim().min(1, "Store chain must not be empty."),
});

// ── server/models/user.py ────────────────────────────────────────────────────

export const UserSchema = z.object({
  user_id: UUIDSchema,
  display_name: z.string().trim().min(1, "display_name must not be empty."),
  last_known_location: GeoCoordinatesSchema.nullish(),
});

// ── server/core/geo_optimizer.py ─────────────────────────────────────────────

export const StoreRankSchema = z.object({
  store_id: UUIDSchema,
  total_basket_cost: z.number().min(0),
  item_count: z.number().int().min(0),
  distance_km: z.number().min(0),
  store_name: z.string(),
});

// ── Inferred types (use these instead of manual interfaces where convenient) ──

export type ItemInput = z.infer<typeof ItemSchema>;
export type ShoppingListInput = z.infer<typeof ShoppingListSchema>;
export type TransactionInput = z.infer<typeof TransactionSchema>;
export type ReceiptInput = z.infer<typeof ReceiptSchema>;
export type BenchmarkInput = z.infer<typeof BenchmarkSchema>;
export type StoreInput = z.infer<typeof StoreSchema>;
export type UserInput = z.infer<typeof UserSchema>;
