import { useEffect, useState } from "react"

import RecentAlerts from "../components/dashboard/RecentAlerts"
import SeverityCards from "../components/dashboard/SeverityCards"
import SeverityDistribution from "../components/dashboard/SeverityDistribution"
import ThreatActivityChart from "../components/dashboard/ThreatActivityChart"
import { getAlerts } from "../services/alerts"
import type { Alert } from "../types/alert"
import { getEvents } from "../services/events"
import type { SecurityEvent } from "../types/event"

function Dashboard() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [events, setEvents] = useState<SecurityEvent[]>([])
  const [lastUpdated, setLastUpdated] = useState(new Date())

  useEffect(() => {
  async function loadDashboard() {
    try {
      const [alertsData, eventsData] = await Promise.all([
        getAlerts(),
        getEvents(),
      ])

      setAlerts(alertsData)
      setEvents(eventsData)
      setLastUpdated(new Date())
      setError(null)
    } catch {
      setError("Failed to load dashboard data")
    } finally {
      setLoading(false)
    }
  }

  loadDashboard()

  const refreshInterval = setInterval(() => {
    loadDashboard()
  }, 30000)

  return () => {
    clearInterval(refreshInterval)
  }
}, [])

  return (
    <>
      <div className="page-header">
         <div>
            <h1>Security Overview</h1>
            <p>
                Monitor threats, alerts, and security events.
            </p>
      </div>

      <div className="refresh-status">
        <span className="live-dot" />
      <div>
        <strong>Auto-refresh</strong>
        <span>
             Updated {lastUpdated.toLocaleTimeString()}
        </span>
      </div>
      </div>
      </div>

      {loading && (
        <p className="table-message">
          Loading dashboard...
        </p>
      )}

      {error && (
        <p className="table-message error">
          {error}
        </p>
      )}

      {!loading && !error && (
        <>
          <SeverityCards alerts={alerts} />

          <div className="dashboard-analytics">
            <ThreatActivityChart events={events} />
            <SeverityDistribution alerts={alerts} />
          </div>

          <RecentAlerts alerts={alerts} />
        </>
      )}
    </>
  )
}

export default Dashboard