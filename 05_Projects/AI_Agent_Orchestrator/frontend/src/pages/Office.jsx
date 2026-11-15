import { useEffect, useState } from "react";

import { api } from "../api";

const AGENT_META = {
  antigravity: { label: "Antigravity", icon: "💻", desk: "code" },
  muse: { label: "Muse", icon: "🎬", desk: "video" },
  python: { label: "Python", icon: "🐍", desk: "script" },
  qa: { label: "QA", icon: "🔍", desk: "checklist" },
  publisher: { label: "Publisher", icon: "📤", desk: "upload" },
};

const PENDING_STATUSES = new Set(["PENDING", "ASSIGNED", "RUNNING", "REVIEW"]);

function moodOf(agent) {
  if (agent.status === "ERROR") return "error";
  if (agent.status === "BUSY") return "busy";
  return "idle";
}

const FACES = {
  idle: "😌",
  busy: "😣",
  error: "😵",
};

const FLAVOR = {
  idle: "Rảnh rang, chưa có việc.",
  busy: "Đang cày hùng hục...",
  error: "Gặp lỗi, cần xem log!",
};

function HpBar({ percent, mood }) {
  return (
    <div className="hp-track" title={`${percent}/100`}>
      <div className={`hp-fill hp-${mood}`} style={{ width: `${percent}%` }} />
    </div>
  );
}

export default function Office() {
  const [agents, setAgents] = useState([]);
  const [pendingByType, setPendingByType] = useState({});
  const [error, setError] = useState(null);

  async function load() {
    try {
      const [agentList, tasks] = await Promise.all([api.listAgents(), api.listTasks({ limit: 100 })]);
      setAgents(agentList);

      const counts = {};
      for (const task of tasks) {
        if (PENDING_STATUSES.has(task.status)) {
          counts[task.assigned_agent] = (counts[task.assigned_agent] || 0) + 1;
        }
      }
      setPendingByType(counts);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
    const timer = setInterval(load, 2500);
    return () => clearInterval(timer);
  }, []);

  const boss = agents.find((agent) => agent.type === "claude");
  const workers = agents.filter((agent) => agent.type !== "claude");
  const totalBusy = workers.filter((agent) => agent.status === "BUSY").length;
  const totalPending = Object.values(pendingByType).reduce((sum, count) => sum + count, 0);

  return (
    <div>
      <h2>Văn phòng</h2>
      <p className="hint">
        Mỗi phòng là một agent thật, lấy đúng trạng thái từ <code>/agents</code> và <code>/tasks</code> — không phải
        hình minh họa tĩnh. Thanh máu = số việc đang chờ/đang chạy của agent đó; hết việc là hết máu (nghỉ ngơi).
      </p>
      {error && <div className="error">{error}</div>}

      <div className="office-grid">
        <div className="room boss-room">
          <div className="room-header">
            <span className="room-icon">🏢</span>
            <span className="room-title">Sếp Claude</span>
          </div>
          <div className="character boss-character">🫃</div>
          <div className="speech-bubble">
            {totalBusy > 0
              ? `Đang có ${totalBusy} đứa cày việc, ${totalPending} việc trong hàng đợi. Tốt lắm!`
              : "Cả văn phòng đang rảnh. Giao thêm việc đi chứ!"}
          </div>
          <div className="boss-status">
            {boss ? `Trạng thái: ${boss.status}` : "Đang tải..."}
          </div>
        </div>

        {Object.entries(AGENT_META).map(([type, meta]) => {
          const agent = workers.find((worker) => worker.type === type);
          const mood = agent ? moodOf(agent) : "idle";
          const pending = pendingByType[type] || 0;
          const hp = Math.min(100, pending * 34);

          return (
            <div className={`room worker-room mood-${mood}`} key={type}>
              <div className="room-header">
                <span className="room-icon">{meta.icon}</span>
                <span className="room-title">{meta.label}</span>
              </div>
              <div className={`character worker-character mood-${mood}`}>{FACES[mood]}</div>
              <div className="worker-task">
                {agent?.current_task ? `Đang làm: ${agent.current_task}` : FLAVOR[mood]}
              </div>
              <HpBar percent={hp} mood={mood} />
              <div className="hp-label">
                Việc đang chờ/chạy: {pending}
              </div>
              {agent?.error_log && mood === "error" && (
                <div className="worker-error" title={agent.error_log}>
                  {agent.error_log.slice(0, 60)}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
