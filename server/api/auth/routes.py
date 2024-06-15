from flask import Blueprint, request, jsonify, session
from ..api import bcrypt
from ..repositories.user_repository import User, UserRepository
from ..repositories.preference_repository import Preference, PreferenceRepository

def create_blueprint(ur: UserRepository, pr: PreferenceRepository)->Blueprint:
    bp = Blueprint('auth', __name__)

    @bp.route("/@me", methods=["GET"])
    def get_current_user():
        user_id = session.get("user_id")
        if not user_id:
            return jsonify(
                {
                    "status": "ERROR",
                    "error": "Invalid session token"
                }), 401
        
        user = ur.get(id=user_id)
        return jsonify({
            "id": user.id,
            "email": user.email
        }) 

    @bp.route("/register", methods=["POST"])
    def register_user():
        email = request.json["email"]
        password = request.json["password"]

        # Email already in use
        if ur.get(email=email):
            return jsonify(
                {
                    "status": "ERROR",
                    "error": "Email already exists"
                }), 409
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password=hashed_password)
        new_preference = Preference(id=new_user.id, email=email)
        ur.add(**vars(new_user))
        pr.add(**vars(new_preference))

        session["user_id"] = new_user.id

        return jsonify({
            "id": new_user.id,
            "email": new_user.email
        })
        
    @bp.route("/login", methods=["POST"])
    def login_user():
        email = request.json["email"]
        password = request.json["password"]
        user = ur.get(email=email)

        # User is not in table
        if not user:
            return jsonify(
                {
                    "status": "ERROR",
                    "error": "Unauthorized"
                }), 401
        
        # Password does not match
        if not bcrypt.check_password_hash(user.password, password):
            return jsonify(
                {
                    "status": "ERROR",
                    "error": "Unauthorized"
                }), 401
        
        session["user_id"] = user.id

        return jsonify({
            "id": user.id,
            "email": user.email
        })

    @bp.route("/logout", methods=["POST"])
    def logout_user():
        session.pop("user_id", None)
        return jsonify(
                { "status": "SUCCESS" }), 200

    @bp.route("/update-password", methods=["POST"])
    def update_user_password():
        user_id = session.get("user_id")
        email = request.json["email"]
        password = request.json["password"]

        if not user_id:
            return jsonify(
                {
                    "status": "ERROR",
                    "error": "Invalid session token"
                }), 401

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        ur.update(id=user_id, email=email, new_password=hashed_password)
        return jsonify({
            "id": user_id,
            "email": email,
        })

    @bp.route("/delete", methods=["POST"])
    def delete_user():
        user_id = session.pop("user_id", None)
        user = ur.get(id=user_id)
        if not user:
            return jsonify(
                {
                    "status": "ERROR",
                    "error": "Invalid session token"
                }), 401

        ur.delete(id=user_id, email=user.email)
        pr.delete(id=user_id, email=user.email)
        return jsonify(
                { "status": "SUCCESS" }), 200

    @bp.route("/get-preferences", methods=["GET"])
    def get_user_preferences():
        user_id = session.get("user_id")

        if not user_id:
            return jsonify(
                {
                    "status": "ERROR",
                    "error": "Invalid session token"
                }), 401
        
        preference = pr.get(id=user_id)
        return jsonify({
            "id": preference.id,
            "email": preference.email,
            "preferences": list(preference.preferences)
        }) 

    @bp.route("/update-preferences", methods=["POST"])
    def update_user_preferences():
        user_id = session.get("user_id")
        email = request.json["email"]
        preferences = request.json["preferences"]

        # Error: could not find entry in table
        if not pr.get(id=user_id, email=email):
            return jsonify(
                {
                    "status": "ERROR",
                    "error" : "Invalid session token"
                }), 401

        response = pr.update(id=user_id, email=email, new_preferences=set(preferences))

        return jsonify({
            "id": user_id,
            "email": email,
            "preferences": list(response['preferences'])
        })

    return bp
