// src/Dashboard.js
import React, { useEffect, useState } from "react";

const Dashboard = () => {
  const [data, setData] = useState({
    current_EAR: 0,
    current_MAR: 0,
    cnn_drowsiness_score: 0,
    final_status: "Awake",
    drowsiness_alert: false,
    yawning_alert: false,
  });
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5000/drowsiness_data");
        const result = await response.json();
        setData(result);

        // If final status indicates drowsiness, add an alert log
        if (result.final_status === "Drowsy") {
          setAlerts((prev) => [
            { id: Date.now(), message: "Drowsiness detected! Wake up!" },
            ...prev,
          ]);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    const interval = setInterval(fetchData, 1000); // Fetch every second
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>REAL TIME DROWSINESS DETECTOR</h1>
      </header>
      <section className="status-section">
        <h2>System Status: {data.final_status}</h2>
        {data.drowsiness_alert && <p className="alert-text">Drowsiness Alert!</p>}
        {data.yawning_alert && <p className="alert-text">Yawning Alert!</p>}
      </section>
      <section className="data-section">
        <p><strong>EAR:</strong> {data.current_EAR.toFixed(2)}</p>
        <p><strong>MAR:</strong> {data.current_MAR.toFixed(2)}</p>
        <p><strong>CNN Score:</strong> {data.cnn_drowsiness_score.toFixed(2)}</p>
      </section>
      <section className="alert-log">
        <h3>Alert Log</h3>
        {alerts.length === 0 ? (
          <p>No alerts yet.</p>
        ) : (
          <ul>
            {alerts.map((alert) => (
              <li key={alert.id}>{alert.message}</li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
};

export default Dashboard;
