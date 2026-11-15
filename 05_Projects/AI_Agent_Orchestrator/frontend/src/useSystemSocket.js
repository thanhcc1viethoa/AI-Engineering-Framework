import { useEffect, useState } from "react";

import { API_BASE } from "./api";

/** Pushes SystemStatus roughly every 2s — Requirement.md FR-019. */
export function useSystemSocket() {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    const wsUrl = `${API_BASE.replace(/^http/, "ws")}/ws`;
    let socket;
    let stopped = false;

    function connect() {
      socket = new WebSocket(wsUrl);
      socket.onmessage = (event) => setStatus(JSON.parse(event.data));
      socket.onclose = () => {
        if (!stopped) setTimeout(connect, 2000);
      };
      socket.onerror = () => socket.close();
    }

    connect();
    return () => {
      stopped = true;
      socket?.close();
    };
  }, []);

  return status;
}
