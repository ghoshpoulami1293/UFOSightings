const connection = new Mongo("localhost:27017"),
  db = connection.getDB("MongoProject"),
  UFOColl = db.getCollection("UFOSightings"),
  geoUFOColl = db.getCollection("GeoUFOSightings");

const IMAGES_FOLDER = "./images";

// this will be a dict to use for later to match the state acronym to the image format
const stateMap = {
  'al': 'alabama', 'ak': 'alaska', 'az': 'arizona', 'ar': 'arkansas', 'ca': 'california',
  'co': 'colorado', 'ct': 'connecticut', 'de': 'delaware', 'fl': 'florida', 'ga': 'georgia',
  'hi': 'hawaiian-islands', 'id': 'idaho', 'il': 'illinois', 'in': 'indiana', 'ia': 'iowa',
  'ks': 'kansas', 'ky': 'kentucky', 'la': 'louisiana', 'me': 'maine', 'md': 'maryland',
  'ma': 'massachusetts', 'mi': 'michigan', 'mn': 'minnesota', 'ms': 'mississippi',
  'mo': 'missouri', 'mt': 'montana', 'ne': 'nebraska', 'nv': 'nevada', 'nh': 'new-hampshire',
  'nj': 'new-jersey', 'nm': 'new-mexico', 'ny': 'new-york', 'nc': 'north-carolina',
  'nd': 'north-dakota', 'oh': 'ohio', 'ok': 'oklahoma', 'or': 'oregon', 'pa': 'pennsylvania',
  'ri': 'rhode-island', 'sc': 'south-carolina', 'sd': 'south-dakota', 'tn': 'tennessee',
  'tx': 'texas', 'ut': 'utah', 'vt': 'vermont', 'va': 'virginia', 'wa': 'washington',
  'wv': 'west-virginia', 'wi': 'wisconsin', 'wy': 'wyoming', 'pr': 'puerto-rico'
};

const ufoMap = {
  'chevron': ['chevron_a', 'chevron_b'],
  'cigar': ['cigar_a', 'cigar_b', 'cigar_c'],
  'cone': ['cone_a'],
  'crescent': ['crescent_a', 'crescent_b'],
  'cross': ['cross_a'],
  'cylinder': ['cylinder_a', 'cylinder_b', 'cylinder_c'],
  'disk': ['disk_a', 'disk_b', 'disk_c'],
  'dome': ['dome_a', 'dome_b', 'dome_c'],
  'pyramid': ['pyramid_a', 'pyramid_b'],
  'sphere': ['sphere_a', 'sphere_b', 'sphere_c'],
  'triangle': ['triangle_a', 'triangle_b', 'triangle_c']
};

// Delete all documents in GeoUFOSightings collection
geoUFOColl.deleteMany({});

// This copies data from the UFOColl collection to GeoUFOSightings
let count = 0;
UFOColl.find().forEach(doc => {
  geoUFOColl.insertOne(doc);
  count++;
  if (count % 1000 === 0) {
    print(count);
  }
});

print(`Document count: ${geoUFOColl.countDocuments()}`);

// This adds longitude and latitude geospatial points to the dataset
geoUFOColl.updateMany(
  {},
  [
    {
      $set: {
        location: {
          // Use aggregation pipeline $cond operator to populate 'location'
          // with null if longitude or latitude doesn't exist
          $cond: {
            if: {
              $or: [
                { $eq: ["$longitude", ""] },
                { $eq: ["$latitude", ""] }
              ]
            },
            then: null,
            else: {
              type: "Point",
              coordinates: [
                { $toDouble: "$longitude" }, // Ensure it's stored as a number
                { $toDouble: "$latitude" }   // Ensure it's stored as a number
              ]
            }
          }
        }
      }
    },
    {
      $unset: ["longitude", "latitude"] // Remove original properties
    }
  ]
);

// Check if update was successful by fetching one document
geoUFOColl.find().limit(1).forEach(doc => { printjson(doc); });

// Create the geospatial index for the location field
geoUFOColl.createIndex({ location: "2dsphere" });
geoUFOColl.createIndex({ city: 1 });       // Add index on city column
geoUFOColl.createIndex({ state: 1 });      // Add index on state column
geoUFOColl.createIndex({ country: 1 });    // Add index on country column

print("\nIndexes:");
printjson(geoUFOColl.getIndexes());

// Adding corresponding image ids to each document based on the state and shape
count = 0;
geoUFOColl.find().forEach(doc => {
  let stateAbbr = doc.state.toLowerCase();
  let shape = doc.shape.toLowerCase();
  
  if (stateMap.hasOwnProperty(stateAbbr)) {
    imageDoc = db.fs.files.findOne({ filename: stateAbbr + ".jpg" });
  }
  else {
    imageDoc = db.fs.files.findOne({ filename: "unknown_state.jpg" });
  }

  if (ufoMap.hasOwnProperty(shape)) {
    const imagesArray = ufoMap[shape];
    const randomImage = imagesArray[Math.floor(Math.random() * imagesArray.length)];
    ufoImageDoc = db.fs.files.findOne({ filename: randomImage + ".jpg" });
  }
  else {
    ufoImageDoc = db.fs.files.findOne({ filename: "default.jpg" });
  }

  let updateFields = {};
  
  if (imageDoc) {
    updateFields.image = imageDoc._id;
  }

  if (ufoImageDoc) {
    updateFields.ufo_image = ufoImageDoc._id;
  }
  // Update the document if there are fields to update
  if (Object.keys(updateFields).length > 0) {
    geoUFOColl.updateOne(
      { _id: doc._id },
      { $set: updateFields }
    );
  }

  count++;
  if (count % 1000 === 0) {
    print(count);
  }
});

print(`Total documents updated with images: ${geoUFOColl.countDocuments({ image: { $exists: true } })}`);

// Query for a specific point near Rochester
print('Let\'s query a specific point near Rochester');
geoUFOColl.find(
  {
    location: {
      $near: {
        $geometry: {
          type: "Point",
          coordinates: [-77.6064018064519, 43.15634212327678]
        },
        $maxDistance: 5000 // in meters
      }
    }
  },
  { _id: 0, id: 1, fromUserName: 1, location: 1, text: 1 }
).forEach(doc => {
  printjson(doc);
});

// Query for coordinates within a polygon
print('Now for a query finding coordinates within a polygon');
geoUFOColl.find(
  {
    location: {
      $geoWithin: {
        $geometry: {
          type: "Polygon",
          coordinates: [[
            [-77.53931906083284, 43.12382109880875],
            [-77.48610403294003, 43.12357051452809],
            [-77.48557651606735, 43.03451155002029],
            [-77.58634092727134, 43.03360224679762],
            [-77.53931906083284, 43.12382109880875]
          ]]
        }
      }
    }
  },
  { _id: 0, id: 1, fromUserName: 1, location: 1, text: 1 }
).forEach(doc => {
  printjson(doc);
});
