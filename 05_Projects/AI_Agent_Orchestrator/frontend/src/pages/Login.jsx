import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { api, setToken } from "../api";

export default function Login() {
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const { access_token: accessToken } = await api.login(password);
      setToken(accessToken);
      navigate("/", { replace: true });
    } catch {
      setError("Sai mật khẩu, hoặc máy chủ chưa cấu hình đăng nhập (xem config/.env).");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="login-screen">
      <form className="login-card" onSubmit={handleSubmit}>
        <h1>AI Agent Orchestrator</h1>
        <p>Nhập mật khẩu để truy cập Dashboard</p>
        <input
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="Mật khẩu"
          autoFocus
        />
        {error && <div className="error">{error}</div>}
        <button type="submit" disabled={submitting}>
          {submitting ? "Đang đăng nhập..." : "Đăng nhập"}
        </button>
      </form>
    </div>
  );
}
