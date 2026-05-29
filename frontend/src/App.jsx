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
    }, 5000);

    return () => clearInterval(interval);
  }, [selectedEquipment]);

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
          fontSize: "3rem",
          marginBottom: "30px",
        }}
      >
        PHM Dashboard
      </h1>

      <div
        style={{
          marginBottom: "30px",
          textAlign: "center",
        }}
      >
        <label
          style={{
            fontSize: "1.2rem",
            marginRight: "10px",
          }}
        >
          Select Tool:
        </label>

        <select
          value={selectedEquipment || ""}
          onChange={(e) =>
            setSelectedEquipment(
              Number(e.target.value)
            )
          }
          style={{
            padding: "10px",
            borderRadius: "8px",
            fontSize: "1rem",
          }}
        >
          {equipmentList.map((eq) => (
            <option
              key={eq.id}
              value={eq.id}
            >
              {eq.tool_id}
            </option>
          ))}
        </select>
      </div>
        {/* ================= FLEET OVERVIEW ================= */}

<div
  style={{
    backgroundColor: "#1e293b",
    padding: "20px",
    borderRadius: "20px",
    marginBottom: "30px",
  }}
>
  <h2
    style={{
      textAlign: "center",
      marginBottom: "20px",
    }}
  >
    Fleet Overview
  </h2>

  <div
    style={{
      display: "grid",
      gridTemplateColumns:
        "repeat(auto-fit, minmax(220px, 1fr))",
      gap: "15px",
    }}
  >
    {fleetHealth.map((tool) => {

      const color =
        tool.health_score > 80
          ? "#22c55e"
          : tool.health_score > 60
          ? "#eab308"
          : "#ef4444";

      return (
                <div
                  key={tool.tool_id}
                  style={{
                    backgroundColor: "#111827",
                    padding: "15px",
                    borderRadius: "10px",
                    border: `2px solid ${color}`,
                  }}
                >
                  <h3>{tool.tool_id}</h3>

                  <p>
                    Health:{" "}
                    <span
                      style={{
                        color,
                        fontWeight: "bold",
                      }}
                    >
                      {tool.health_score.toFixed(2)}%
                    </span>
                  </p>

                  <p>
                    Status:{" "}
                    {tool.is_anomaly
                      ? "Anomaly"
                      : "Healthy"}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
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