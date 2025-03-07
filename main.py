import os
from flask import Flask, jsonify, request
import functions_framework

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Hello, Flask Cloud Function!"})

@app.route('/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'Guest')
    return jsonify({"message": f"Hello, {name}!"})

# Google Cloud Function requires an entry point function
@functions_framework.http
def flask_app(request):
    # Use the environment variable PORT if set, default to 8080
    port = int(os.environ.get("PORT", 8080))
    return app(request)
