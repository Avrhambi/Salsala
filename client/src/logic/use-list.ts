/**
 * useList — orchestrates all shopping list operations.
 * Screens call this hook; no direct API imports in screen files.
 */
import { useCallback } from "react";
import { UUID } from "../../common/types";
import { ShoppingList } from "../../common/types";
import {
  addItemToList,
  createList,
  deleteList,
  fetchHistory,
  fetchList,
  markItemBought,
  removeItemFromList,
  renameList,
} from "../api/list.api";
import { useAppStore } from "../store/app-store";

export function useList() {
  const { setActiveList, setLists, upsertList, removeList, setHistory, setLoading, setError } =
    useAppStore();

  const startList = useCallback(
    async (userIds: UUID[], name: string) => {
      setLoading(true);
      setError(null);
      try {
        const list = await createList(userIds, name);
        upsertList(list);
        setActiveList(list);
        return list;
      } catch (err) {
        setError((err as Error).message);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [upsertList, setActiveList, setLoading, setError]
  );

  const loadList = useCallback(
    async (listId: UUID) => {
      setLoading(true);
      setError(null);
      try {
        const list = await fetchList(listId);
        setActiveList(list);
        upsertList(list);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    },
    [setActiveList, upsertList, setLoading, setError]
  );

  const rename = useCallback(
    async (listId: UUID, name: string) => {
      setError(null);
      try {
        const updated = await renameList(listId, name);
        upsertList(updated);
        setActiveList(updated);
      } catch (err) {
        setError((err as Error).message);
      }
    },
    [upsertList, setActiveList, setError]
  );

  const remove = useCallback(
    async (listId: UUID) => {
      setError(null);
      try {
        await deleteList(listId);
        removeList(listId);
        setActiveList(null);
      } catch (err) {
        setError((err as Error).message);
      }
    },
    [removeList, setActiveList, setError]
  );

  const addItem = useCallback(
    async (listId: UUID, itemId: string, quantity: number) => {
      setError(null);
      try {
        const updated = await addItemToList(listId, itemId, quantity);
        upsertList(updated);
        setActiveList(updated);
      } catch (err) {
        setError((err as Error).message);
      }
    },
    [upsertList, setActiveList, setError]
  );

  const removeItem = useCallback(
    async (listId: UUID, itemId: UUID) => {
      setError(null);
      try {
        const updated = await removeItemFromList(listId, itemId);
        upsertList(updated);
        setActiveList(updated);
      } catch (err) {
        setError((err as Error).message);
      }
    },
    [upsertList, setActiveList, setError]
  );

  const markBought = useCallback(
    async (listId: UUID, itemId: UUID) => {
      setError(null);
      try {
        const updated = await markItemBought(listId, itemId);
        if (updated.is_completed) {
          removeList(listId);
          setActiveList(null);
        } else {
          upsertList(updated);
          setActiveList(updated);
        }
      } catch (err) {
        setError((err as Error).message);
      }
    },
    [upsertList, removeList, setActiveList, setError]
  );

  const loadHistory = useCallback(
    async (userId: UUID) => {
      setError(null);
      try {
        const completed = await fetchHistory(userId);
        setHistory(completed);
      } catch (err) {
        setError((err as Error).message);
      }
    },
    [setHistory, setError]
  );

  const reuseList = useCallback(
    async (source: ShoppingList) => {
      const uid = useAppStore.getState().userId;
      setLoading(true);
      setError(null);
      try {
        let current = await createList(uid ? [uid] : [], source.name);
        for (const item of source.items) {
          current = await addItemToList(current.list_id, item.id, item.default_quantity);
        }
        upsertList(current);
        setActiveList(current);
        return current;
      } catch (err) {
        setError((err as Error).message);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [upsertList, setActiveList, setLoading, setError]
  );

  return { startList, loadList, rename, remove, addItem, removeItem, markBought, loadHistory, reuseList };
}
