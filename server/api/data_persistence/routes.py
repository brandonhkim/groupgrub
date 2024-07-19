from flask import Blueprint, request, jsonify, session

def create_blueprint()->Blueprint:
    bp = Blueprint('session', __name__)

    ''' ~ Session information related routes ~ '''
    @bp.route("/get-session-info", methods=["GET"])
    def get_nickname():
        session_info = session.get("session_info")
        if "session_info" not in session:
            return jsonify({ 
            "status": "ERROR",
            "error": "session_info is null"
        }), 400
        return jsonify({ 
            "status": "SUCESS",
            "session_info": session_info 
        })

    @bp.route("/set-session-info", methods=["POST"])
    def set_nickname():
        nickname = request.json["nickname"]
        socket_ID = request.json["socket_ID"]
        session["session_info"] = {
            "nickname": nickname,
            "session_ID": nickname + socket_ID,
        }
        session.modified = True
        return get_nickname()   # NOTE: check here first while debugging
    
    ''' ~ Session index + votes related routes (for SwipingPage persistence) ~ '''
    @bp.route("/get-session-index", methods=["GET"])
    def get_session_index():
        session_index = session.get("session_index")
        if "session_index" not in session:
            return jsonify({ 
            "status": "ERROR",
            "error": "Session index does not exist"
        }), 404
        return jsonify({ 
            "status": "SUCCESS",
            "session_index": session_index
        })

    @bp.route("/set-session-index", methods=["POST"])
    def set_session_index():
        session_index = request.json["session_index"]
        session["session_index"] = session_index
        session.modified = True
        return get_session_index()
    
    @bp.route("/get-session-votes", methods=["GET"])
    def get_session_votes():
        session_votes = session.get("session_votes")
        print("votes", session_votes)

        if "session_votes" not in session:
            return jsonify({ 
            "status": "ERROR",
            "error": "Session votes does not exist"
        }), 404
        return jsonify({ 
            "status": "SUCCESS",
            "session_votes": session_votes
        })

    @bp.route("/set-session-votes", methods=["POST"])
    def set_session_votes():
        session_votes = request.json["session_votes"]
        session["session_votes"] = session_votes
        session.modified = True
        return get_session_votes()
    
    return bp

