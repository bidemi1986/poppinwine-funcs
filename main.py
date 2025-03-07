# main.py
import os
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify, request
import functions_framework
from firestore_vector_search.query import query_the_web

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv() 
PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
# LOCATION = os.getenv("FIREBASE_SERVER_LOCATION")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Hello, Flask Cloud Function!"})

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')
    return jsonify({"message": f"Hello, {name}!"})

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "Please provide a query in the request body"}), 400
    
    query_text = data['query']
    try:
        result = query_the_web(query_text)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({"error": f"Failed to process query: {str(e)}"}), 500

@functions_framework.http
def flask_app(request):
    return app(request)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))