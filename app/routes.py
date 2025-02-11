from flask import Blueprint, jsonify, request
from app.manga_scraper import MangaScraper
from app.mosque_scraper import MosqueScraper
from flask_cors import CORS

api = Blueprint("api", __name__)
CORS(api)

@api.route("/api/manga/list", methods=["POST"])
def get_manga():
    data = request.json
    if not data['url']:
        return jsonify({"error": "URL parameter is required"}), 400

    result = MangaScraper.scrape_manga(data)
    if "error" in result:
        return jsonify(result), 500

    return jsonify(result)

@api.route("/api/manga/detail", methods=["POST"])
def get_manga_detail():
    data = request.json
    if not data['url']:
        return jsonify({"error": "URL parameter is required"}), 400

    result = MangaScraper.scrape_manga_detail(data)
    if "error" in result:
        return jsonify(result), 500

    return jsonify(result)

@api.route("/api/mosque/list", methods=["POST"])
def get_mosque():
    data = request.json

    result = MosqueScraper.scrape_mosque(data)
    if "error" in result:
        return jsonify(result), 500

    return jsonify(result)

@api.route("/api/mosque/detail", methods=["POST"])
def get_mosque_detail():
    data = request.json
    if not data['url']:
        return jsonify({"error": "URL parameter is required"}), 400

    result = MosqueScraper.scrape_mosque_detail(data)
    if "error" in result:
        return jsonify(result), 500

    return jsonify(result)

@api.route('/api/health-check', methods=['GET'])
def endpoint():
    print("Request received!")
    return jsonify({"message": "Success!"})