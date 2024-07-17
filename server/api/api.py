from flask import Flask, request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, leave_room
from .config import Config
from .repositories.user_repository import UserRepository
from .repositories.lobby_repository import LobbyRepository
from .repositories.fusion_repository import FusionRepository

bcrypt = Bcrypt()
cors = CORS()
server_session = Session()
socketio = SocketIO()

# TODO: setup CORS on frontend

def create_app(ur: UserRepository=UserRepository(), lr: LobbyRepository=LobbyRepository(), fr: FusionRepository=FusionRepository()):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Instantiate objects w/ current Flask Application
    bcrypt.init_app(app)
    cors.init_app(app, supports_credentials=True)
    server_session.init_app(app)   # enables server-sided sessions for flask's "session" var

    socketio.init_app(app, cors_allowed_origins="*")

    # Import Socket.io events if not a test instance
    if type(ur) == UserRepository and type(fr) == FusionRepository:
        from .lobby import events

        @socketio.on("JOIN_ROOM_REQUEST")   # The following events require LobbyRepository, so I'm putting them here :c
        def enter_room(lobbyID, sessionID):
            """event listener for when client is joining a specific room"""
            join_room(lobbyID)
            lr.add_sockets(lobbyID=lobbyID, socketID=sessionID)
            emit("JOIN_ROOM_ACCEPTED", to=lobbyID, broadcast=True)
            
            @socketio.on("disconnect")
            def disconnect():
                print(request.sid, "disconnected")
                lobby = lr.get(lobbyID=lobbyID)
                if request.sid == lobby.host:
                    lr.update_joinable(lobbyID=lobbyID, joinable=False)
                    lr.update_host(lobbyID=lobbyID, host="")
                    emit("LEAVE_ROOM_EARLY", to=lobbyID, broadcast=True)

        @socketio.on("LEAVE_ROOM_REQUEST")
        def exit_room(lobbyID, sesionID):
            print(request.sid, "leaving room")
            leave_room(lobbyID)
            lr.remove_sockets(lobbyID=lobbyID, socketID=sesionID)

    # Import route blueprints for necessary API calls
    from .auth.routes import create_blueprint as auth_bp
    app.register_blueprint(auth_bp(ur=ur), url_prefix='/auth')

    from .selection.routes import create_blueprint as selection_bp
    app.register_blueprint(selection_bp(fr=fr), url_prefix='/selection')

    from .lobby.routes import create_blueprint as lobby_bp
    app.register_blueprint(lobby_bp(lr=lr), url_prefix='/lobby')

    return app

if __name__ == '__main__':
    socketio.run(create_app(), debug=True)

