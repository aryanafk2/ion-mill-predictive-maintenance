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

function App() {
  const [health, setHealth] = useState(null);
  const [readings, setReadings] = useState([]);
  const [alerts, setAlerts] = useState([]);

  const fetchData = () => {
    axios
      .get("http://127.0.0.1:8000/api/equipment/1/health/")
      .then((response) => {
        setHealth(response.data);
      })
      .catch((error) => console.error(error));

    axios
      .get("http://127.0.0.1:8000/api/equipment/1/readings/")
      .then((response) => {
        setReadings(response.data.reverse());
      })
      .catch((error) => console.error(error));

    axios
      .get("http://127.0.0.1:8000/api/alerts/")
      .then((response) => {
        setAlerts(response.data);
      })
      .catch((error) => console.error(error));
  };

  useEffect(() => {
    fetchData();

    const interval = setInterval(() => {
      fetchData();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const healthColor =
    health?.health_score > 80
      ? "#22c55e"
      : health?.health_score > 60
      ? "#eab308"
      : "#ef4444";

  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#0f172a",
        color: "white",
        padding: "40px",
      }}
    >
      <h1
        style={{
          textAlign: "center",
          fontSize: "4rem",
          marginBottom: "40px",
        }}
      >
        PHM Dashboard
      </h1>

      {health && (
        <div
          style={{
            border: "1px solid #ffffff40",
            borderRadius: "20px",
            padding: "25px",
            width: "450px",
            marginBottom: "40px",
            backgroundColor: "#111827",
          }}
        >
          <h2
            style={{
              textAlign: "center",
              fontSize: "2rem",
              marginBottom: "20px",
            }}
          >
            {health.tool_id}
          </h2>

          <p style={{ fontSize: "1.3rem" }}>
            <strong>Health:</strong>{" "}
            <span
              style={{
                color: healthColor,
                fontWeight: "bold",
              }}
            >
              {health.health_score?.toFixed(2)}%
            </span>
          </p>

          <p style={{ fontSize: "1.3rem" }}>
            <strong>Status:</strong>{" "}
            <span
              style={{
                color: health.is_anomaly
                  ? "#ef4444"
                  : "#22c55e",
                fontWeight: "bold",
              }}
            >
              {health.is_anomaly
                ? "Anomaly Detected"
                : "Healthy"}
            </span>
          </p>

          <p style={{ fontSize: "1.3rem" }}>
            <strong>Timestamp:</strong>{" "}
            {health.timestamp}
          </p>
        </div>
      )}

      <div
        style={{
          backgroundColor: "#1e293b",
          padding: "20px",
          borderRadius: "20px",
          height: "450px",
          marginBottom: "30px",
        }}
      >
        <h2
          style={{
            textAlign: "center",
            marginBottom: "20px",
          }}
        >
          Health Trend
        </h2>

        <ResponsiveContainer width="100%" height="90%">
          <LineChart data={readings}>
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="timestamp" />

            <YAxis domain={[0, 100]} />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="health_score"
              stroke="#22c55e"
              strokeWidth={3}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div
        style={{
          backgroundColor: "#1e293b",
          padding: "20px",
          borderRadius: "20px",
        }}
      >
        <h2
          style={{
            textAlign: "center",
            marginBottom: "20px",
          }}
        >
          Alerts
        </h2>

        {alerts.length === 0 ? (
          <p
            style={{
              textAlign: "center",
            }}
          >
            No active alerts
          </p>
        ) : (
          alerts.map((alert, index) => (
            <div
              key={index}
              style={{
                marginBottom: "12px",
                padding: "15px",
                border: "1px solid #ef4444",
                borderRadius: "10px",
                backgroundColor: "#111827",
              }}
            >
              <strong>{alert.message}</strong>

              <br />

              Health Score: {alert.health_score}

              <br />

              Timestamp: {alert.timestamp}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;