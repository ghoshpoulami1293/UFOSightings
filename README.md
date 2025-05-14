
# UFO Sightings

## Technology Stack

### Backend: Flask (Python) with MongoDB

**Flask** is lightweight, easy to set up, and allows for rapid API development. Members of the team have already had work experience in backend development using Flask, so it was an easy choice.

**MongoDB** is a flexible NoSQL database that supports efficient text search and geospatial queries, which are crucial for our dataset. It leads to fast retrieval of data from api calls, and is a requirement for this project.

### Frontend:

The frontend is built using **ReactJS** with **Vite**, which provides fast development and build time. We chose React for its component-based structure, ease of integration with APIs, and flexibility in managing application state.

**Leaflet** is used for its interactive mapping capabilities, enhancing the user experience with geospatial visualization.

## Process

### Preparing the Dataset

The process of preparing our dataset involved four steps:

- **Obtaining the Data Source:** An online datasource was found for UFO sightings in CSV format.

- **Data Cleansing:** The dataset was cleaned by removing invalid latitude and longitude values and renaming column names for correct syntax in the database. Then, the following mongoimport line was run:
  `mongoimport --db MongoProject --collection UFOSightings --type csv --file "ufo_scrubbed.csv" --headerline`

- **Adding Images to GridFS:** State images and UFO images resembling shapes described in the dataset were uploaded to the GridFS database using the `mongofiles` feature. These were added to our dataset not native to original data source.
  e.g. `mongofiles --db MongoProject put al.jpg --local images/al.jpg`

- **Database Modification:** A JavaScript file was created to update the database by:

  - Converting latitude and longitude points into geographic location data for each document.
  - Mapping `image_ids` to respective state and UFO images based on the shape description and location of each sighting.

### Dataset Challenges

Biggest challenges with creating the database was data cleansing of the UFOSightings, as well as gathering and sythesizing an image data set of state and ufo images with our UFO Sightings dataset.

## Volume

Paste in the result of running countDocuments() on all of your collections:\

db.getCollectionNames().forEach(function(coll) {print(coll + ": " + db[coll].countDocuments({}));});\

GeoUFOSightings: 80332\

UFOSightings: 80332\

fs.files: 79\

fs.chunks: 151\

## Variety

Our application supports multiple types of search filters, each yielding a diverse set of results.

- Search by Country: Selecting "US" from the country dropdown returns a large number of sightings across different states in the U.S.

- Search by State: Selecting "NY" returns sightings primarily around urban areas like Buffalo and New York City.

- Search by Shape: Selecting "disk" shows multiple clustered sightings from different states.

- Search by City: Typing "rochester" in the city search box returns one of the most well-documented events in UFO history.

- Search by Comments: Typing "terrific" reveals a wide range of sightings reported as terrific incidents.

- Search Nearby (Geospatial): Clicking on a location in the map, and entering a radius like 10 miles, lets us observe localized sightings cluster.

## Bells and Whistles

Our team collaborated very well utilizing discord at github for this highly collaborative effort. Our database was uniquely structured with built index's on key search fields and two images related to location and ufo appearence. In addition, we included pagination capabilities for all searches so the front end could handle very large web result queries using sort by mongo features, limits, and offsets.

To improve the user experience, we included the following key features:

- Search Filters & Pagination:

Users can search UFO sightings by country, state, city, shape, or keywords in comments. We support pagination to efficiently handle large result sets.

- Interactive Map View (Leaflet)

A dynamic Leaflet map allows users to visually locate sightings by clicking on a point, entering a radius, and finding nearby events.

- Google Maps Embed Integration:

For each search result, we include a zoomed-in embedded Google Map of the sighting's location using the EmbeddedGoogleMap component. This provides geographic context and improves visualization of where the event occurred.

In addition, the application's comprehensive test suite verifies all API endpoints across multiple files, covering search functionality, data filtering, pagination, individual sighting details, comment addition, image handling, and metadata aggregation, with both success and error cases thoroughly tested through mocked MongoDB interactions.

# How to Run the Application

## Boot up MongoDB with authentication

Run the following command in a terminal:

`sudo mongod --dbpath /var/lib/mongodb --bind_ip 127.0.0.1 --port 27017 --auth`

## Load the Dataset

Navigate to `mongo-project-lilo-stitch/backend/app`:

- Run: `mongosh create_db.js`

- Run: `mongosh build_project_db.js`

## Start the Flask Application

Navigate to the root directory `mongo-project-lilo-stitch/backend/app` and run:

`python3 -m app`
