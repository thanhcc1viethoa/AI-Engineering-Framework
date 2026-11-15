import { useEffect, useRef, useState } from "react";

import { api } from "../api";

export default function SystemLogs() {
  const [lines, setLines] = useState([]);
  const [error, setError] = useState(null);
  const preRef = useRef(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await api.getSystemLogs(300);
        setLines(data.lines);
        setError(null);
      } catch (err) {
        setError(err.message);
      }
    }
    load();
    const timer = setInterval(load, 3000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (preRef.current) preRef.current.scrollTop = preRef.current.scrollHeight;
  }, [lines]);

  return (
    <div>
      <h2>Log hệ thống</h2>
      {error && <div className="error">{error}</div>}
      <pre className="log-view" ref={preRef}>
        {lines.length ? lines.join("\n") : "Chưa có log nào."}
      </pre>
    </div>
  );
}
