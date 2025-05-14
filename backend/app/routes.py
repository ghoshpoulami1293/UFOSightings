import base64
from flask import request, jsonify, send_from_directory
from bson import ObjectId
from db import ufoSightings, fs

# Set a fixed limit for pagination
LIMIT = 10

# Helper Functions
def convert_to_str(doc):
    """Convert ObjectId fields to strings and extract required fields."""
    return {
        "_id": str(doc["_id"]),
        "city": doc.get("city", "N/A"),
        "comments": doc.get("comments", "N/A"),
        "country": doc.get("country", "N/A"),
        "shape": doc.get("shape", "N/A"),
        "state": doc.get("state", "N/A"),
        "latitude": doc.get("location", {}).get("coordinates", [None, None])[1],
        "longitude": doc.get("location", {}).get("coordinates", [None, None])[0]
    }

def get_base64_encoded_image(img_id):
    """Fetch and encode an image to Base64 format."""
    try:
        with fs.get(ObjectId(img_id)) as img:
            return base64.b64encode(img.read()).decode('utf-8')
    except Exception as e:
        print(f"Error fetching image with ID {img_id}: {e}")
        return None

def paginate(query, page, sort_field="_id", sort_order=1):
    """Apply pagination to a MongoDB query."""
    offset = (page - 1) * LIMIT
    results = (
        ufoSightings.find(query)
        .sort([(sort_field, sort_order)])
        .skip(offset)
        .limit(LIMIT)
    )
    total_results = ufoSightings.count_documents(query)
    return list(results), total_results

# Initialize routes
def init_routes(app):

    @app.route("/")
    def home():
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/search_word", methods=['GET'])
    def search_sightings():
        """Search for sightings using a keyword (partial match, case-insensitive) with pagination."""
        keyword = request.args.get("q", "").strip()
        page = int(request.args.get("page", 1))

        if not keyword:
            return jsonify({"error": "No search term provided"}), 400

        query = {"$or": [
            {"comments": {"$regex": keyword, "$options": "i"}},
            {"city": {"$regex": keyword, "$options": "i"}},
            {"state": {"$regex": keyword, "$options": "i"}},
            {"shape": {"$regex": keyword, "$options": "i"}}
        ]}

        results, total = paginate(query, page)
        response = {
            "data": [convert_to_str(doc) for doc in results],
            "total": total,
            "page": page,
            "limit": LIMIT
        }
        return jsonify(response)

    @app.route("/search_nearby", methods=['GET'])
    def search_nearby():
        """Find sightings within a geospatial area (latitude, longitude, and radius) with pagination."""
        try:
            lat, lon, radius_miles = float(request.args["lat"]), float(request.args["lon"]), float(request.args["radius"])
            page = int(request.args.get("page", 1))
        except (KeyError, ValueError):
            return jsonify({"error": "Invalid latitude, longitude, radius, page, or limit"}), 400

        radius_radians = radius_miles / 3959  # Convert miles to radians
        query = {
            "location": {
                "$geoWithin": {
                    "$centerSphere": [[lon, lat], radius_radians]  
                }
            }
        }
        results, total = paginate(query, page)
        response = {
            "data": [convert_to_str(doc) for doc in results],
            "total": total,
            "page": page,
            "limit": LIMIT
        }
        return jsonify(response)

    @app.route("/sighting/<sighting_id>", methods=['GET'])
    def get_sighting(sighting_id):
        """Fetch full sighting details including text and images."""
        doc = ufoSightings.find_one({"_id": ObjectId(sighting_id)})
        if not doc:
            return jsonify({"error": "Sighting not found"}), 404

        img_id = doc.get("image")
        encoded_string = get_base64_encoded_image(img_id) if img_id else None

        ufo_img_id = doc.get("ufo_image")
        ufo_encoded_string = get_base64_encoded_image(ufo_img_id) if ufo_img_id else None


        doc["_id"] = str(doc["_id"])
        doc["image"] = encoded_string  # Base64 encoded string for frontend display
        doc["ufo_image"] = ufo_encoded_string  # Base64 encoded string for frontend display

        coordinates = doc.get("location", {}).get("coordinates", [None, None])
        longitude, latitude = coordinates 
        doc["latitude"] = latitude  
        doc["longitude"] = longitude  

        return jsonify(doc)

    @app.route("/sighting/<sighting_id>/comment", methods=['POST'])
    def add_comment(sighting_id):
        """Add a comment to a sighting."""
        doc = ufoSightings.find_one({"_id": ObjectId(sighting_id)})
        if not doc:
            return jsonify({"error": "Sighting not found"}), 404

        comment = request.json.get("comment", "").strip()
        if not comment:
            return jsonify({"error": "Empty comment"}), 400

        ufoSightings.update_one({"_id": ObjectId(sighting_id)}, {"$push": {"user_comments": comment}})
        return jsonify({"success": True, "user_comment": comment})

    @app.route("/sightings/country/<country_code>", methods=['GET'])
    def search_country(country_code):
        """Search for sightings using a country with pagination."""
        try:
            page = int(request.args.get("page", 1))

            query = {"country": {"$regex": country_code, "$options": "i"}}
            results, total = paginate(query, page)
            
            response = {
                "data": [convert_to_str(doc) for doc in results],
                "total": total,
                "page": page,
                "limit": LIMIT
            }
            return jsonify(response)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/sightings/city/<city_name>", methods=['GET'])
    def search_city(city_name):
        """Search for sightings using a city with pagination."""
        try:
            page = int(request.args.get("page", 1))

            query = {"city": {"$regex": city_name, "$options": "i"}}
            results, total = paginate(query, page)
            
            response = {
                "data": [convert_to_str(doc) for doc in results],
                "total": total,
                "page": page,
                "limit": LIMIT
            }
            return jsonify(response)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/sightings/shape/<shape_name>", methods=['GET'])
    def search_shape(shape_name):
        """Search for sightings using a shape with pagination."""
        try:
            page = int(request.args.get("page", 1))

            query = {"shape": {"$regex": shape_name, "$options": "i"}}
            results, total = paginate(query, page)

            response = {
                "data": [convert_to_str(doc) for doc in results],
                "total": total,
                "page": page,
                "limit": LIMIT
            }
            return jsonify(response)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @app.route("/sightings/comments/<comment>", methods=['GET'])
    def search_comments(comment):
        """Search for sightings using a comment with pagination."""
        page = int(request.args.get("page", 1))
        
        query = {"comments": {"$regex": comment, "$options": "i"}}
        results, total = paginate(query, page)
        
        response = {
            "data": [convert_to_str(doc) for doc in results],
            "total": total,
            "page": page,
            "limit": LIMIT
        }
        return jsonify(response)

    @app.route("/sightings/state/<state_code>", methods=['GET'])
    def search_state(state_code):
        """Search for sightings using a state with pagination."""
        try:
            page = int(request.args.get("page", 1))

            query = {"state": {"$regex": state_code, "$options": "i"}}
            results, total = paginate(query, page)
            
            response = {
                "data": [convert_to_str(doc) for doc in results],
                "total": total,
                "page": page,
                "limit": LIMIT
            }
            return jsonify(response)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @app.route("/countries", methods=['GET'])
    def get_countries():
        """Fetch list of all countries."""
        pipeline = [
            {"$group": {"_id": "$country"}}
        ]
        
        try:
            # Fetch the aggregated results as a list
            results = list(ufoSightings.aggregate(pipeline))
            
            # Check if results are empty
            if not results:
                return jsonify({"error": "Countries not found"}), 404
            
            # Create a simple list of country names
            countries = [r["_id"] for r in results if r["_id"]]
            return jsonify(countries), 200

        except Exception as e:
            # Handle unexpected errors
            return jsonify({"error": str(e)}), 500
        
    @app.route("/states", methods=['GET'])
    def get_states():
        """Fetch list of all states."""
        pipeline = [
            {"$group": {"_id": "$state"}}
        ]
        
        try:
            # Fetch the aggregated results as a list
            results = list(ufoSightings.aggregate(pipeline))
            
            # Check if results are empty
            if not results:
                return jsonify({"error": "States not found"}), 404
            
            # Create a simple list of state names
            states = [r["_id"] for r in results if r["_id"]]
            return jsonify(states), 200

        except Exception as e:
            # Handle unexpected errors
            return jsonify({"error": str(e)}), 500
        
    @app.route("/shapes", methods=['GET'])
    def get_shapes():
        """Fetch list of all shapes."""
        pipeline = [
            {"$group": {"_id": "$shape"}}
        ]
        
        try:
            # Fetch the aggregated results as a list
            results = list(ufoSightings.aggregate(pipeline))
            
            # Check if results are empty
            if not results:
                return jsonify({"error": "Shapes not found"}), 404
            
            # Create a simple list of country names
            shapes = [r["_id"] for r in results if r["_id"]]
            return jsonify(shapes), 200

        except Exception as e:
            # Handle unexpected errors
            return jsonify({"error": str(e)}), 500
