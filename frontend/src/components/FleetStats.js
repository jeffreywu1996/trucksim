import React from 'react';

const FleetStats = ({ trucks }) => {
  // Calculate statistics from trucks data
  const totalTrucks = trucks.length;

  const avgSpeed = totalTrucks > 0
    ? trucks.reduce((sum, truck) => sum + truck.speed, 0) / totalTrucks
    : 0;

  const avgFuel = totalTrucks > 0
    ? trucks.reduce((sum, truck) => sum + truck.fuel_level, 0) / totalTrucks
    : 0;

  const totalMiles = trucks.reduce((sum, truck) => sum + truck.miles_accumulated, 0);

  return (
    <div className="fleet-stats">
      <h2>Fleet Statistics</h2>
      <div className="stats-grid">
        <div className="stat-item">
          <h3>Total Trucks</h3>
          <p>{totalTrucks}</p>
        </div>
        <div className="stat-item">
          <h3>Avg Speed</h3>
          <p>{avgSpeed.toFixed(1)} mph</p>
        </div>
        <div className="stat-item">
          <h3>Avg Fuel</h3>
          <p>{avgFuel.toFixed(1)}%</p>
        </div>
        <div className="stat-item">
          <h3>Total Miles</h3>
          <p>{totalMiles.toFixed(1)} mi</p>
        </div>
      </div>
    </div>
  );
};

export default FleetStats;
