/**
 * List resource API calls — mirrors routes/list.py on the backend.
 * Validates responses with Zod before returning (fail-fast at boundary).
 */
import { ShoppingList, UUID } from "../../common/types";
import { ShoppingListSchema } from "../../common/validation";
import { z } from "zod";
import { apiClient } from "./client";

export async function createList(userIds: UUID[], name: string): Promise<ShoppingList> {
  const { data } = await apiClient.post("/list/create", { users: userIds, name });
  return ShoppingListSchema.parse(data);
}

export async function fetchList(listId: UUID): Promise<ShoppingList> {
  const { data } = await apiClient.get(`/list/${listId}`);
  return ShoppingListSchema.parse(data);
}

export async function renameList(listId: UUID, name: string): Promise<ShoppingList> {
  const { data } = await apiClient.patch(`/list/${listId}`, { name });
  return ShoppingListSchema.parse(data);
}

export async function deleteList(listId: UUID): Promise<void> {
  await apiClient.delete(`/list/${listId}`);
}

export async function addItemToList(listId: UUID, itemId: string, quantity: number): Promise<ShoppingList> {
  const { data } = await apiClient.post(`/list/${listId}/items`, { item_id: itemId, quantity });
  return ShoppingListSchema.parse(data);
}

export async function removeItemFromList(listId: UUID, itemId: UUID): Promise<ShoppingList> {
  const { data } = await apiClient.delete(`/list/${listId}/items/${itemId}`);
  return ShoppingListSchema.parse(data);
}

export async function markItemBought(listId: UUID, itemId: UUID): Promise<ShoppingList> {
  const { data } = await apiClient.patch(`/list/${listId}/items/${itemId}/bought`);
  return ShoppingListSchema.parse(data);
}

export async function fetchHistory(userId: UUID): Promise<ShoppingList[]> {
  const { data } = await apiClient.get(`/list/history/${userId}`);
  return z.array(ShoppingListSchema).parse(data);
}
