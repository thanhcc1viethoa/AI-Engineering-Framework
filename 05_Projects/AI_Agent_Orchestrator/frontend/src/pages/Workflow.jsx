import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { api } from "../api";

export default function Workflow() {
  const { workflowId } = useParams();
  const [idInput, setIdInput] = useState(workflowId || "");
  const [workflow, setWorkflow] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState(null);

  async function load(id) {
    if (!id) return;
    try {
      const wf = await api.getWorkflow(id);
      setWorkflow(wf);
      const details = await Promise.all(wf.task_ids.map((taskId) => api.getTask(taskId)));
      setTasks(details);
      setError(null);
    } catch (err) {
      setError(err.message);
      setWorkflow(null);
    }
  }

  useEffect(() => {
    if (!workflowId) return;
    load(workflowId);
    const timer = setInterval(() => load(workflowId), 3000);
    return () => clearInterval(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [workflowId]);

  return (
    <div>
      <h2>Workflow</h2>

      <div className="filters">
        <input
          placeholder="Nhập workflow_id (vd. wf-xxxxxxxx)..."
          value={idInput}
          onChange={(event) => setIdInput(event.target.value)}
        />
        <button onClick={() => load(idInput)}>Xem</button>
      </div>

      {error && <div className="error">{error}</div>}

      {workflow && (
        <>
          <p>
            <strong>{workflow.workflow_name}</strong> — mục tiêu: {workflow.goal}
          </p>
          <p>
            Trạng thái:{" "}
            <span className={`status status-${workflow.status.toLowerCase()}`}>{workflow.status}</span>
          </p>

          <div className="workflow-diagram">
            {tasks.map((task, index) => (
              <div className="workflow-step" key={task.task_id}>
                <div className={`workflow-box status-${task.status.toLowerCase()}`}>
                  <div className="workflow-agent">{task.assigned_agent}</div>
                  <div>{task.task_name}</div>
                  <div className="workflow-status">{task.status}</div>
                </div>
                {index < tasks.length - 1 && <div className="workflow-arrow">→</div>}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
