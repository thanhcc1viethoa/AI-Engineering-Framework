import { useEffect, useState } from "react";

import { api } from "../api";

export default function VideoManager() {
  const [videos, setVideos] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        setVideos(await api.listTasks({ assigned_agent: "muse" }));
        setError(null);
      } catch (err) {
        setError(err.message);
      }
    }
    load();
    const timer = setInterval(load, 5000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div>
      <h2>Quản lý video</h2>
      {error && <div className="error">{error}</div>}
      <table>
        <thead>
          <tr>
            <th>Tên</th>
            <th>Tạo lúc</th>
            <th>Trạng thái</th>
            <th>Đường dẫn file</th>
            <th>Yêu cầu tạo video</th>
          </tr>
        </thead>
        <tbody>
          {videos.map((video) => (
            <tr key={video.task_id}>
              <td>{video.task_name}</td>
              <td>{video.created_at}</td>
              <td>
                <span className={`status status-${video.status.toLowerCase()}`}>{video.status}</span>
              </td>
              <td>{video.output_path || "—"}</td>
              <td>
                <code>{JSON.stringify(video.payload)}</code>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {videos.length === 0 && <p>Chưa có yêu cầu tạo video nào.</p>}
    </div>
  );
}
