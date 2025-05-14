import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import EmbeddedGoogleMap from "./EmbeddedGoogleMap";  
import styles from "./assets/css/UFO_Sighting_Details.module.css";
import { useNavigate } from "react-router-dom";
import BASE_URL from './config';

const UFO_Sighting_Details = () => {
  const { id } = useParams();
  const [sighting, setSighting] = useState(null);
  const [loading, setLoading] = useState(true);
  const [newComment, setNewComment] = useState("");
  const [userComments, setUserComments] = useState([]);
  const [coordinates, setCoordinates] = useState(null);

  useEffect(() => {
    console.log("Fetching sighting details for ID:", id);

    const fetchSighting = async () => {
      try {
        const response = await fetch(`${BASE_URL}/sighting/${id}`);
        if (!response.ok) {
          throw new Error(`Failed to fetch sighting: ${response.status}`);
        }

        const data = await response.json();
        console.log("Sighting details received:", data);

        setSighting(data);
        setUserComments(data.user_comments || []);

        if (data.image) {
          console.log("Base64 Image Data (First 100 chars):", data.image.substring(0, 100));
        }

        if (data.ufo_image) {
          console.log("Base64 Image Data (First 100 chars):", data.ufo_image.substring(0, 100));
        }
  

        if (data.latitude && data.longitude) {
          console.log("Setting Coordinates:", data.latitude, data.longitude);
          setCoordinates({ lat: data.latitude, lng: data.longitude });
        } else {
          console.warn("Missing latitude and longitude in API response!");
        }
      } catch (error) {
        console.error("Error fetching sighting:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSighting();
  }, [id]);

  const handleAddComment = async () => {
    if (!newComment.trim()) return;

    try {
      const response = await fetch(`${BASE_URL}/sighting/${id}/comment`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ comment: newComment }),
      });

      if (!response.ok) throw new Error("Failed to add comment");

      setUserComments([...userComments, newComment]); // Update UI
      setNewComment(""); // Clear input box
    } catch (error) {
      console.error(" Error adding comment:", error);
    }
  };

    // Go back to previous page
    const navigate = useNavigate();
    const handleBack = () => {
      navigate(-1); 
    };

  // Decoding the images
  const base64Image = sighting?.image?`data:image/jpeg;base64,${sighting.image}`: null;
  console.log("Base64 Image Data:", base64Image);

  const base64UfoImage = sighting?.ufo_image?`data:image/jpeg;base64,${sighting.ufo_image}`: null;
  console.log("Base64 UFO Image Data:", base64UfoImage);

  return (
    <div className={styles.container}>
      <button onClick={handleBack} className={styles.backButton}>⬅ Back</button>
      <h1 className={styles.header}>🚀👽 UFO Sighting Details</h1>

      {loading && <p className={styles.loadingText}>Loading...</p>}
      {!loading && !sighting && <p className={styles.errorText}>Sighting Not Found</p>}

      {sighting && (
        <div className={styles.detailsWrapper}>

          {/* Left Side: Image (if available) + Map */}
          <div className={styles.leftSide}>            
            {/* If both images are available, show them side by side */}
            {(base64Image || base64UfoImage) && (
              <div className={styles.imageRow}>
                {base64Image && (
                  <div className={styles.sightingImageContainer}>
                    <img
                      src={base64Image}
                      className={styles.sightingImage}
                      alt="Sighting"
                    />
                  </div>
                )}
                {base64UfoImage && (
                  <div className={styles.sightingImageContainer}>
                    <img
                      src={base64UfoImage}
                      className={styles.sightingImage}
                      alt="UFO"
                    />
                  </div>
                )}
              </div>
            )}
            {/* Map - Full Height if No Image, Half Height Otherwise */}
            <div className={`${styles.mapContainer} ${!sighting.image ? styles.fullHeight : ""}`}>
              <EmbeddedGoogleMap coordinates={coordinates} />
            </div>
        </div>
        
        {/*  Right Side: Details & Comments */}
          <div className={styles.rightSide}>
            <div className={styles.infoSection}>
              <div className={styles.stateCity}>
                <p><strong>State: </strong> {sighting.state ? sighting.state.toUpperCase() : "N/A"}</p>
                <p><strong>City: </strong> {sighting.city ? sighting.city.charAt(0).toUpperCase() + sighting.city.slice(1).toLowerCase() : "Unknown"}</p>
                <p><strong>Shape of UFO: </strong> {sighting.shape ? sighting.shape.charAt(0).toUpperCase() + sighting.shape.slice(1).toLowerCase() : "Unknown"}</p>
              </div>
              <div className={styles.commentBox}>
                <p><strong>Comment:</strong> {sighting.comments || "No comments"}</p>
              </div>
            </div>

            {/* User Comments */}
            <div className={styles.userComments}>
              <h3>User Comments</h3>
              {userComments.length > 0 ? (
                userComments.map((comment, index) => (
                  <p key={index} className={styles.comment}>{comment}</p>
                ))
              ) : (
                <p>No user comments yet.</p>
              )}
            </div>

            {/* Add Comment Section */}
            <div className={styles.addComment}>
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="Add a comment..."
                className={styles.commentInput}
              />
              <button onClick={handleAddComment} className={styles.commentButton}>Add Comment</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};


export default UFO_Sighting_Details;
