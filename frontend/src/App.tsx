import { Navigate, Route, Routes } from "react-router-dom"

import Sidebar from "./components/layout/Sidebar"
import { useAuth } from "./hooks/useAuth"
import Alerts from "./pages/Alerts"
import Dashboard from "./pages/Dashboard"
import Detections from "./pages/Detections"
import Events from "./pages/Events"
import Login from "./pages/LoginPage"


function ProtectedApp() {
  const {
    user,
    loading,
    isAuthenticated,
  } = useAuth()

  if (loading) {
    return (
      <div className="auth-loading">
        Verifying session...
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return (
    <div className="app-shell">
      <Sidebar user={user} />

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/alerts" element={<Alerts />} />
          <Route path="/events" element={<Events />} />
          <Route path="/detections" element={<Detections />} />
        </Routes>
      </main>
    </div>
  )
}


function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/*" element={<ProtectedApp />} />
    </Routes>
  )
}

export default App