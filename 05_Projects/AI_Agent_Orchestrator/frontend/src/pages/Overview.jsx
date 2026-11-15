import { useSystemSocket } from "../useSystemSocket";

const CARDS = [
  ["agents_total", "Tổng số Agent"],
  ["agents_active", "Agent đang hoạt động"],
  ["tasks_running", "Nhiệm vụ đang chạy"],
  ["tasks_completed", "Nhiệm vụ hoàn thành"],
  ["tasks_failed", "Nhiệm vụ thất bại"],
  ["videos_created", "Video đã tạo"],
];

export default function Overview() {
  const status = useSystemSocket();

  if (!status) return <p>Đang kết nối tới Orchestrator...</p>;

  return (
    <div>
      <h2>Tổng quan</h2>
      <div className="card-grid">
        {CARDS.map(([key, label]) => (
          <div className="card" key={key}>
            <div className="card-value">{status[key]}</div>
            <div className="card-label">{label}</div>
          </div>
        ))}
      </div>
      <p className="uptime">Thời gian hoạt động: {Math.round(status.uptime_seconds)} giây</p>
    </div>
  );
}
