/**
 * Global Zustand state — single store for the whole app.
 * Screens and hooks read/write here; no prop-drilling required.
 */
import { create } from "zustand";
import { ShoppingList, UUID } from "../../common/types";

interface AppState {
  // All active (non-completed) lists for the current user
  lists: ShoppingList[];
  setLists: (lists: ShoppingList[]) => void;
  upsertList: (list: ShoppingList) => void;
  removeList: (listId: UUID) => void;

  // Currently opened list (drill-down view)
  activeList: ShoppingList | null;
  setActiveList: (list: ShoppingList | null) => void;

  // Completed lists (History tab)
  history: ShoppingList[];
  setHistory: (lists: ShoppingList[]) => void;

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
  lists: [],
  setLists: (lists) => set({ lists }),
  upsertList: (list) =>
    set((state) => {
      const existing = state.lists.findIndex((l) => l.list_id === list.list_id);
      if (existing >= 0) {
        const updated = [...state.lists];
        updated[existing] = list;
        return { lists: updated };
      }
      return { lists: [...state.lists, list] };
    }),
  removeList: (listId) =>
    set((state) => ({ lists: state.lists.filter((l) => l.list_id !== listId) })),

  activeList: null,
  setActiveList: (list) => set({ activeList: list }),

  history: [],
  setHistory: (lists) => set({ history: lists }),

  userId: null,
  setUserId: (id) => set({ userId: id }),

  isLoading: false,
  setLoading: (loading) => set({ isLoading: loading }),

  error: null,
  setError: (message) => set({ error: message }),
}));
