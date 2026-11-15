import { BrowserRouter, Navigate, NavLink, Outlet, Route, Routes } from "react-router-dom";

import { getToken, setToken } from "./api";
import AgentMonitor from "./pages/AgentMonitor";
import Login from "./pages/Login";
import Overview from "./pages/Overview";
import Settings from "./pages/Settings";
import SystemLogs from "./pages/SystemLogs";
import TaskManager from "./pages/TaskManager";
import VideoManager from "./pages/VideoManager";
import Workflow from "./pages/Workflow";

function RequireAuth() {
  if (!getToken()) return <Navigate to="/login" replace />;
  return <Outlet />;
}

function Layout() {
  function handleLogout() {
    setToken(null);
    window.location.href = "/login";
  }

  return (
    <div className="layout">
      <nav className="sidebar">
        <h1>AI Agent Orchestrator</h1>
        <NavLink to="/" end>
          Tổng quan
        </NavLink>
        <NavLink to="/agents">Giám sát Agent</NavLink>
        <NavLink to="/tasks">Quản lý nhiệm vụ</NavLink>
        <NavLink to="/workflows">Workflow</NavLink>
        <NavLink to="/videos">Quản lý video</NavLink>
        <NavLink to="/logs">Log hệ thống</NavLink>
        <NavLink to="/settings">Cài đặt</NavLink>
        <button className="logout" onClick={handleLogout}>
          Đăng xuất
        </button>
      </nav>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<RequireAuth />}>
          <Route element={<Layout />}>
            <Route path="/" element={<Overview />} />
            <Route path="/agents" element={<AgentMonitor />} />
            <Route path="/tasks" element={<TaskManager />} />
            <Route path="/workflows" element={<Workflow />} />
            <Route path="/workflows/:workflowId" element={<Workflow />} />
            <Route path="/videos" element={<VideoManager />} />
            <Route path="/logs" element={<SystemLogs />} />
            <Route path="/settings" element={<Settings />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
