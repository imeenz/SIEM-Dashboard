import { Route, Routes } from "react-router-dom"

import Sidebar from "./components/layout/Sidebar"
import Alerts from "./pages/Alerts"
import Dashboard from "./pages/Dashboard"
import Detections from "./pages/Detections"
import Events from "./pages/Events"

function App() {
  return (
    <div className="app-shell">
      <Sidebar />

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

export default App