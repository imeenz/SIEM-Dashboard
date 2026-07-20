import {
  Activity,
  Bell,
  LayoutDashboard,
  Radar,
  Shield,
} from "lucide-react"
import { NavLink } from "react-router-dom"

const navigation = [
  {
    name: "Dashboard",
    icon: LayoutDashboard,
    path: "/",
  },
  {
    name: "Alerts",
    icon: Bell,
    path: "/alerts",
  },
  {
    name: "Events",
    icon: Activity,
    path: "/events",
  },
  {
    name: "Detections",
    icon: Radar,
    path: "/detections",
  },
]
function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-icon">
          <Shield size={22} />
        </div>

        <div>
          <h1>SIEM</h1>
          <span>Security Operations</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <span className="nav-label">MONITORING</span>

        {navigation.map((item) => {
            const Icon = item.icon

            return (
            <NavLink
            key={item.name}
            to={item.path}
            end={item.path === "/"}
            className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
      }
            >
           <Icon size={18} />
           <span>{item.name}</span>
           </NavLink>
  )
})}
      </nav>

      <div className="sidebar-footer">
        <div className="system-status">
          <span className="status-dot" />

          <div>
            <strong>System Operational</strong>
            <span>All services online</span>
          </div>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar