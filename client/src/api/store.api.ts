/**
 * Store / Geo resource API calls — mirrors routes/store.py.
 * Returns ranked store recommendations for the active shopping list.
 */
import { GeoCoordinates, StoreRank, UUID } from "../../common/types";
import { StoreRankSchema } from "../../common/validation";
import { z } from "zod";
import { apiClient } from "./client";

export async function fetchStoreRecommendations(
  listId: UUID,
  coordinates: GeoCoordinates
): Promise<StoreRank[]> {
  const { data } = await apiClient.get(`/store/recommend`, {
    params: {
      list_id: listId,
      lat: coordinates.latitude,
      lng: coordinates.longitude,
    },
  });
  return z.array(StoreRankSchema).parse(data);
}
