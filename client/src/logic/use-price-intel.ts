/**
 * usePriceIntel — fetches and caches price trend for a single item.
 * Reads from the global store cache first; only hits the API on a miss.
 */
import { useEffect } from "react";
import { TrendValue, UUID } from "../../common/types";
import { apiClient } from "../api/client";
import { useAppStore } from "../store/app-store";

export function usePriceIntel(itemId: UUID | null): TrendValue | null {
  const priceTrends = useAppStore((s) => s.priceTrends);
  const setPriceTrend = useAppStore((s) => s.setPriceTrend);

  useEffect(() => {
    if (!itemId || priceTrends[itemId]) return;

    apiClient
      .get<{ trend: TrendValue }>(`/item/${itemId}/trend`)
      .then(({ data }) => {
        setPriceTrend(itemId, data.trend);
      })
      .catch(() => {
        setPriceTrend(itemId, TrendValue.NA);
      });
  }, [itemId, priceTrends, setPriceTrend]);

  return itemId ? (priceTrends[itemId] ?? null) : null;
}
