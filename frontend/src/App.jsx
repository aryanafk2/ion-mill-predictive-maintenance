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

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/equipment/1/health/")
      .then((response) => {
        setHealth(response.data);
      })
      .catch((error) => {
        console.error(error);
      });

    axios
      .get("http://127.0.0.1:8000/api/equipment/1/readings/")
      .then((response) => {
        setReadings(response.data.reverse());
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

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
            border: "1px solid #ffffff50",
            borderRadius: "20px",
            padding: "30px",
            width: "500px",
            marginBottom: "50px",
          }}
        >
          <h2
            style={{
              textAlign: "center",
              fontSize: "3rem",
            }}
          >
            {health.tool_id}
          </h2>

          <p style={{ fontSize: "2rem" }}>
            <strong>Health:</strong>{" "}
            {health.health_score?.toFixed(2)}%
          </p>

          <p style={{ fontSize: "2rem" }}>
            <strong>Status:</strong>{" "}
            {health.is_anomaly
              ? "Anomaly Detected"
              : "Healthy"}
          </p>

          <p style={{ fontSize: "2rem" }}>
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
        }}
      >
        <h2
          style={{
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
    </div>
  );
}

export default App;