import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from "react-leaflet";
import L from "leaflet"; 
import "leaflet/dist/leaflet.css";
import styles from "./assets/css/LeafletMapComponent.module.css";

const userIcon = new L.Icon({
  iconUrl: "https://maps.google.com/mapfiles/ms/icons/red-dot.png",
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const sightingIcon = new L.Icon({
  iconUrl: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png",
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const ClickHandler = ({ setCoordinates }) => {
  useMapEvents({
    click(e) {
      setCoordinates({ lat: e.latlng.lat, lng: e.latlng.lng });
    },
  });
  return null;
};


const LeafletMapComponent = ({ coordinates, setCoordinates, searchResults }) => {
  const [markerPosition, setMarkerPosition] = useState(null);

  useEffect(() => {
    if (!coordinates || coordinates.lat === null || coordinates.lng === null) {
      setMarkerPosition(null); 
    }
  }, [coordinates]);
  

  return (
    <div className={styles.mapContainer}>
      <MapContainer center={[40.7128, -74.006]} zoom={10} className={styles.map}>
        <TileLayer
          url="https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}"
          subdomains={["mt0", "mt1", "mt2", "mt3"]}
        />

        <ClickHandler setCoordinates={(coords) => {
          setCoordinates(coords);
          setMarkerPosition(coords);
        }} />

        {markerPosition && (
          <Marker position={[markerPosition.lat, markerPosition.lng]} icon={userIcon}>
            <Popup><strong>User Selected Location</strong></Popup>
          </Marker>
        )}

        {searchResults &&
          searchResults.map((sighting, index) =>
            sighting.latitude && sighting.longitude ? (
              <Marker
                key={index}
                position={[sighting.latitude, sighting.longitude]}
                icon={sightingIcon}
              >
                <Popup>
                  <strong>City:</strong> {sighting.city} <br />
                  <strong>State:</strong> {sighting.state.toUpperCase()} <br />
                  <strong>Shape:</strong> {sighting.shape} <br />
                  <strong>Comments:</strong> {sighting.comments}
                </Popup>
              </Marker>
            ) : null
          )}
      </MapContainer>
    </div>
  );
};

export default LeafletMapComponent;