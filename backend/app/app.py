from flask import Flask
from flask_cors import CORS
from routes import init_routes

# Initialize Flask app
app = Flask(__name__, static_folder="static/dist", static_url_path="/")

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type"]}})

# Initialize routes
init_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3000) 
