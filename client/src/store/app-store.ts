/**
 * Global Zustand state — single store for the whole app.
 * Screens and hooks read/write here; no prop-drilling required.
 */
import { create } from "zustand";
import { Item, ShoppingList, StoreRank, TrendValue, UUID } from "../../common/types";

interface AppState {
  // Active shopping list
  activeList: ShoppingList | null;
  setActiveList: (list: ShoppingList) => void;

  // Item search results (NLP)
  searchResults: Item[];
  setSearchResults: (items: Item[]) => void;

  // Store recommendations
  storeRankings: StoreRank[];
  setStoreRankings: (rankings: StoreRank[]) => void;

  // Price trend cache: item_id → TrendValue
  priceTrends: Record<UUID, TrendValue>;
  setPriceTrend: (itemId: UUID, trend: TrendValue) => void;

  // Current user
  userId: UUID | null;
  setUserId: (id: UUID) => void;

  // Global loading / error state
  isLoading: boolean;
  setLoading: (loading: boolean) => void;
  error: string | null;
  setError: (message: string | null) => void;
}

export const useAppStore = create<AppState>((set) => ({
  activeList: null,
  setActiveList: (list) => set({ activeList: list }),

  searchResults: [],
  setSearchResults: (items) => set({ searchResults: items }),

  storeRankings: [],
  setStoreRankings: (rankings) => set({ storeRankings: rankings }),

  priceTrends: {},
  setPriceTrend: (itemId, trend) =>
    set((state) => ({ priceTrends: { ...state.priceTrends, [itemId]: trend } })),

  userId: null,
  setUserId: (id) => set({ userId: id }),

  isLoading: false,
  setLoading: (loading) => set({ isLoading: loading }),

  error: null,
  setError: (message) => set({ error: message }),
}));
