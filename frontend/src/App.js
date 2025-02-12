import React, { useState, useEffect } from 'react';
import TruckMap from './components/Map';
import Dashboard from './components/Dashboard';
import TruckSearch from './components/TruckSearch';
import FleetStats from './components/FleetStats';
import './App.css';

function App() {
  const [selectedTruck, setSelectedTruck] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [trucks, setTrucks] = useState([]);

  // WebSocket connection and data handling
  useEffect(() => {
    const ws = new WebSocket(process.env.REACT_APP_BACKEND_URL || 'ws://localhost:8000/ws');

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'trucks_update') {
          setTrucks(data.data);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, []);

  return (
    <div className="App">
      <div className="sidebar">
        <TruckSearch onSearch={setSearchQuery} />
        <FleetStats trucks={trucks} />
      </div>
      <div className="main-content">
        <TruckMap
          selectedTruck={selectedTruck}
          onTruckSelect={setSelectedTruck}
          searchQuery={searchQuery}
          trucks={trucks}
        />
      </div>
    </div>
  );
}

export default App;
