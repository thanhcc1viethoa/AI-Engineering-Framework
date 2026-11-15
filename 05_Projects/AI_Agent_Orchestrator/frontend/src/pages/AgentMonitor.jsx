import { useEffect, useState } from "react";

import { api } from "../api";

export default function AgentMonitor() {
  const [agents, setAgents] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        setAgents(await api.listAgents());
        setError(null);
      } catch (err) {
        setError(err.message);
      }
    }
    load();
    const timer = setInterval(load, 3000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div>
      <h2>Giám sát Agent</h2>
      {error && <div className="error">{error}</div>}
      <table>
        <thead>
          <tr>
            <th>Agent</th>
            <th>Loại</th>
            <th>Trạng thái</th>
            <th>Nhiệm vụ hiện tại</th>
            <th>Hoạt động lần cuối</th>
            <th>Lỗi gần nhất</th>
          </tr>
        </thead>
        <tbody>
          {agents.map((agent) => (
            <tr key={agent.agent_id}>
              <td>{agent.name}</td>
              <td>{agent.type}</td>
              <td>
                <span className={`status status-${agent.status.toLowerCase()}`}>{agent.status}</span>
              </td>
              <td>{agent.current_task || "—"}</td>
              <td>{agent.last_active || "—"}</td>
              <td>{agent.error_log || "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
