from flask import Blueprint, request, jsonify, session
from datetime import datetime, timezone
from nanoid import generate
from decimal import Decimal
from ..repositories.lobby_repository import Lobby, LobbyRepository

MAXIMUM_LOBBY_AGE = 1800    # 1800s = 30min

def isExpiredLobby(timestamp: str) -> bool:
    format = '%Y-%m-%dT%H:%M:%SZ'   # JavaScript UTC Date format
    start = datetime.strptime(timestamp, format)
    now = datetime.now(timezone.utc)
    delta = (now - start).total_seconds()
    return delta >= MAXIMUM_LOBBY_AGE

def create_blueprint(lr: LobbyRepository)->Blueprint:
    bp = Blueprint('lobby', __name__)

    @bp.route("/create-lobby", methods=["POST"])
    def create_lobby():
        socketID = request.json["socketID"]
        lobby = None
        for _ in range(10):
            lobbyID = generate('23456789abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ', 4)
            lobby = lr.get(lobbyID=lobbyID)
            if not lobby or isExpiredLobby(lobby.timestamp):
                lobby = Lobby(lobbyID=lobbyID, host=socketID, timestamp=None)
                lr.add(**vars(lobby))
                return jsonify({
                    "status": "SUCCESS",
                    "lobbyID": lobbyID,
                }) 
            
        return jsonify({
            "status": "TIMEOUT",
            "error": "10 collisions occurred"
        }), 409

    # TODO: check timestamp
    @bp.route("/join-lobby", methods=["POST"])
    def join_lobby():
        lobbyID = request.json["lobbyID"]
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        if not lobby.joinable:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby already started"
            }), 403
        return jsonify({
            "status": "SUCCESS",
            "lobbyID": lobbyID,
        }) 

    @bp.route("/delete-lobby", methods=["POST"])
    def delete_lobby():
        lobbyID = request.json["lobbyID"]
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        lr.delete(lobbyID=lobbyID)
        return jsonify({ "status": "SUCCESS" }), 200

    @bp.route("/get-lobby-timestamp", methods=["GET"])
    def get_lobby_timestamp():
        lobbyID = request.args.get('lobbyID')
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "timestamp": lobby.timestamp
        }) 
    
    @bp.route("/get-lobby-joinable", methods=["GET"])
    def get_lobby_joinable():
        lobbyID = request.args.get('lobbyID')
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "joinable": lobby.joinable
        }) 
    
    @bp.route("/get-lobby-businesses", methods=["GET"])
    def get_lobby_businesses():
        lobbyID = request.args.get('lobbyID')
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "businesses": lobby.businesses
        }) 
    
    @bp.route("/get-lobby-categories", methods=["GET"])
    def get_lobby_categories():
        lobbyID = request.args.get('lobbyID')
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "lobby does not exist"
            }), 404
        categories = lobby.categories
        return jsonify({
            "status": "SUCCESS",
            "categories": categories
        }) 
    
    @bp.route("/get-lobby-votes", methods=["GET"])
    def get_lobby_votes():
        lobbyID = request.args.get('lobbyID')
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "votes": lobby.votes
        }) 
    
    @bp.route("/get-lobby-sockets", methods=["GET"])
    def get_lobby_sockets():
        lobbyID = request.args.get('lobbyID')
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "sockets": lobby.sockets
        }) 
    
    @bp.route("/get-lobby-preferences", methods=["GET"])
    def get_lobby_preferences():
        lobbyID = request.args.get('lobbyID')
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "preferences": lobby.preferences
        }) 
    
    @bp.route("/get-lobby-host", methods=["GET"])
    def get_lobby_host():
        lobbyID = request.args.get('lobbyID')
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "host": lobby.host
        }) 
    
    @bp.route("/get-lobby-phase", methods=["GET"])
    def get_lobby_phase():
        lobbyID = request.args.get('lobbyID')
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "phase": lobby.phase
        }) 
    
    @bp.route("/update-lobby-preferences", methods=["POST"])
    def update_lobby_preferences():
        lobbyID = request.json["lobbyID"]
        preferences = request.json["preferences"]
        if ("coordinates" not in preferences or 
            "latitude" not in preferences["coordinates"] or 
            "longitude" not in preferences["coordinates"]):
            return jsonify({
                "status": "ERROR",
                "error": "Preferences not formatted correctly"
            })
        preferences["coordinates"]["latitude"] = Decimal(str(preferences["coordinates"]["latitude"]))
        preferences["coordinates"]["longitude"] = Decimal(str(preferences["coordinates"]["longitude"]))
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        lr.update_preferences(lobbyID=lobbyID, preferences=preferences)
        return jsonify({ "status": "SUCCESS" }), 200
    
    @bp.route("/update-lobby-timestamp", methods=["POST"])
    def update_lobby_timestamp():
        lobbyID = request.json["lobbyID"]
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        lr.update_timestamp(lobbyID=lobbyID)
        return jsonify({ "status": "SUCCESS" }), 200
    
    @bp.route("/update-lobby-phase", methods=["POST"])
    def update_lobby_phase():
        lobbyID = request.json["lobbyID"]
        phase = request.json["phase"]
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        lr.update_phase(lobbyID=lobbyID, phase=phase)
        return jsonify({ "status": "SUCCESS" }), 200
    
    @bp.route("/update-lobby-joinable", methods=["POST"])
    def update_lobby_joinable():
        lobbyID = request.json["lobbyID"]
        joinable = request.json["joinable"]
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        lr.update_joinable(lobbyID=lobbyID, joinable=joinable)
        return jsonify({ "status": "SUCCESS" }), 200
    
    @bp.route("/update-lobby-businesses", methods=["POST"])
    def update_lobby_businesses():
        lobbyID = request.json["lobbyID"]
        businesses = request.json["businesses"]
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        lr.update_businesses(lobbyID=lobbyID, businesses=businesses)
        return jsonify({ "status": "SUCCESS" }), 200

    @bp.route("/add-lobby-category", methods=["POST"])
    def add_lobby_categories():
        lobbyID = request.json["lobbyID"]
        socketID = request.json["socketID"]
        category = request.json["category"]
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "lobby does not exist"
            }), 404
        index, isNew = 0, True
        categories = lobby.categories
        for i, category_obj in enumerate(categories): # For now, at most O(30)
            if category_obj["name"] == category:
                category_obj["sockets"].append(socketID) 
                categories[i] = category_obj
                isNew = False
                break
            index += 1
        if isNew:
            categories.append({
                "name": category,
                "sockets": [socketID]
            })
        lr.update_categories(lobbyID=lobbyID, categories=categories)
        return jsonify({ 
            "status": "SUCCESS",
        }), 200

    @bp.route("/remove-lobby-category", methods=["POST"])
    def remove_lobby_categories():
        lobbyID = request.json["lobbyID"]
        socketID = request.json["socketID"]
        category = request.json["category"]
        deletion_index = request.json["deletion_index"]
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        if len(lobby.categories) <= deletion_index:
            return jsonify({
                "status": "ERROR",
                "error": "deletion_index out of bounds"
            }), 404
        if category != lobby.categories[deletion_index]["name"]:
            return jsonify({
                "status": "ERROR",
                "error": "Category at index does not match"
            }), 404
        if socketID not in lobby.categories[deletion_index]["sockets"]:
            return jsonify({
                "status": "ERROR",
                "error": "Socket was not mapped to the category"
            }), 404

        categories = lobby.categories
        categories[deletion_index]["sockets"].remove(socketID)
        if not categories[deletion_index]["sockets"]:
            del categories[deletion_index]
        lr.update_categories(lobbyID=lobbyID, categories=categories)

        return jsonify({ "status": "SUCCESS" })
    
    @bp.route("/update-lobby-votes", methods=["POST"])
    def update_lobby_votes():
        lobbyID = request.json["lobbyID"]
        votes = request.json["votes"]
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        lr.update_votes(lobbyID=lobbyID, votes=votes)
        return jsonify({ "status": "SUCCESS" }), 200
    
    @bp.route("/socket-finished-swiping", methods=["POST"])
    def socket_finished_swiping():
        lobbyID = request.json["lobbyID"]
        socketID = request.json["socketID"]
        lobby = lr.get(lobbyID=lobbyID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        lr.update_sockets(lobbyID=lobbyID, socketID=socketID)
        isFinished = True
        for socket, finished in lobby.sockets.items():
            if socket != socketID and not finished:
                isFinished = False
                break
        return jsonify({ 
            "status": "SUCCESS",
            "lobbyFinished": isFinished
        }), 200
    
    @bp.route("/get-session-index", methods=["GET"])
    def get_session_index():
        session_index = session.get("session_index")
        if not session_index:
            return jsonify({ 
            "status": "ERROR",
            "error": "Session index does not exist"
        }), 404
        return jsonify({ 
            "status": "SUCCESS",
            "session_index": session_index
        }), 200

    @bp.route("/set-session-index", methods=["POST"])
    def set_session_index():
        session_index = request.json["session_index"]
        session["session_index"] = session_index
        return jsonify({ 
            "status": "SUCCESS",
            "session_index": session.get("session_index")
        }), 200
    
    @bp.route("/get-session-votes", methods=["GET"])
    def get_session_votes():
        session_votes = session.get("session_votes")
        if not session_votes:
            return jsonify({ 
            "status": "ERROR",
            "error": "Session votes does not exist"
        }), 404
        return jsonify({ 
            "status": "SUCCESS",
            "session_votes": session_votes
        }), 200

    @bp.route("/set-session-votes", methods=["POST"])
    def set_session_votes():
        session_votes = request.json["session_votes"]
        session["session_votes"] = session_votes
        return jsonify({ 
            "status": "SUCCESS",
            "session_votes": session.get("session_votes")
        }), 200

    return bp