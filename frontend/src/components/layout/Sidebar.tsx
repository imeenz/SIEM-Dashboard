import {
  Activity,
  Bell,
  LayoutDashboard,
  LogOut,
  Radar,
  Shield,
} from "lucide-react"
import { NavLink } from "react-router-dom"
import { removeToken } from "../../services/auth"
import type { CurrentUser } from "../../services/auth"

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
interface SidebarProps {
  user: CurrentUser | null
}
function Sidebar({ user }: SidebarProps) { 
  function handleLogout() {
    removeToken()
    window.location.href = "/login"
}
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
        <div className="analyst-profile">
          <div className="analyst-avatar">
             {user?.full_name.charAt(0).toUpperCase()}
             </div>
        
        <div className="analyst-info">
          <strong>{user?.full_name}</strong>
          <span>{user?.email}</span>
        </div>
      </div>
        <button
        type="button"
        className="logout-button"
        onClick={handleLogout}
        >
          <LogOut size={18} />
          <span>Sign Out</span>
        </button>

  
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