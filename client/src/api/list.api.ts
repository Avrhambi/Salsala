/**
 * List resource API calls — mirrors routes/list.py on the backend.
 * Validates responses with Zod before returning (fail-fast at boundary).
 */
import { ShoppingList, UUID } from "../../common/types";
import { ShoppingListSchema } from "../../common/validation";
import { apiClient } from "./client";

export async function fetchList(listId: UUID): Promise<ShoppingList> {
  const { data } = await apiClient.get(`/list/${listId}`);
  return ShoppingListSchema.parse(data);
}

export async function createList(userIds: UUID[]): Promise<ShoppingList> {
  const { data } = await apiClient.post("/list", { users: userIds });
  return ShoppingListSchema.parse(data);
}

export async function addItemToList(listId: UUID, itemId: UUID, quantity: number): Promise<ShoppingList> {
  const { data } = await apiClient.post(`/list/${listId}/items`, {
    item_id: itemId,
    quantity,
  });
  return ShoppingListSchema.parse(data);
}

export async function removeItemFromList(listId: UUID, itemId: UUID): Promise<ShoppingList> {
  const { data } = await apiClient.delete(`/list/${listId}/items/${itemId}`);
  return ShoppingListSchema.parse(data);
}
