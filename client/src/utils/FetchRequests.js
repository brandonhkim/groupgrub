// TODO: check for non-200 codes

import { socket } from "../context/socket";

export const requestCreateLobby = async (socketID) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "socketID": socketID })}
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/create-lobby`, requestOptions);
        const responseJSON = await responseData.json();
        const lobbyID = responseJSON["lobbyID"];
        return lobbyID;
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestJoinLobby = async (lobbyCode) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "lobbyID": lobbyCode })}
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/join-lobby`, requestOptions)
        const responseJSON = await responseData.json();
        const lobbyID = responseJSON["lobbyID"];
        return lobbyID ? lobbyID : null;
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestYelpBusinesses = async (coordinates, categories, priceRange, numResults, driveRadius) => {
    console.log(coordinates, categories, priceRange, numResults, driveRadius)
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

export const requestGetCategories = async (lobbyID) => {
    try {
        const requestOptions = {
            method: 'GET',
            headers: { "Content-Type": "application/json" }
        }
        const categoriesData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/get-lobby-categories?lobbyID=${lobbyID}`, requestOptions)
        const categoriesJSON = await categoriesData.json();
        return categoriesJSON["categories"];
    } catch (error) {
        console.log(error);
    }
}

export const requestGetTimestamp = async (lobbyID) => {
    try {
        const requestOptions = {
            method: 'GET',
            headers: { "Content-Type": "application/json" }
        }
        const timestampData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/get-lobby-timestamp?lobbyID=${lobbyID}`, requestOptions);
        const timestampJSON = await timestampData.json()
        return timestampJSON["timestamp"];
    } catch (error) {
        console.log(error);
    }
}

export const requestGetBusinesses = async (lobbyID) => {
    try {
        const requestOptions = {
            method: 'GET',
            headers: { "Content-Type": "application/json" }
        }
        const businessesData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/get-lobby-businesses?lobbyID=${lobbyID}`, requestOptions);
        const businessesJSON = await businessesData.json()
        return businessesJSON["businesses"];
    } catch (error) {
        console.log(error);
    }
}

export const requestGetVotes = async (lobbyID) => {
    try {
        const requestOptions = {
            method: 'GET',
            headers: { "Content-Type": "application/json" }
        }
        const votesData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/get-lobby-votes?lobbyID=${lobbyID}`, requestOptions);
        const votesJSON = await votesData.json()
        return votesJSON["votes"];
    } catch (error) {
        console.log(error);
    }
}

export const requestGetSockets = async (lobbyID) => {
    try {
        const requestOptions = {
            method: 'GET',
            headers: { "Content-Type": "application/json" }
        }
        const socketsData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/get-lobby-sockets?lobbyID=${lobbyID}`, requestOptions);
        const socketsJSON = await socketsData.json()
        console.log("SOCKETS", socketsJSON)
        return socketsJSON["sockets"];
    } catch (error) {
        console.log(error);
    }
}

export const requestGetHost = async (lobbyID) => {
    try {
        const requestOptions = {
            method: 'GET',
            headers: { "Content-Type": "application/json" }
        }
        const hostData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/get-lobby-host?lobbyID=${lobbyID}`, requestOptions);
        const hostJSON = await hostData.json()
        return hostJSON["host"];
    } catch (error) {
        console.log(error);
    }
}

export const requestGetPhase = async (lobbyID) => {
    try {
        const requestOptions = {
            method: 'GET',
            headers: { "Content-Type": "application/json" }
        }
        const phaseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/get-lobby-phase?lobbyID=${lobbyID}`, requestOptions);
        const phaseJSON = await phaseData.json()
        return phaseJSON["phase"];
    } catch (error) {
        console.log(error);
    }
}

export const requestGetPreferences = async (lobbyID) => {
    try {
        const requestOptions = {
            method: 'GET',
            headers: { "Content-Type": "application/json" }
        }
        const preferencesData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/get-lobby-preferences?lobbyID=${lobbyID}`, requestOptions);
        const preferencesJSON = await preferencesData.json()
        return preferencesJSON["preferences"];
    } catch (error) {
        console.log(error);
    }
}

export const requestGetJoinable = async (lobbyID) => {
    try {
        const requestOptions = {
            method: 'GET',
            headers: { "Content-Type": "application/json" }
        }
        const joinableData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/get-lobby-joinable?lobbyID=${lobbyID}`, requestOptions);
        const joinableJSON = await joinableData.json()
        return joinableJSON["joinable"];
    } catch (error) {
        console.log(error);
    }
}

export const requestUpdateSockets = async (lobbyID, socketID) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(
                { 
                    "lobbyID": lobbyID, 
                    "socketID": socketID, 
            })}
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/socket-finished-swiping`, requestOptions);
        const responseJSON = await responseData.json();
        return responseJSON["lobbyFinished"];
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestAddCategory = async (lobbyID, socketID, categoryName) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(
                { 
                    "lobbyID": lobbyID, 
                    "socketID": socketID, 
                    "category": categoryName
            })}
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/add-lobby-category`, requestOptions);
        const responseJSON = await responseData.json();
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestRemoveCategory = async (lobbyID, socketID, categoryName, deletionIndex, thenFunction) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                "lobbyID": lobbyID,
                "socketID": socketID,
                "category": categoryName,
                "deletion_index": deletionIndex
            })}
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/remove-lobby-category`, requestOptions);
        const responseJSON = await responseData.json();
        thenFunction();
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestUpdateTimestamp = async (lobbyID) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "lobbyID": lobbyID })
        }
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/update-lobby-timestamp`, requestOptions);
        const responseJSON = await responseData.json();
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestUpdatePhase = async (lobbyID, phase) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                "lobbyID": lobbyID,
                "phase": phase
            })
        }
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/update-lobby-phase`, requestOptions);
        const responseJSON = await responseData.json();
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestUpdateJoinable = async (lobbyID, joinable) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                "lobbyID": lobbyID,
                "joinable": joinable
            })
        }
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/update-lobby-joinable`, requestOptions);
        const responseJSON = await responseData.json();
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestUpdateBusinesses = async (lobbyID, businesses) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                "lobbyID": lobbyID,
                "businesses": businesses
            })
        }
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/update-lobby-businesses`, requestOptions)
        const responseJSON = await responseData.json();
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestUpdateVotes = async (lobbyID, votes) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                "lobbyID": lobbyID,
                "votes": votes
            })
        }
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/update-lobby-votes`, requestOptions)
        const responseJSON = await responseData.json();
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestUpdatePreferences = async (lobbyID, preferences) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                "lobbyID": lobbyID,
                "preferences": preferences
            })
        }
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/update-lobby-preferences`, requestOptions)
        const responseJSON = await responseData.json();
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestSetSessionID = async (socketID) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "socketID": socketID }),
            credentials: 'include'
        }
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}auth/set-session-ID`, requestOptions)
        const responseJSON = await responseData.json();
        return responseJSON["session_id"]
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestGetSessionID = async () => {
    try {
        const requestOptions = {
            method: 'GET',
            headers: { "Content-Type": "application/json" },
            credentials: 'include'
        }
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}auth/get-session-ID`, requestOptions)
        const responseJSON = await responseData.json();
        return responseJSON["session_id"]
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestSetSessionIndex = async (sessionIndex) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "session_index": sessionIndex }),
            credentials: 'include'
        }
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/set-session-index`, requestOptions)
        const responseJSON = await responseData.json();
        return responseJSON["session_index"]
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestGetSessionIndex = async () => {
    try {
        const requestOptions = {
            method: 'GET',
            headers: { "Content-Type": "application/json" },
            credentials: 'include'
        }
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/get-session-index`, requestOptions)
        const responseJSON = await responseData.json();
        return responseJSON["session_index"]
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestSetSessionVotes = async (sessionVotes) => {
    try {
        const requestOptions = {
            method: 'POST',
            headers: { 
                "Content-Type": "application/json" },
            body: JSON.stringify({ 
                "session_votes": sessionVotes
            }),
            credentials: 'include'
        }
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/set-session-votes`, requestOptions)
        const responseJSON = await responseData.json();
        return responseJSON["session_votes"]
    } catch (error) {
        console.log("error:", error);
    }
}

export const requestGetSessionVotes = async () => {
    try {
        const requestOptions = {
            method: 'GET',
            headers: { "Content-Type": "application/json" },
            credentials: 'include'
        }
        const responseData = await fetch(`${process.env.REACT_APP_SOCKET_ENDPOINT}lobby/get-session-votes`, requestOptions)
        const responseJSON = await responseData.json();
        return responseJSON["session_votes"]
    } catch (error) {
        console.log("error:", error);
    }
}