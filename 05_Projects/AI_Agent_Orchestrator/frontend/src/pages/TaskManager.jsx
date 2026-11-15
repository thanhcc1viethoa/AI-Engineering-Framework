import { Fragment, useEffect, useState } from "react";

import { api } from "../api";

const STATUSES = ["", "PENDING", "QUEUED", "RUNNING", "WAITING", "COMPLETED", "FAILED", "CANCELLED"];
const AGENTS = ["antigravity", "muse", "python", "qa"];
const CANCELLABLE = ["PENDING", "QUEUED", "RUNNING"];

export default function TaskManager() {
  const [tasks, setTasks] = useState([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [search, setSearch] = useState("");
  const [expandedId, setExpandedId] = useState(null);
  const [form, setForm] = useState({
    task_name: "",
    assigned_agent: "python",
    description: "",
    payloadText: "{}",
  });
  const [formError, setFormError] = useState(null);

  async function load() {
    const params = statusFilter ? { status: statusFilter } : {};
    setTasks(await api.listTasks(params));
  }

  useEffect(() => {
    load();
    const timer = setInterval(load, 3000);
    return () => clearInterval(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter]);

  async function handleCreate(event) {
    event.preventDefault();
    setFormError(null);

    let payload;
    try {
      payload = JSON.parse(form.payloadText || "{}");
    } catch {
      setFormError("Payload phải là JSON hợp lệ.");
      return;
    }

    try {
      await api.submitTask({
        task_name: form.task_name,
        description: form.description || null,
        assigned_agent: form.assigned_agent,
        payload,
      });
      setForm({ ...form, task_name: "", description: "", payloadText: "{}" });
      load();
    } catch (err) {
      setFormError(err.message);
    }
  }

  async function handleCancel(taskId) {
    await api.cancelTask(taskId);
    load();
  }

  const filtered = tasks.filter((task) =>
    task.task_name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <h2>Quản lý nhiệm vụ</h2>

      <form className="panel" onSubmit={handleCreate}>
        <h3>Tạo nhiệm vụ mới</h3>
        <input
          placeholder="Tên nhiệm vụ"
          value={form.task_name}
          onChange={(event) => setForm({ ...form, task_name: event.target.value })}
          required
        />
        <select
          value={form.assigned_agent}
          onChange={(event) => setForm({ ...form, assigned_agent: event.target.value })}
        >
          {AGENTS.map((agent) => (
            <option key={agent} value={agent}>
              {agent}
            </option>
          ))}
        </select>
        <input
          placeholder="Mô tả (tùy chọn)"
          value={form.description}
          onChange={(event) => setForm({ ...form, description: event.target.value })}
        />
        <textarea
          placeholder="Payload (JSON)"
          value={form.payloadText}
          onChange={(event) => setForm({ ...form, payloadText: event.target.value })}
        />
        <button type="submit">Tạo nhiệm vụ</button>
        {formError && <div className="error">{formError}</div>}
      </form>

      <div className="filters">
        <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>
          {STATUSES.map((status) => (
            <option key={status} value={status}>
              {status || "Tất cả trạng thái"}
            </option>
          ))}
        </select>
        <input
          placeholder="Tìm theo tên nhiệm vụ..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
      </div>

      <table>
        <thead>
          <tr>
            <th>Tên</th>
            <th>Agent</th>
            <th>Trạng thái</th>
            <th>Tạo lúc</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((task) => (
            <Fragment key={task.task_id}>
              <tr>
                <td>{task.task_name}</td>
                <td>{task.assigned_agent}</td>
                <td>
                  <span className={`status status-${task.status.toLowerCase()}`}>{task.status}</span>
                </td>
                <td>{task.created_at}</td>
                <td>
                  <button onClick={() => setExpandedId(expandedId === task.task_id ? null : task.task_id)}>
                    {expandedId === task.task_id ? "Ẩn" : "Xem kết quả"}
                  </button>
                  {CANCELLABLE.includes(task.status) && (
                    <button onClick={() => handleCancel(task.task_id)}>Dừng</button>
                  )}
                </td>
              </tr>
              {expandedId === task.task_id && (
                <tr>
                  <td colSpan={5}>
                    <pre>{JSON.stringify(task, null, 2)}</pre>
                  </td>
                </tr>
              )}
            </Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
}
