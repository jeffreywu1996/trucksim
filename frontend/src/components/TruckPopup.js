import React from 'react';

const formatDuration = (seconds) => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  return `${hours}h ${minutes}m`;
};

const TruckPopup = ({ truck }) => {
  return (
    <div className="truck-popup">
      <h3>Truck {truck.id}</h3>
      <div className="truck-popup-content">
        <span className="truck-popup-label">Speed:</span>
        <span>{truck.speed.toFixed(1)} mph</span>

        <span className="truck-popup-label">Fuel Level:</span>
        <span>{truck.fuel_level.toFixed(1)}%</span>

        <span className="truck-popup-label">Engine Status:</span>
        <span>{truck.engine_status}</span>

        <span className="truck-popup-label">Running Time:</span>
        <span>{formatDuration(truck.running_time)}</span>

        <span className="truck-popup-label">Miles:</span>
        <span>{truck.miles_accumulated.toFixed(1)} mi</span>
      </div>
    </div>
  );
};

export default TruckPopup;
