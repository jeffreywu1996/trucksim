import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard = ({ selectedTruck }) => {
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState({
    totalTrucks: 0,
    avgSpeed: 0,
    avgFuel: 0,
    totalMiles: 0
  });

  // Fetch historical data when a truck is selected
  useEffect(() => {
    if (selectedTruck) {
      fetch(`/api/trucks/${selectedTruck.id}/history?hours=1`)
        .then(res => res.json())
        .then(data => setHistory(data));
    }
  }, [selectedTruck]);

  // Calculate aggregate statistics
  useEffect(() => {
    fetch('/api/trucks')
      .then(res => res.json())
      .then(trucks => {
        const totalTrucks = trucks.length;
        const avgSpeed = trucks.reduce((acc, t) => acc + t.speed, 0) / totalTrucks;
        const avgFuel = trucks.reduce((acc, t) => acc + t.fuel_level, 0) / totalTrucks;
        const totalMiles = trucks.reduce((acc, t) => acc + t.miles_accumulated, 0);

        setStats({ totalTrucks, avgSpeed, avgFuel, totalMiles });
      });
  }, []);

  return (
    <div className="dashboard">
      <div className="dashboard-section">
        <h2>Fleet Statistics</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <div>Total Trucks</div>
            <div>{stats.totalTrucks}</div>
          </div>
          <div className="stat-card">
            <div>Avg Speed</div>
            <div>{stats.avgSpeed.toFixed(1)} mph</div>
          </div>
          <div className="stat-card">
            <div>Avg Fuel</div>
            <div>{stats.avgFuel.toFixed(1)}%</div>
          </div>
          <div className="stat-card">
            <div>Total Miles</div>
            <div>{stats.totalMiles.toFixed(1)} mi</div>
          </div>
        </div>
      </div>

      {selectedTruck && (
        <div className="dashboard-section">
          <h2>Truck {selectedTruck.id} History</h2>
          <div className="history-chart">
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={history}>
                <XAxis dataKey="timestamp" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="speed" stroke="#8884d8" />
                <Line type="monotone" dataKey="fuel_level" stroke="#82ca9d" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
