import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/equipment/1/health/")
      .then((response) => {
        setHealth(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div style={{ padding: "30px" }}>
      <h1>PHM Dashboard</h1>

      {health ? (
        <div
          style={{
            border: "1px solid #ccc",
            padding: "20px",
            width: "300px",
            borderRadius: "10px",
          }}
        >
          <h2>{health.tool_id}</h2>

          <p>
            <strong>Health:</strong>{" "}
            {health.health_score?.toFixed(2)}%
          </p>

          <p>
            <strong>Status:</strong>{" "}
            {health.is_anomaly ? "Anomaly Detected" : "Healthy"}
          </p>

          <p>
            <strong>Timestamp:</strong>{" "}
            {health.timestamp}
          </p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;