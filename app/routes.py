from flask import Blueprint, jsonify, request
from app.scraper import MangaScraper

api = Blueprint("api", __name__)

@api.route("/api/manga", methods=["GET"])
def get_manga():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    result = MangaScraper.scrape_manga(url)
    if "error" in result:
        return jsonify(result), 500

    return jsonify(result)
