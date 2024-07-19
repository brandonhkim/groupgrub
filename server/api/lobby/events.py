from flask import request
from flask_socketio import emit, leave_room
from __main__ import socketio

@socketio.on("USER_ONLINE")
def connected(userID):
    """event listener when client connects to the server"""
    print(f'{request.sid} has connected')
    emit("JOIN_SOCKET_ACCEPTED")

@socketio.on("USER_DISCONNECTED")
def disconnected():
    """event listener when client disconnects from the server"""
    print(f'{request.sid} has disconnected')

@socketio.on("ROOM_CLOSE_EARLY")
def disconnected(lobbyID):
    """event listener when client disconnects from the server"""
    leave_room(lobbyID)
    emit("LEAVE_ROOM_EARLY", to=lobbyID, broadcast=True, include_self=False)

@socketio.on("ROOM_PREFERENCES_CHANGE")
def room_preferences_change(lobbyID):
    """event listener for when host changes LobbyDropdown Component value"""
    emit("ROOM_PREFERENCES_UPDATE", to=lobbyID, broadcast=True, include_self=False)

@socketio.on("ROOM_CATEGORY_CHANGE")
def room_category_change(lobbyID):
    """event listener for when client is leaving a specific room"""
    emit("ROOM_CATEGORY_CHANGE", to=lobbyID, broadcast=True, include_self=False)

@socketio.on("ROOM_BUSINESSES_SEND")
def room_businesses_send(lobbyID):
    """event listener for when room's host receives yelp businesses"""
    emit("ROOM_BUSINESSES_RECEIVED", to=lobbyID, broadcast=True, include_self=False)

@socketio.on("LOBBY_FINISHED_SWIPING")
def lobby_finished_swiping(lobbyID):
    """event listener for when room's host receives yelp businesses"""
    emit("LOBBY_FINISHED_SWIPING", to=lobbyID, broadcast=True, include_self=False)

@socketio.on("LATE_FINISHED_SWIPING")
def late_finished_swiping(lobbyID):
    """event listener for when room's host receives yelp businesses"""
    emit("ROOM_VOTE_UPDATE", to=lobbyID, broadcast=True, include_self=False)

@socketio.on("LOBBY_NAVIGATION_UPDATE")
def lobby_navigation_update(lobbyID, path, message):
    """event listener for when room's host updates phase"""
    print("navigation update")
    emit("ROOM_PROGRESS_NAVIGATION", (path, message), to=lobbyID, broadcast=True)