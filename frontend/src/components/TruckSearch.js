import React from 'react';

const TruckSearch = ({ onSearch }) => {
  return (
    <input
      type="text"
      className="search-box"
      placeholder="Search trucks..."
      onChange={(e) => onSearch(e.target.value)}
    />
  );
};

export default TruckSearch;
