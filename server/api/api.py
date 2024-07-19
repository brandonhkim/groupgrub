from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_socketio import SocketIO, emit, join_room, leave_room
from .config import Config
from .repositories.lobby_repository import LobbyRepository
from .repositories.fusion_repository import FusionRepository

bcrypt = Bcrypt()
cors = CORS()
server_session = Session()
socketio = SocketIO()

# TODO: setup CORS on frontend

def create_app(lr: LobbyRepository=LobbyRepository(), fr: FusionRepository=FusionRepository()):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Instantiate objects w/ current Flask Application
    bcrypt.init_app(app)
    cors.init_app(app, supports_credentials=True)
    server_session.init_app(app)   # enables server-sided sessions for flask's "session" var

    socketio.init_app(app, cors_allowed_origins="*")

    # Import Socket.io events if not a test instance
    if type(lr) == LobbyRepository and type(fr) == FusionRepository:
        from .lobby import events

        @socketio.on("JOIN_ROOM_REQUEST")   # The following events require LobbyRepository, so I'm putting them here :c
        def enter_room(lobby_ID, session):
            """event listener for when client is joining a specific room"""
            join_room(lobby_ID)
            
            lr.add_session(lobby_ID=lobby_ID, session=session)
            emit("JOIN_ROOM_ACCEPTED", to=lobby_ID, broadcast=True)
            
            @socketio.on("disconnect")
            def disconnect():
                print("disconnect", session)
                lobby = lr.get(lobby_ID=lobby_ID)
                lr.remove_sessions(lobby_ID=lobby_ID, session=session)
                if session == lobby.host:
                    lr.update_joinable(lobby_ID=lobby_ID, joinable=False)
                    lr.update_host(lobby_ID=lobby_ID, host="")
                    emit("LEAVE_ROOM_EARLY", to=lobby_ID, broadcast=True)
                else:
                    emit("LEAVE_ROOM_ACCEPTED", to=lobby_ID, broadcast=True)


        @socketio.on("LEAVE_ROOM_REQUEST")
        def exit_room(lobby_ID, session):
            emit("LEAVE_ROOM_ACCEPTED", to=lobby_ID, broadcast=True)
            leave_room(lobby_ID)
            lr.remove_sessions(lobby_ID=lobby_ID, session=session)

    # Import route blueprints for necessary API calls
    from .data_persistence.routes import create_blueprint as session_bp
    app.register_blueprint(session_bp(), url_prefix='/session')

    from .selection.routes import create_blueprint as selection_bp
    app.register_blueprint(selection_bp(fr=fr), url_prefix='/selection')

    from .lobby.routes import create_blueprint as lobby_bp
    app.register_blueprint(lobby_bp(lr=lr), url_prefix='/lobby')

    return app

if __name__ == '__main__':
    socketio.run(create_app(), debug=True)

