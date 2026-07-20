import { useEffect, useState } from "react"
import { Search } from "lucide-react"

import {
  getAlerts,
  updateAlertStatus,
} from "../services/alerts"
import type { Alert } from "../types/alert"

function Alerts() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [severity, setSeverity] = useState("")
  const [status, setStatus] = useState("")
  const [search, setSearch] = useState("")

  useEffect(() => {
    async function loadAlerts() {
      setLoading(true)
      setError(null)

      try {
        const data = await getAlerts({
          severity: severity || undefined,
          status: status || undefined,
        })

        setAlerts(data)
      } catch {
        setError("Failed to load alerts")
      } finally {
        setLoading(false)
      }
    }

    loadAlerts()
  }, [severity, status])

  async function handleStatusChange(
    alertId: number,
    newStatus: string,
  ) {
    try {
      const updatedAlert = await updateAlertStatus(
        alertId,
        newStatus,
      )

      setAlerts((currentAlerts) =>
        currentAlerts.map((alert) =>
          alert.id === alertId ? updatedAlert : alert,
        ),
      )
    } catch {
      setError("Failed to update alert status")
    }
  }

  const filteredAlerts = alerts.filter((alert) =>
    alert.title
      .toLowerCase()
      .includes(search.toLowerCase()),
  )

  return (
    <>
      <div className="page-header">
        <div>
          <h1>Alerts</h1>
          <p>
            Investigate and manage active security alerts.
          </p>
        </div>
      </div>

      <section className="dashboard-panel alerts-page-panel">
        <div className="alerts-toolbar">
          <div className="search-box">
            <Search size={16} />

            <input
              type="text"
              placeholder="Search alerts..."
              value={search}
              onChange={(event) =>
                setSearch(event.target.value)
              }
            />
          </div>

          <div className="alert-filters">
            <select
              value={severity}
              onChange={(event) =>
                setSeverity(event.target.value)
              }
            >
              <option value="">All Severities</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>

            <select
              value={status}
              onChange={(event) =>
                setStatus(event.target.value)
              }
            >
              <option value="">All Statuses</option>
              <option value="open">Open</option>
              <option value="investigating">
                Investigating
              </option>
              <option value="resolved">
                Resolved
              </option>
            </select>
          </div>
        </div>

        {loading && (
          <p className="table-message">
            Loading alerts...
          </p>
        )}

        {error && (
          <p className="table-message error">
            {error}
          </p>
        )}

        {!loading && !error && (
          <div className="alerts-table-wrapper">
            <table className="alerts-table">
              <thead>
                <tr>
                  <th>Alert</th>
                  <th>Severity</th>
                  <th>Status</th>
                  <th>Time</th>
                </tr>
              </thead>

              <tbody>
                {filteredAlerts.map((alert) => (
                  <tr key={alert.id}>
                    <td className="alert-title">
                      {alert.title}
                    </td>

                    <td>
                      <span
                        className={`severity-badge ${alert.severity}`}
                      >
                        {alert.severity}
                      </span>
                    </td>

                    <td>
                      <select
                        className={`status-select ${alert.status}`}
                        value={alert.status}
                        onChange={(event) =>
                          handleStatusChange(
                            alert.id,
                            event.target.value,
                          )
                        }
                      >
                        <option value="open">
                          Open
                        </option>
                        <option value="investigating">
                          Investigating
                        </option>
                        <option value="resolved">
                          Resolved
                        </option>
                      </select>
                    </td>

                    <td className="alert-time">
                      {new Date(
                        alert.created_at,
                      ).toLocaleString()}
                    </td>
                  </tr>
                ))}

                {filteredAlerts.length === 0 && (
                  <tr>
                    <td
                      colSpan={4}
                      className="table-message"
                    >
                      No alerts found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </>
  )
}

export default Alerts