import { useEffect, useState } from "react";

import { api } from "../api";

const LABELS = {
  orchestrator_host: "Host Orchestrator",
  orchestrator_port: "Cổng Orchestrator",
  mcp_port: "Cổng MCP",
  antigravity_cli_path: "Đường dẫn Antigravity CLI",
  muse4ai_base_url: "Muse4AI Base URL",
  muse4ai_api_key_set: "Muse4AI API key đã cấu hình?",
  max_concurrent_tasks: "Số task chạy song song tối đa",
  max_task_timeout_seconds: "Timeout tối đa cho 1 task (giây)",
  max_fix_retries: "Số lần thử lại tối đa",
  projects_dir: "Thư mục làm việc (projects)",
  output_dir: "Thư mục đầu ra (output)",
};

export default function Settings() {
  const [config, setConfig] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .getSystemConfig()
      .then(setConfig)
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div>
      <h2>Cài đặt</h2>
      <p className="hint">
        Đây là cấu hình hiện tại (chỉ xem). Secret (mật khẩu, API key, JWT secret) không bao giờ
        hiển thị ở đây — xem/sửa trực tiếp trong <code>config/.env</code> trên máy, sau đó khởi
        động lại dịch vụ bằng <code>scripts/restart.ps1</code> để áp dụng.
      </p>
      {error && <div className="error">{error}</div>}
      {config && (
        <table>
          <tbody>
            {Object.entries(config).map(([key, value]) => (
              <tr key={key}>
                <td>{LABELS[key] || key}</td>
                <td>{String(value)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
