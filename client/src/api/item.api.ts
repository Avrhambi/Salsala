/**
 * Item resource API calls — mirrors routes/item.py (NLP Hebrew search).
 */
import { Item } from "../../common/types";
import { ItemSchema } from "../../common/validation";
import { z } from "zod";
import { apiClient } from "./client";

export async function searchItems(query: string): Promise<Item[]> {
  const { data } = await apiClient.get("/item/search", {
    params: { q: query },
  });
  return z.array(ItemSchema).parse(data);
}

export async function fetchItem(itemId: string): Promise<Item> {
  const { data } = await apiClient.get(`/item/${itemId}`);
  return ItemSchema.parse(data);
}
