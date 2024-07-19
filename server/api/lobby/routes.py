from flask import Blueprint, request, jsonify, session
from datetime import datetime, timezone
from nanoid import generate
from decimal import Decimal
from ..repositories.lobby_repository import Lobby, LobbyRepository

TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
MAXIMUM_LOBBY_AGE = 1800    # 1800s = 30min


def isExpiredLobby(timestamp: str) -> bool:
    format = '%Y-%m-%dT%H:%M:%SZ'   # JavaScript UTC Date format
    start = datetime.strptime(timestamp, format)
    now = datetime.now(timezone.utc)
    delta = (now - start).total_seconds()
    return delta >= MAXIMUM_LOBBY_AGE

def create_blueprint(lr: LobbyRepository)->Blueprint:
    bp = Blueprint('lobby', __name__)

    ''' ~ Routes related to initial Lobby creation + lobby teardown ~ '''
    @bp.route("/create-lobby", methods=["POST"])
    def create_lobby():
        session_info = request.json["session_info"]
        if not session_info:
            return jsonify({
                "status": "ERROR",
                "error": "Invalid session_info provided" }), 400
        lobby = None
        for _ in range(10):
            lobby_ID = generate('23456789abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ', 4)
            lobby = lr.get(lobby_ID=lobby_ID)
            if not lobby or isExpiredLobby(lobby.timestamp):
                lobby = Lobby(lobby_ID=lobby_ID, host=session_info, timestamp=None)
                lr.add(**vars(lobby))
                return jsonify({
                    "status": "SUCCESS",
                    "lobby_ID": lobby_ID,
                }) 
        return jsonify({
            "status": "TIMEOUT",
            "error": "10 collisions occurred"
        }), 409

    @bp.route("/join-lobby", methods=["POST"])
    def join_lobby():
        lobby_ID = request.json["lobby_ID"]
        lobby = lr.get(lobby_ID=lobby_ID)
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
        # TODO: check length before joining
        return jsonify({
            "status": "SUCCESS",
            "lobby_ID": lobby_ID,
        }) 

    @bp.route("/delete-lobby", methods=["DELETE"])
    def delete_lobby():
        lobby_ID = request.args.get('lobby_ID')
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        lr.delete(lobby_ID=lobby_ID)
        return jsonify({ "status": "SUCCESS" })


    ''' ~ Host related routes  ~ '''
    @bp.route("/get-lobby-host", methods=["GET"])
    def get_lobby_host():
        lobby_ID = request.args.get('lobby-ID')
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "host": lobby.host
        }) 
    
    @bp.route("/update-lobby-host", methods=["POST"])
    def update_lobby_host():
        lobby_ID = request.json["lobby_ID"]
        host = request.json["host"]
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        lr.update_host(lobby_ID=lobby_ID, host=host)
        return jsonify({ 
            "status": "SUCCESS",
            "updated_host": host
        })
    

    ''' ~ Timestamp related routes ~ '''
    @bp.route("/get-lobby-timestamp", methods=["GET"])
    def get_lobby_timestamp():
        lobby_ID = request.args.get('lobby-ID')
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "timestamp": lobby.timestamp
        }) 
    
    @bp.route("/update-lobby-timestamp", methods=["POST"])
    def update_lobby_timestamp():
        lobby_ID = request.json["lobby_ID"]
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        timestamp = datetime.now(timezone.utc).strftime(TIME_FORMAT)
        lr.update_timestamp(lobby_ID=lobby_ID, timestamp=timestamp)
        return jsonify({ 
            "status": "SUCCESS",
            "updated_timestamp": timestamp
        })
    

    ''' ~ Joinable related routes ~ '''
    @bp.route("/get-lobby-joinable", methods=["GET"])
    def get_lobby_joinable():
        lobby_ID = request.args.get('lobby-ID')
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "joinable": lobby.joinable
        }) 
    
    @bp.route("/update-lobby-joinable", methods=["POST"])
    def update_lobby_joinable():
        lobby_ID = request.json["lobby_ID"]
        joinable = request.json["joinable"]
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        lr.update_joinable(lobby_ID=lobby_ID, joinable=joinable)
        return jsonify({ 
            "status": "SUCCESS",
            "updated_joinable": joinable
        })
    

    ''' ~ Phase related routes ~ '''
    @bp.route("/get-lobby-phase", methods=["GET"])
    def get_lobby_phase():
        lobby_ID = request.args.get('lobby-ID')
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "phase": lobby.phase
        }) 
    
    @bp.route("/update-lobby-phase", methods=["POST"])
    def update_lobby_phase():
        lobby_ID = request.json["lobby_ID"]
        phase = request.json["phase"]
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        lr.update_phase(lobby_ID=lobby_ID, phase=phase)
        return jsonify({ 
            "status": "SUCCESS",
            "updated_phase": phase
        })
    

    ''' ~ Sessions related routes ~ '''
    @bp.route("/get-lobby-sessions", methods=["GET"])
    def get_lobby_sessions():
        lobby_ID = request.args.get('lobby-ID')
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "sessions": lobby.sessions
        }) 
    
    # Update session finished attribute + returns is_lobby_finished if all sessions are finished
    @bp.route("/update-lobby-session", methods=["POST"])
    def update_lobby_session():
        lobby_ID = request.json["lobby_ID"]
        lobby = lr.get(lobby_ID=lobby_ID)
        session_info = request.json["session_info"]
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        if not session_info:
            return jsonify({
                "status": "ERROR",
                "error": "session_info is invalid"
            }), 400
        
        ind, is_lobby_finished = -1, True
        for i, cur in enumerate(lobby.sessions):
            if ind != -1 and not is_lobby_finished:
                break
            cur_session_info = cur["session_info"]
            cur_is_finished = cur["is_finished"]
            if cur_session_info["session_ID"] == session_info["session_ID"]:
                ind = i
            elif cur_session_info["session_ID"] != session_info["session_ID"] and not cur_is_finished:
                is_lobby_finished = False
        
        if ind != -1: lr.update_sessions(lobby_ID=lobby_ID, i=ind, new_session=session_info, is_finished=True)
        
        return jsonify({ 
            "status": "SUCCESS",
            "is_lobby_finished": is_lobby_finished
        })
    

    ''' ~ Preferences related routes ~ '''
    @bp.route("/get-lobby-preferences", methods=["GET"])
    def get_lobby_preferences():
        lobby_ID = request.args.get('lobby-ID')
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "preferences": lobby.preferences
        }) 
    
    @bp.route("/update-lobby-preferences", methods=["POST"])
    def update_lobby_preferences():
        lobby_ID = request.json["lobby_ID"]
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
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        lr.update_preferences(lobby_ID=lobby_ID, preferences=preferences)
        return jsonify({ 
            "status": "SUCCESS",
            "updated_preferences": preferences
        })


    ''' ~ Categories related routes ~ '''
    @bp.route("/get-lobby-categories", methods=["GET"])
    def get_lobby_categories():
        lobby_ID = request.args.get('lobby-ID')
        lobby = lr.get(lobby_ID=lobby_ID)
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
    
    @bp.route("/add-lobby-category", methods=["POST"])
    def add_lobby_categories():
        session_info = request.json["session_info"]
        lobby_ID = request.json["lobby_ID"]
        category = request.json["category"]
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "lobby does not exist"
            }), 404
        index, is_new = 0, True
        categories = lobby.categories
        for i, category_obj in enumerate(categories): # For now, at most O(30)
            if category_obj["category"] == category:
                category_obj["sessions"].append(session_info) 
                categories[i] = category_obj
                is_new = False
                break
            index += 1
        if is_new:
            categories.append({
                "category": category,
                "sessions": [session_info]
            })
        lr.update_categories(lobby_ID=lobby_ID, categories=categories)
        return jsonify({ 
            "status": "SUCCESS",
            "updated_categories": categories,
            "is_new": is_new
        })

    @bp.route("/remove-lobby-category", methods=["POST"])
    def remove_lobby_categories():
        session_info = request.json["session_info"]
        lobby_ID = request.json["lobby_ID"]
        deletion_category = request.json["category"]
        deletion_index = request.json["deletion_index"]
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        
        if lobby.categories[deletion_index]["category"] != deletion_category:
            for i, category in enumerate(lobby.categories):
                if category["category"] == deletion_category:
                    deletion_index = i
                    break
                
        if deletion_index == -1:
            return jsonify({
                "status": "ERROR",
                "error": "Category does not exist"
            }), 404
        if session_info not in lobby.categories[deletion_index]["sessions"]:
            return jsonify({
                "status": "ERROR",
                "error": "Session was not mapped to the category"
            }), 404

        categories = lobby.categories
        categories[deletion_index]["sessions"].remove(session_info)
        is_unused = not categories[deletion_index]["sessions"]
        if is_unused:  # Category no longer chosen by any sessions
            del categories[deletion_index]
        lr.update_categories(lobby_ID=lobby_ID, categories=categories)
        return jsonify({ 
            "status": "SUCCESS",
            "updated_categories": categories,
            "is_unused": is_unused
        })
    

    ''' ~ Businesses related routes ~ '''
    @bp.route("/get-lobby-businesses", methods=["GET"])
    def get_lobby_businesses():
        lobby_ID = request.args.get('lobby-ID')
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "businesses": lobby.businesses
        }) 
    
    @bp.route("/update-lobby-businesses", methods=["POST"])
    def update_lobby_businesses():
        lobby_ID = request.json["lobby_ID"]
        businesses = request.json["businesses"]
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        lr.update_businesses(lobby_ID=lobby_ID, businesses=businesses)
        return jsonify({ 
            "status": "SUCCESS",
            "updated_businesses": businesses
        })
    

    ''' ~ Votes related routes ~ '''
    @bp.route("/get-lobby-votes", methods=["GET"])
    def get_lobby_votes():
        lobby_ID = request.args.get('lobby-ID')
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "lobby does not exist"
            }), 404
        return jsonify({
            "status": "SUCCESS",
            "votes": lobby.votes
        }) 

    @bp.route("/update-lobby-votes", methods=["POST"])
    def update_lobby_votes():
        lobby_ID = request.json["lobby_ID"]
        votes = request.json["votes"]
        lobby = lr.get(lobby_ID=lobby_ID)
        if not lobby:
            return jsonify({
                "status": "ERROR",
                "error": "Lobby does not exist"
            }), 404
        lr.update_votes(lobby_ID=lobby_ID, votes=votes)
        return jsonify({ 
            "status": "SUCCESS",
            "updated_votes": votes 
        })

    return bp

