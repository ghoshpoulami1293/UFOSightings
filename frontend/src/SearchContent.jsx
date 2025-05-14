import React, { useState } from "react";
import LeafletMapComponent from "./LeafletMapComponent";
import styles from "./assets/css/SearchContent.module.css";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import BASE_URL from './config';

const SearchContent = () => {
  const [coordinates, setCoordinates] = useState({ lat: null, lng: null });
  const [searchQuery, setSearchQuery] = useState(""); 
  const [searchType, setSearchType] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false); 

  const [radius, setRadius] = useState("");
  const [dropdownOptions, setDropdownOptions] = useState([]);
  const [showDropdownInput, setShowDropdownInput] = useState(false);


  const [page, setPage] = useState(1);
  const [hasSearched, setHasSearched] = useState(false);
  const [dropdownValues, setDropdownValues] = useState([]);
  const [selectedValue, setSelectedValue] = useState("");
  const [pendingNearbySearch, setPendingNearbySearch] = useState(false);
  const [searchTrigger, setSearchTrigger] = useState(0);

  
  // console.log(coordinates);
  useEffect(() => {
    const fetchDropdownValues = async () => {
      let url = "";
      if (searchType === "country") url = `${BASE_URL}/countries`;
      else if (searchType === "state") url = `${BASE_URL}/states`;
      else if (searchType === "shape") url = `${BASE_URL}/shapes`;
      else {
        setDropdownValues([]);
        return;
      }
  
      const response = await fetch(url);
      const data = await response.json();
      setDropdownValues(data);
    };
  
    fetchDropdownValues();
    // setSelectedValue(""); 
    setPage(1); 
  }, [searchType]);
  
  const handleSearchNearby = () => {
    if (!coordinates.lat || !coordinates.lng) {
      alert("Please click on the map to select a location.");
      return;
    }
    if (!radius.trim() || isNaN(radius) || Number(radius) <= 0) {
      alert("Please enter a valid radius.");
      return;
    }
  
    setSearchType("location");          
    // setPendingNearbySearch(true);    
    setPage(1);                         
    setHasSearched(true);       
    setSearchTrigger((prev) => prev + 1);       
  };


  const specificSearch = () => {

    setSearchType(searchType);          
    // setPendingNearbySearch(true);    
    setPage(1);                         
    setHasSearched(true);       
    setSearchTrigger((prev) => prev + 1);       
  };




  const handleSearch = async () => {

    setSearchResults([]);
  
    let apiUrl = "";
  
    if (searchType === "location") {
      apiUrl = `${BASE_URL}/search_nearby?lat=${coordinates.lat}&lon=${coordinates.lng}&radius=${radius}&page=${page}`;
    } else {
      // setHasSearched(false);
      setCoordinates({ lat: null, lng: null });
      
      let queryParam = selectedValue;
      // if (!queryParam.trim() || !searchQuery.trim()) {
      //   alert("Please select or enter a value.");
      //   return;
      // }


      switch (searchType) {
        case "all":
          if (!searchQuery.trim()) {
            alert("Please select or enter a value.");
            return;
          }
      
          apiUrl = `${BASE_URL}/search_word?q=${searchQuery}&page=${page}`;
          break;
        case "country":
          if (!queryParam.trim()) {
            alert("Please select or enter a value.");
            return;
          }
          apiUrl = `${BASE_URL}/sightings/country/${queryParam}?page=${page}`;
          break;
        case "state":
          if (!queryParam.trim()) {
            alert("Please select or enter a value.");
            return;
          }
          apiUrl = `${BASE_URL}/sightings/state/${queryParam}?page=${page}`;
          break;
        case "shape":
          if (!queryParam.trim()) {
            alert("Please select or enter a value.");
            return;
          }
          apiUrl = `${BASE_URL}/sightings/shape/${queryParam}?page=${page}`;
          break;
        case "city":
          if (!searchQuery.trim()) {
            alert("Please select or enter a value.");
            return;
          }
      
          apiUrl = `${BASE_URL}/sightings/city/${searchQuery}?page=${page}`;
          break;
        case "comments":
          if (!searchQuery.trim()) {
            alert("Please select or enter a value.");
            return;
          }
      
          apiUrl = `${BASE_URL}/sightings/comments/${searchQuery}?page=${page}`;
          break;
        default:
          alert("Invalid search type selected.");
          return;
      }
    }
  
    try {
      setLoading(true);
      const response = await fetch(apiUrl);
      const data = await response.json();
      setSearchResults(data.data || []);
      // setSearchType("default");  
    } catch (error) {
      console.error("Error fetching data:", error);
      alert("Failed to fetch data.");
    } finally {
      setLoading(false);
    }
  };
  

  useEffect(() => {
    if (hasSearched) {
      handleSearch();
    }
  }, [page, searchType, searchTrigger]);


// useEffect(() => {
//   if (hasSearched) {
//     handleSearch();
//     setPendingNearbySearch(false);
//   }
// }, [page, searchType, hasSearched]);



const handleNextPage = () => setPage((prev) => prev + 1);
const handlePrevPage = () => setPage((prev) => Math.max(prev - 1, 1));



// const handleSearchNearby = async () => {
//   if (!coordinates.lat || !coordinates.lng) {
//     alert("Please click on the map to select a location.");
//     return;
//   }
//   if (!radius.trim() || isNaN(radius) || Number(radius) <= 0) {
//     alert("Please enter a valid radius.");
//     return;
//   }

//   const apiUrl = `http://localhost:5000/search_nearby?lat=${coordinates.lat}&lon=${coordinates.lng}&radius=${radius}&page=${page}`;

//   try {
//     setLoading(true);
//     const response = await fetch(apiUrl, {
//       method: "GET",
//       headers: {
//         "Content-Type": "application/json",
//       },
//     });

//     if (!response.ok) {
//       throw new Error("Network response was not ok");
//     }

//     const data = await response.json();
//     setSearchResults(data?.data || []); // Assuming data structure { data: [], page, total, limit }
//   } catch (error) {
//     console.error("Error fetching data:", error);
//     alert("Failed to fetch data. Please try again.");
//   } finally {
//     setLoading(false);
//   }
// };



  const [sortColumn, setSortColumn] = useState(null);
  const [sortOrder, setSortOrder] = useState("asc");

  const handleSort = (column) => {
    const newSortOrder = sortColumn === column && sortOrder === "asc" ? "desc" : "asc";
    setSortColumn(column);
    setSortOrder(newSortOrder);

    const sortedResults = [...searchResults].sort((a, b) => {
      if (a[column] < b[column]) return newSortOrder === "asc" ? -1 : 1;
      if (a[column] > b[column]) return newSortOrder === "asc" ? 1 : -1;
      return 0;
    });

    setSearchResults(sortedResults);
  };
  const navigate = useNavigate();
  
  const handleRowClick = (result) => {
    navigate(`/searchcontent/${result._id}`); 
  };

  return (
    <div className={styles.container}>
      <div className={styles.mapSection}>
    
            <div className={styles.radiusInputContainer}>
              <label className={styles.label} htmlFor="radiusInput">
                  Find sightings within a radius:
              </label>
              <input
                  type="number"
                  placeholder="Enter radius (miles)"
                  value={radius}
                  onChange={(e) => setRadius(e.target.value)}
                  className={styles.radiusInput}
              />
              <button className={styles.goButton} onClick={handleSearchNearby}>
                  Search Nearby
              </button>
            </div>

            <LeafletMapComponent coordinates={coordinates} setCoordinates={setCoordinates} searchResults={searchResults} />
      </div>


      <div className={styles.searchSection}>
        <label className={styles.label} >
            Search by filter (country, state, city, Shape or Comments):
        </label>
        <div className={styles.searchBox}>


        <select
            value={searchType}
            onChange={(e) => {
              setSearchType(e.target.value);
              setPage(1); 
            }}
            
            className={styles.dropdown}
          >
            <option value="">-- Select --</option>
            <option value="country">Country</option>
            <option value="state">State</option>
            <option value="city">City</option>
            <option value="shape">Shape</option>
            <option value="comments">Comments</option>
            <option value="all">All</option>
          </select>



          {["country", "state", "shape"].includes(searchType) ? (
            <select
              className={styles.searchInput}
              value={selectedValue}
              // onChange={(e) => setSelectedValue(e.target.value)}
              onChange={(e) => {
                setSelectedValue(e.target.value);
                setPage(1); 
              }}
              
            >
              <option value="">-- Select --</option>
              {dropdownValues.map((val) => (
                <option key={val} value={val}>
                  {val.toUpperCase()}
                </option>
              ))}
            </select>
          ) : (
            <input
              type="text"
              placeholder="Search..."
              value={searchQuery}
             
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setPage(1); 
              }}
              className={styles.searchInput}
            />
          )}


          <button className={styles.goButton} onClick={specificSearch} disabled={loading}>
            {loading ? "Searching..." : "Go"}
          </button>
        </div>


        <div className={styles.resultsTable}>
          <table>
            <thead>
              <tr>
                <th onClick={() => handleSort("city")}>City {sortColumn === "city" ? (sortOrder === "asc" ? "▲" : "▼") : ""}</th>
                <th onClick={() => handleSort("state")}>State {sortColumn === "state" ? (sortOrder === "asc" ? "▲" : "▼") : ""}</th>
                <th onClick={() => handleSort("country")}>Country {sortColumn === "country" ? (sortOrder === "asc" ? "▲" : "▼") : ""}</th>
                <th onClick={() => handleSort("shape")}>Shape {sortColumn === "shape" ? (sortOrder === "asc" ? "▲" : "▼") : ""}</th>
                <th>Comments</th>
              </tr>
            </thead>

            <tbody>
                {searchResults.length > 0 ? (
                    searchResults.map((result, index) => (
                    <tr key={index} onClick={() => handleRowClick(result)} className={styles.clickableRow}>
                        <td>{result.city}</td>
                        <td>{result.state.toUpperCase()}</td>
                        <td>{result.country || "N/A"}</td>
                        <td>{result.shape}</td>
                        <td>{result.comments}</td>
                    </tr>
                    ))
                ) : (
                    <tr>
                    <td colSpan="5">No results found.</td>
                    </tr>
                )}
                </tbody>

          </table>

          <div className={styles.pagination}>
            <button disabled={page === 1} onClick={handlePrevPage}>Previous</button>
            <span>Page {page}</span>
            <button disabled={searchResults.length === 0} onClick={handleNextPage}>Next</button>
            {/* <button onClick={handleNextPage}>Next</button> */}
          </div>

        </div>
      </div>
    </div>
  );
};

export default SearchContent;