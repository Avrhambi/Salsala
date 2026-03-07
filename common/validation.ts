/**
 * Zod validation schemas — mirrors Pydantic validators in server/models/*.py.
 * Import these in the mobile client to validate API responses at the boundary.
 */

import { z } from "zod";

// ── Primitives ───────────────────────────────────────────────────────────────

export const UUIDSchema = z.string().uuid();

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

// ── server/models/user.py ────────────────────────────────────────────────────

export const UserSchema = z.object({
  user_id: UUIDSchema,
  display_name: z.string().trim().min(1, "display_name must not be empty."),
});

// ── Inferred types ────────────────────────────────────────────────────────────

export type ItemInput = z.infer<typeof ItemSchema>;
export type ShoppingListInput = z.infer<typeof ShoppingListSchema>;
export type UserInput = z.infer<typeof UserSchema>;
