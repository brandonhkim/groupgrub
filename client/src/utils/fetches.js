
/* ~ Fetches related to lobby creation/teardown ~ */
export const createLobby = async (session_info) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "session_info": session_info })}
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/create-lobby`, requestOptions);
        const responseJSON = await responseData.json();
        return responseJSON["lobby_ID"];
    } catch (error) {
        console.log("error:", error);
    }
}

export const joinLobby = async (lobby_ID) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "lobby_ID": lobby_ID })}
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/join-lobby`, requestOptions)
        const responseJSON = await responseData.json();
        return responseJSON["lobby_ID"];
    } catch (error) {
        console.log("error:", error);
    }
}

export const deleteLobby = async (lobby_ID) => {
    try {
        const requestOptions = {
            method: 'DELETE',
            headers: { "Content-Type": "application/json" }}
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/delete-lobby?lobby-ID=${lobby_ID}`, requestOptions)
        const responseJSON = await responseData.json();
        return responseJSON["status"];
    } catch (error) {
        console.log("error:", error);
    }
}


/* ~ Fetches w/ more robust logic - Lobby category updates + session updates~ */
export const updateLobbyCategory = async (lobby_ID, session_info, category, do_add, deletion_index=-1) => {
    const action = do_add ? "add" : "remove";
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                "lobby_ID": lobby_ID,
                "session_info": session_info,
                "category": category,
                "deletion_index": deletion_index
            })}
        const categoryData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/${action}-lobby-category`, requestOptions);
        return await categoryData.json();
    } catch (error) {
        console.log("error:", error);
    }
}

export const updateLobbySession = async (lobby_ID, session_info) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                "lobby_ID": lobby_ID,
                "session_info": session_info
            })}
        const isFinishedData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/update-lobby-session`, requestOptions);
        const isFinishedJSON = await isFinishedData.json();
        return isFinishedJSON["is_lobby_finished"];
    } catch (error) {
        console.log("error:", error);
    }
}

export const setSessionInfo = async (nickname, socket_ID) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                "nickname": nickname, 
                "socket_ID": socket_ID }),
            credentials: 'include' 
        }
        const requestData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}session/set-session-info`, requestOptions);
        const requestJSON = await requestData.json();
        return requestJSON[`session_info`];
    } catch (error) {
        console.log("error:", error);
    }
}


/* ~ Basic fetching templates ~ */
export const getYelpRequest = async (coordinates, categories, priceRange, numResults, driveRadius) => {
    try {
        const requestOptions = {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            "geolocation": coordinates,
            "categories": categories,
            "price": priceRange,
            "num_results": numResults,
            "radius": driveRadius,
        })}
        const yelpBusinessesData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}selection/get-businesses`, requestOptions);
        const yelpBusinessesJSON = await yelpBusinessesData.json();
        return yelpBusinessesJSON["selections"]
    } catch (error) {
        console.log("error:", error);
    }
}

export const getLobbyRequest = async (lobby_ID, field) => {
    try {
        const requestOptions = {
            method: 'GET',
            headers: { "Content-Type": "application/json" }
        }
        const requestData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/get-lobby-${field}?lobby-ID=${lobby_ID}`, requestOptions);
        const requestJSON = await requestData.json()
        return requestJSON[field];
    } catch (error) {
        console.log(error);
    }
}

export const postLobbyRequest = async (lobby_ID, field, newData) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                "lobby_ID": lobby_ID, 
                [field]: newData })}
        const requestData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/update-lobby-${field}`, requestOptions);
        const requestJSON = await requestData.json();
        return requestJSON[`updated_${field}`];
    } catch (error) {
        console.log("error:", error);
    }
}

export const getSessionRequest = async (field) => {
    try {
        const requestOptions = {
            method: 'GET',
            headers: { "Content-Type": "application/json" },
            credentials: 'include'
        }
        const requestData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}session/get-session-${field}`, requestOptions);
        const requestJSON = await requestData.json()
        return requestJSON[`session_${field}`];
    } catch (error) {
        console.log(error);
    }
}

export const postSessionRequest = async (field, newData) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ [`session_${field}`] : newData }),
            credentials: 'include' 
        }
        const requestData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}session/set-session-${field}`, requestOptions);
        const requestJSON = await requestData.json();
        return requestJSON[`session_${field}`];
    } catch (error) {
        console.log("error:", error);
    }
}