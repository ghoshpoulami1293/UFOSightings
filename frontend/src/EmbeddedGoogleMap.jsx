import React from "react";
import styles from "./assets/css/EmbeddedGoogleMap.module.css"; 
const EmbeddedGoogleMap = ({ coordinates }) => {
  if (!coordinates) return <p className={styles.errorText}>Location data not available</p>;

  const { lat, lng } = coordinates;
  const googleMapsUrl = `https://www.google.com/maps?q=${lat},${lng}&output=embed`;

  return (
    <div className={styles.container}>      
        <iframe          
          className={styles.mapFrame}
          title="Google Maps Location"
          loading="lazy"
          allowFullScreen
          referrerPolicy="no-referrer-when-downgrade"
          src={googleMapsUrl}
        />
      </div>   
 
  );
};

export default EmbeddedGoogleMap;
