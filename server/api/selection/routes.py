import re
from flask import Blueprint, request, jsonify, session
from ..repositories.fusion_repository import FusionRepository

'''
    TODO:
     - set default categories if unprovided
'''
VALID_NUM_RESULTS = [10, 20, 30]

def create_blueprint(fr: FusionRepository)->Blueprint:
    bp = Blueprint('selection', __name__)

    # Note: POST for a simpler request body
    @bp.route("/get-businesses", methods=["POST"])
    def get_businesses():
        geolocation = request.json["geolocation"]
        categoriesArr = request.json["categories"]
        price = request.json["price"]
        num_results = request.json["num_results"]
        radius = request.json["radius"]

        latitude = geolocation['latitude']
        longitude = geolocation['longitude']

        # Check if geolocation ranges are valid
        if not -90 < float(latitude) < 90 or not -180 < float(longitude) < 180:
            return jsonify({
                "status": "ERROR",
                "error": "Invalid geolocation coordinates provided"
            }), 400
        
        # Check if valid price is provided
        if not 1 <= len(price) <= 4:
            return jsonify({
                "status": "ERROR",
                "error": "Invalid price range requested"
            }), 400
        
        if price != "$" * len(price):
            return jsonify({
                "status": "ERROR",
                "error": "Invalid price string requested"
            }), 400
        
        # Check if valid num_results is provided
        if type(num_results) == str and not num_results.isdigit():
            return jsonify({
                "status": "ERROR",
                "error": "Invalid format of num_results provided"
            }), 400
        num_results = int(num_results)

        if num_results not in VALID_NUM_RESULTS:
            return jsonify({
                "status": "ERROR",
                "error": "Invalid number of results requested"
            }), 400
        
        # Check if valid radius is provided
        if type(radius) == str and not radius.isdigit():
            return jsonify({
                "status": "ERROR",
                "error": "Invalid format of radius provided"
            }), 400
        radius = int(radius)
        
        if not 5 <= radius <= 25:
            return jsonify({
                "status": "ERROR",
                "error": "Invalid search radius requested"
            }), 400
        
        # Extract category name from array of objects
        categories = []
        for category in categoriesArr:
            categories.append(category["category"].lower())

        # remove whitespace from categories
        for i in range(len(categories)):
            categories[i].strip()

            # Clean up categories to prepare for url
            categories[i] = re.sub(r"[^\w\s]", '', categories[i])
            categories[i] = re.sub(r"\s+", '+', categories[i])

        # Format the price range
        price = range(1, len(price) + 1)
        price = [str(i) for i in price]
        price = '%2C'.join(price)

        # Convert miles to meters
        radius = int(round(radius * 1609.34))
        radius = min(radius, 40000) # Maximum range of the API

        selections = fr.get_all(
            geolocation=geolocation, 
            categories=categories, 
            price=price,
            num_results=num_results,
            radius=radius
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

