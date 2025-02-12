import React, { useEffect, useState } from 'react';
import Map, { Marker, Popup } from 'react-map-gl';
import TruckPopup from './TruckPopup';
import 'mapbox-gl/dist/mapbox-gl.css';
import truckIcon from '../assets/truck-icon.svg';

const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN;
const WEBSOCKET_URL = process.env.REACT_APP_BACKEND_URL || 'ws://localhost:8000/ws';

const TruckMap = ({ selectedTruck, onTruckSelect, searchQuery }) => {
  const [trucks, setTrucks] = useState([]);
  const [viewState, setViewState] = useState({
    latitude: 40.7128,
    longitude: -74.0060,
    zoom: 11
  });

  // WebSocket connection
  useEffect(() => {
    console.log('Connecting to WebSocket at:', WEBSOCKET_URL);
    const ws = new WebSocket(WEBSOCKET_URL);

    ws.onopen = () => {
      console.log('WebSocket Connected');
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('Received WebSocket data:', data);
        if (data.type === 'trucks_update') {
          setTrucks(data.data);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };

    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, []);

  // Filter trucks based on search query
  const filteredTrucks = trucks.filter(truck =>
    truck.id.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="map-container" style={{ height: '100vh', width: '100%' }}>
      <Map
        {...viewState}
        onMove={evt => setViewState(evt.viewState)}
        style={{ width: '100%', height: '100%' }}
        mapStyle="mapbox://styles/mapbox/streets-v11"
        mapboxAccessToken={MAPBOX_TOKEN}
      >
        {filteredTrucks.map((truck) => (
          <Marker
            key={truck.id}
            latitude={truck.latitude}
            longitude={truck.longitude}
            onClick={(e) => {
              e.originalEvent.stopPropagation();
              onTruckSelect(truck);
            }}
          >
            <div
              className={`truck-marker ${selectedTruck?.id === truck.id ? 'active' : ''}`}
              style={{
                width: '20px',
                height: '20px',
                backgroundImage: `url(${truckIcon})`,
                backgroundSize: 'cover',
                cursor: 'pointer',
                filter: truck.engine_status === 'running' ? 'hue-rotate(120deg)' : 'hue-rotate(0deg)'
              }}
            />
          </Marker>
        ))}

        {selectedTruck && (
          <Popup
            latitude={selectedTruck.latitude}
            longitude={selectedTruck.longitude}
            onClose={() => onTruckSelect(null)}
            closeButton={true}
            closeOnClick={false}
            anchor="bottom"
          >
            <TruckPopup truck={selectedTruck} />
          </Popup>
        )}
      </Map>
    </div>
  );
};

export default TruckMap;
