/**
 * WebSocket client for real-time list sync — /list/ws/{list_id}.
 * Wraps the native WebSocket API with connect/disconnect/send helpers.
 */
import Constants from "expo-constants";
import { ShoppingList } from "../../common/types";
import { ShoppingListSchema } from "../../common/validation";

const WS_BASE: string =
  (Constants.expoConfig?.extra?.wsBaseUrl as string) ?? "ws://localhost:8000";

export type SyncHandler = (list: ShoppingList) => void;
export type ErrorHandler = (error: Event) => void;

export function createListSocket(
  listId: string,
  onSync: SyncHandler,
  onError?: ErrorHandler
): WebSocket {
  const socket = new WebSocket(`${WS_BASE}/list/ws/${listId}`);

  socket.onmessage = (event: MessageEvent) => {
    try {
      const raw = JSON.parse(event.data as string);
      const list = ShoppingListSchema.parse(raw);
      onSync(list);
    } catch (err) {
      console.warn("[websocket] Malformed frame dropped:", err);
    }
  };

  if (onError) {
    socket.onerror = onError;
  }

  return socket;
}

export function sendListUpdate(socket: WebSocket, payload: object): void {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(payload));
  }
}
