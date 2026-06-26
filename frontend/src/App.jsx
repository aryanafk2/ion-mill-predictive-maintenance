import { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import "./App.css";

// ---------------------------------------------------------------------------
// Status helpers
// ---------------------------------------------------------------------------

function getStatus(score, isAnomaly) {
  if (isAnomaly) return "critical";
  if (score == null) return "unknown";
  if (score > 80) return "healthy";
  if (score > 60) return "warning";
  return "critical";
}

const STATUS_LABEL = {
  healthy: "Healthy",
  warning: "Warning",
  critical: "Critical",
  unknown: "Unknown",
};

function formatTimestamp(value) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleString([], {
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatTick(value) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

// ---------------------------------------------------------------------------
// Presentational components (UI only — no data fetching, no business logic)
// ---------------------------------------------------------------------------

function StatusBadge({ status }) {
  return (
    <span className={`status-badge status-badge--${status}`}>
      <span className="status-dot" />
      {STATUS_LABEL[status] ?? "Unknown"}
    </span>
  );
}

function HealthGauge({ score, status, size = 96 }) {
  const stroke = 8;
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const pct = Math.max(0, Math.min(100, score ?? 0));
  const offset = circumference - (pct / 100) * circumference;

  return (
    <div className="gauge" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle
          className="gauge__track"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={stroke}
        />
        <circle
          className={`gauge__progress gauge__progress--${status}`}
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={stroke}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
      </svg>
      <div className="gauge__readout">
        <span className="gauge__value">
          {score != null ? score.toFixed(0) : "—"}
        </span>
        <span className="gauge__unit">%</span>
      </div>
    </div>
  );
}

function KpiCard({ label, value, unit, status = "neutral" }) {
  return (
    <div className={`kpi-card kpi-card--${status}`}>
      <span className="kpi-card__label">{label}</span>
      <span className="kpi-card__value">
        {value}
        {unit ? <span className="kpi-card__unit">{unit}</span> : null}
      </span>
    </div>
  );
}

function EquipmentCard({ tool, isSelected, onSelect }) {
  const status = getStatus(tool.health_score, tool.is_anomaly);

  return (
    <button
      type="button"
      className={[
        "equipment-card",
        `equipment-card--${status}`,
        isSelected ? "equipment-card--selected" : "",
      ].join(" ")}
      onClick={onSelect}
    >
      <div className="equipment-card__header">
        <span className="equipment-card__id">{tool.tool_id}</span>
        <StatusBadge status={status} />
      </div>

      <div className="equipment-card__body">
        <HealthGauge score={tool.health_score} status={status} size={72} />

        <dl className="equipment-card__stats">
          <div>
            <dt>Health</dt>
            <dd>
              {tool.health_score != null
                ? `${tool.health_score.toFixed(1)}%`
                : "—"}
            </dd>
          </div>
          <div>
            <dt>Predicted TTF</dt>
            <dd>
              {tool.predicted_ttf != null
                ? tool.predicted_ttf.toFixed(0)
                : "—"}
            </dd>
          </div>
        </dl>
      </div>
    </button>
  );
}

function AlertRow({ alert }) {
  return (
    <div className="alert-item">
      <span className="alert-item__icon" aria-hidden="true">
        ▲
      </span>
      <div className="alert-item__content">
        <p className="alert-item__message">{alert.message}</p>
        <div className="alert-item__meta">
          <span>Health Score: {alert.health_score}</span>
          <span className="alert-item__dot" aria-hidden="true" />
          <span>{formatTimestamp(alert.timestamp)}</span>
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// App — data fetching, polling, and state are unchanged from the original
// ---------------------------------------------------------------------------

function App() {
  const [equipmentList, setEquipmentList] = useState([]);
  const [selectedEquipment, setSelectedEquipment] = useState(null);

  const [health, setHealth] = useState(null);
  const [readings, setReadings] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [fleetHealth, setFleetHealth] = useState([]);

  const fetchEquipment = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/api/equipment/"
      );

      setEquipmentList(response.data);

      if (
        response.data.length > 0 &&
        selectedEquipment === null
      ) {
        setSelectedEquipment(response.data[0].id);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const fetchData = async () => {
    if (!selectedEquipment) return;

    try {
      const healthResponse = await axios.get(
        `http://127.0.0.1:8000/api/equipment/${selectedEquipment}/health/`
      );

      setHealth(healthResponse.data);

      const readingsResponse = await axios.get(
        `http://127.0.0.1:8000/api/equipment/${selectedEquipment}/readings/`
      );

      setReadings(readingsResponse.data.reverse());

      const alertsResponse = await axios.get(
        "http://127.0.0.1:8000/api/alerts/"
      );
      const fleetResponse = await axios.get(
        "http://127.0.0.1:8000/api/fleet-health/"
      );

      setFleetHealth(fleetResponse.data);
      setAlerts(alertsResponse.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchEquipment();
  }, []);

  useEffect(() => {
    if (!selectedEquipment) return;

    fetchData();

    const interval = setInterval(() => {
      fetchData();
    }, 2000);

    return () => clearInterval(interval);
  }, [selectedEquipment]);

  // ---- derived display-only values (no effect on fetching/state shape) ----
  const selectedStatus = getStatus(health?.health_score, health?.is_anomaly);

  const totalTools = equipmentList.length;
  const avgHealth =
    fleetHealth.length > 0
      ? fleetHealth.reduce((sum, t) => sum + (t.health_score ?? 0), 0) /
        fleetHealth.length
      : null;
  const criticalCount = fleetHealth.filter(
    (t) => getStatus(t.health_score, t.is_anomaly) === "critical"
  ).length;

  return (
    <div className="dashboard">
      <header className="topbar">
        <div className="topbar__brand">
          <span className="topbar__eyebrow">Predictive Maintenance</span>
          <h1 className="topbar__title">PHM Console</h1>
        </div>

        <div className="topbar__controls">
          <span className="live-pill">
            <span className="live-dot" />
            Live
          </span>

          <div className="select-group">
            <label className="select-label" htmlFor="equipment-select">
              Tool
            </label>
            <select
              id="equipment-select"
              className="equipment-select"
              value={selectedEquipment || ""}
              onChange={(e) =>
                setSelectedEquipment(Number(e.target.value))
              }
            >
              {equipmentList.map((eq) => (
                <option key={eq.id} value={eq.id}>
                  {eq.tool_id}
                </option>
              ))}
            </select>
          </div>
        </div>
      </header>

      <main className="dashboard__main">
        <section className="kpi-grid" aria-label="Fleet summary">
          <KpiCard label="Total Tools" value={totalTools} status="info" />
          <KpiCard
            label="Avg Fleet Health"
            value={avgHealth != null ? avgHealth.toFixed(1) : "—"}
            unit={avgHealth != null ? "%" : ""}
            status={
              avgHealth == null
                ? "neutral"
                : avgHealth > 80
                ? "healthy"
                : avgHealth > 60
                ? "warning"
                : "critical"
            }
          />
          <KpiCard
            label="Active Alerts"
            value={alerts.length}
            status={alerts.length > 0 ? "critical" : "healthy"}
          />
          <KpiCard
            label="Critical Equipment"
            value={criticalCount}
            status={criticalCount > 0 ? "critical" : "healthy"}
          />
        </section>

        <section className="panel fleet-panel">
          <div className="panel__header">
            <h2>Fleet Overview</h2>
            <span className="panel__meta">
              {fleetHealth.length} tool{fleetHealth.length === 1 ? "" : "s"}{" "}
              monitored
            </span>
          </div>

          {fleetHealth.length === 0 ? (
            <p className="empty-state">No fleet data available yet.</p>
          ) : (
            <div className="equipment-grid">
              {fleetHealth.map((tool) => {
                const match = equipmentList.find(
                  (eq) => eq.tool_id === tool.tool_id
                );
                return (
                  <EquipmentCard
                    key={tool.tool_id}
                    tool={tool}
                    isSelected={
                      match ? match.id === selectedEquipment : false
                    }
                    onSelect={() => match && setSelectedEquipment(match.id)}
                  />
                );
              })}
            </div>
          )}
        </section>

        <section className="detail-grid">
          <div className="panel detail-panel">
            <div className="panel__header">
              <h2>Selected Tool</h2>
              {health && <StatusBadge status={selectedStatus} />}
            </div>

            {health ? (
              <div className="detail-readout">
                <div className="detail-readout__hero">
                  <HealthGauge
                    score={health.health_score}
                    status={selectedStatus}
                    size={120}
                  />
                  <div className="detail-readout__id-block">
                    <span className="detail-readout__id">
                      {health.tool_id}
                    </span>
                    <span className="detail-readout__caption">
                      {STATUS_LABEL[selectedStatus]}
                      {health.is_anomaly ? " · Anomaly detected" : ""}
                    </span>
                  </div>
                </div>

                <div className="detail-readout__row">
                  <span className="detail-readout__label">
                    Predicted TTF
                  </span>
                  <span className="detail-readout__value">
                    {health.predicted_ttf != null
                      ? health.predicted_ttf.toFixed(0)
                      : "N/A"}
                  </span>
                </div>

                <div className="detail-readout__row">
                  <span className="detail-readout__label">
                    Last reading
                  </span>
                  <span className="detail-readout__value detail-readout__value--mono">
                    {formatTimestamp(health.timestamp)}
                  </span>
                </div>
              </div>
            ) : (
              <p className="empty-state">Select a tool to view details.</p>
            )}
          </div>

          <div className="panel trend-panel">
            <div className="panel__header">
              <h2>Health Trend</h2>
            </div>

            <div className="chart-wrap">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={readings}>
                  <CartesianGrid
                    stroke="#1f2937"
                    strokeDasharray="3 3"
                    vertical={false}
                  />
                  <XAxis
                    dataKey="timestamp"
                    stroke="#5b6779"
                    tick={{ fill: "#8b98a8", fontSize: 11 }}
                    tickFormatter={formatTick}
                    axisLine={{ stroke: "#1f2937" }}
                    tickLine={false}
                  />
                  <YAxis
                    domain={[0, 100]}
                    stroke="#5b6779"
                    tick={{ fill: "#8b98a8", fontSize: 11 }}
                    axisLine={{ stroke: "#1f2937" }}
                    tickLine={false}
                  />
                  <Tooltip
                    contentStyle={{
                      background: "#111827",
                      border: "1px solid #1f2937",
                      borderRadius: 8,
                      fontSize: 12,
                    }}
                    labelStyle={{ color: "#8b98a8" }}
                    labelFormatter={formatTimestamp}
                    itemStyle={{ color: "#34d8c8" }}
                  />
                  <Line
                    type="monotone"
                    dataKey="health_score"
                    stroke="#34d8c8"
                    strokeWidth={2.5}
                    dot={false}
                    activeDot={{ r: 4, fill: "#34d8c8" }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </section>

        <section className="panel alerts-panel">
          <div className="panel__header">
            <h2>Alerts</h2>
            <span className="panel__meta">{alerts.length} active</span>
          </div>

          {alerts.length === 0 ? (
            <p className="empty-state">No active alerts</p>
          ) : (
            <div className="alerts-list">
              {alerts.map((alert, index) => (
                <AlertRow key={index} alert={alert} />
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;