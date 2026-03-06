/**
 * useSync — manages the WebSocket connection for live collaborative list sync.
 * Opens a socket on mount, applies server-pushed list updates to the store,
 * and cleans up on unmount.
 */
import { useEffect, useRef } from "react";
import { createListSocket, sendListUpdate } from "../api/websocket";
import { useAppStore } from "../store/app-store";

export function useSync(listId: string | null) {
  const socketRef = useRef<WebSocket | null>(null);
  const setActiveList = useAppStore((s) => s.setActiveList);
  const setError = useAppStore((s) => s.setError);

  useEffect(() => {
    if (!listId) return;

    const socket = createListSocket(
      listId,
      (updatedList) => setActiveList(updatedList),
      () => setError("Live sync connection lost. Reconnecting…")
    );
    socketRef.current = socket;

    return () => {
      socket.close();
      socketRef.current = null;
    };
  }, [listId, setActiveList, setError]);

  const pushUpdate = (payload: object) => {
    if (socketRef.current) {
      sendListUpdate(socketRef.current, payload);
    }
  };

  return { pushUpdate };
}
