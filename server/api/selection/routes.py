import re
from flask import Blueprint, request, jsonify, session
from ..repositories.fusion_repository import FusionRepository

'''
    TODO:
     - set default categories if unprovided
     - create react component that sends the number of results
     - catch any errors from the query
'''
VALID_NUM_RESULTS = [10, 20, 30]

def create_blueprint(fr: FusionRepository)->Blueprint:
    bp = Blueprint('selection', __name__)

    @bp.route("/get-businesses", methods=["POST"])
    def get_businesses():
        geolocation = request.json["geolocation"]
        categories = request.json["categories"]
        num_results = request.json["num_results"]

        latitude = geolocation['latitude']
        longitude = geolocation['latitude']

        # Check if geolocation ranges are valid
        if not -90 < latitude < 90 or not -180 < longitude < 180:
            return jsonify({
                "status": "ERROR",
                "error": "Invalid geolocation coordinates provided"
            }), 400
        
        # Check if valid num_results is provided
        if num_results not in VALID_NUM_RESULTS:
            return jsonify({
                "status": "ERROR",
                "error": "Invalid request received"
            }), 400

        # remove whitespace from categories
        for i in range(len(categories)):
            categories[i].strip()

            # Clean up categories to prepare for url
            categories[i] = re.sub(r"[^\w\s]", '', categories[i])
            categories[i] = re.sub(r"\s+", '+', categories[i])

        # TODO: Make category formatting more sophisticated

        selections = fr.get_all(
            geolocation=geolocation, 
            categories=categories, 
            num_results=num_results
        )

        if not selections:
            return jsonify({
                "status": "ERROR",
                "error": "No results available"
            }), 400

        return jsonify({
            "selections": selections,
        })
        
    return bp

