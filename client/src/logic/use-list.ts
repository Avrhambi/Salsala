/**
 * useList — orchestrates all shopping list operations.
 * Screens call this hook; no direct API imports in screen files.
 */
import { useCallback } from "react";
import { UUID } from "../../common/types";
import { addItemToList, createList, fetchList, removeItemFromList } from "../api/list.api";
import { useAppStore } from "../store/app-store";

export function useList() {
  const { setActiveList, setLoading, setError } = useAppStore();

  const loadList = useCallback(async (listId: UUID) => {
    setLoading(true);
    setError(null);
    try {
      const list = await fetchList(listId);
      setActiveList(list);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }, [setActiveList, setLoading, setError]);

  const startList = useCallback(async (userIds: UUID[]) => {
    setLoading(true);
    setError(null);
    try {
      const list = await createList(userIds);
      setActiveList(list);
      return list;
    } catch (err) {
      setError((err as Error).message);
      return null;
    } finally {
      setLoading(false);
    }
  }, [setActiveList, setLoading, setError]);

  const addItem = useCallback(async (listId: UUID, itemId: UUID, quantity: number) => {
    setError(null);
    try {
      const updated = await addItemToList(listId, itemId, quantity);
      setActiveList(updated);
    } catch (err) {
      setError((err as Error).message);
    }
  }, [setActiveList, setError]);

  const removeItem = useCallback(async (listId: UUID, itemId: UUID) => {
    setError(null);
    try {
      const updated = await removeItemFromList(listId, itemId);
      setActiveList(updated);
    } catch (err) {
      setError((err as Error).message);
    }
  }, [setActiveList, setError]);

  return { loadList, startList, addItem, removeItem };
}
