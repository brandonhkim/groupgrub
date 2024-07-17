import { useCallback, useContext, useEffect, useRef, useState } from "react"
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { getDropdownValues } from "../../utils/DropdownValues";
import { SocketContext } from '../../context/socket';
import { 
    requestGetPreferences, 
    requestGetSessionID, 
    requestSetSessionIndex, 
    requestSetSessionVotes, 
    requestUpdateJoinable, 
    requestUpdatePhase, 
    requestUpdatePreferences,
    requestUpdateTimestamp } from "../../utils/FetchRequests";
import toast from 'react-hot-toast';
import PlacesLoader from "../../components/PlacesLoader/PlacesLoader";
import LocationSearchInput from "../../components/LocationSearchInput/LocationSearchInput";
import LobbyDropdown from "../../components/LobbyDropdown/LobbyDropdown"
import useHostChecker from "../../hooks/useHostChecker";

function SetupPage() {
    const socket = useContext(SocketContext);
    const navigate = useNavigate()
    const { lobbyID } = useParams();
    const { state = {} } = useLocation();
    const isHost = useHostChecker(lobbyID);
    const isFirstRender = useRef(true); // Used to prevent useEffect on first render

    /* ~ State variables + setters ~ */
    const [isLoading, setLoading] = useState(true);     // Tracks completion of Google Place JS Loader
    const [numResults, setNumResults] = useState(10);   // Query Parameters vvvv
    const [priceRange, setPriceRange] = useState("$");
    const [driveRadius, setDriveRadius] = useState(5);
    const [coordinates, setCoordinates] = useState({
        latitude: 91,
        longitude: 181,
        name: ""
    });

    /* ~ Setup for LobbyDropdown Components ~ */
    const dropdowns = getDropdownValues(
        numResults, 
        setNumResults, 
        priceRange, 
        setPriceRange, 
        driveRadius, 
        setDriveRadius);

    /* ~ Teardown for lobby's database entry + socket communication ~ */
    const lobbyEarlyTeardown = async () => {
        await requestUpdateTimestamp(lobbyID);
        await requestUpdateJoinable(lobbyID, false);
        socket.emit("ROOM_CLOSE_EARLY", lobbyID)
    }

    /* ~ Updates lobby's database entry w/ new Preferences + socket communication ~ */
    const updateLobbyPreferences = useCallback(async () => {
        await requestUpdatePreferences(lobbyID,  {
            "numResults": numResults,
            "priceRange": priceRange,
            "driveRadius": driveRadius,
            "coordinates": coordinates
        });
        socket.emit("ROOM_PREFERENCES_CHANGE", lobbyID);
    }, [lobbyID, socket, numResults, priceRange, driveRadius, coordinates]);

    /* ~ Socket event handlers ~ */
    const handleSocketAccepted = useCallback(async () => { 
        const sessionID = await requestGetSessionID();
        socket.emit("JOIN_ROOM_REQUEST", lobbyID, sessionID) 
    }, [lobbyID, socket]);
    const handleRoomCompletion = useCallback(async () => { 
        const sessionID = await requestGetSessionID();
        socket.emit("LEAVE_ROOM_REQUEST", lobbyID, sessionID)
        navigate(`/home`, { state: { "errorMessage": "Host closed the room"}, replace: true }); 
    }, [socket, navigate]);
    const handlePreferencesChange = useCallback(async () => {
        const updatedPreferences = await requestGetPreferences(lobbyID);
        if (!updatedPreferences) { console.log("Error: problem while receiving preferences") }  // TODO: catch error
        for (const [k, v] of Object.entries(updatedPreferences)) {
            if (k === "numResults") { setNumResults(v) }
            if (k === "priceRange") { setPriceRange(v) }
            if (k === "driveRadius") { setDriveRadius(v) }
            if (k === "coordinates") { setCoordinates(v) }
        }}, [lobbyID]);
    const handlePreferencesFinalized = useCallback(() => {
        navigate(`/lobby/${lobbyID}/categories`, { replace: true })}, [isHost, lobbyID, navigate]);

    /* ~ Button event handlers ~ */
    const readyBtnOnClick = () => {
        // Prepare and notify sockets to move to next phase
        const lobbyCategorySetup = async () => {
            await requestUpdateTimestamp(lobbyID);
            await requestUpdateJoinable(lobbyID, false);
            await requestUpdatePhase(lobbyID, "categories");
            socket.emit("LOBBY_NAVIGATION_UPDATE", lobbyID, `/lobby/${lobbyID}/categories`)
        }
        if (coordinates.name !== "") { lobbyCategorySetup(); }
        else { toast("Please provide a starting location!") }
    }
    const homeBtnOnClick = () => {
        if (isHost) { lobbyEarlyTeardown(); }           // Update DB info + communicate room to leave   
        socket.emit("LEAVE_ROOM_REQUEST", lobbyID);     // Leave room yourself
        navigate(`/`, { replace: true });
    }
    window.onpopstate = () => {
        if (isHost) { lobbyEarlyTeardown(); }           // On back button press, leave the room
      }

    /* ~ Setup + Teardown for socket communication ~ */
    useEffect(() => {
        // Emit to server a new connection
        socket.emit("USER_ONLINE", "userID"); 
    
        // Receive event from server, subscribe to prerequisite socket events
        socket.on("JOIN_SOCKET_ACCEPTED", handleSocketAccepted); 
        socket.on("LEAVE_ROOM_EARLY", handleRoomCompletion);
        socket.on("ROOM_PREFERENCES_UPDATE", handlePreferencesChange);
        socket.on("ROOM_PROGRESS_NAVIGATION", handlePreferencesFinalized);
    
        return () => {
            // Unbind all event handlers before component destruction
            socket.off("JOIN_SOCKET_ACCEPTED", handleSocketAccepted);
            socket.off("LEAVE_ROOM_EARLY", handleRoomCompletion);
            socket.off("ROOM_PREFERENCES_UPDATE", handlePreferencesChange);
            socket.off("ROOM_PROGRESS_NAVIGATION", handlePreferencesFinalized);  
        };
    }, [socket, handleSocketAccepted, handleRoomCompletion, handlePreferencesChange, handlePreferencesFinalized]);

    /* ~ On page load, receive lobby preferences from the database + reset session swiping data ~ */
    useEffect(() => { 
        if (state && "errorMessage" in state) { toast(state["errorMessage"]); }
        const resetSwipingData = async () => {
            await requestSetSessionIndex(null);     // Upon entering SwipingPate in the route,
            await requestSetSessionVotes(null);     // component will use null values to determine a new session
        }
        resetSwipingData();
        handlePreferencesChange(); 
    }, [handlePreferencesChange, state]);

    /* ~ On preference change, update database + socket communication ~ */
    useEffect(() => {
        if (isHost && !isFirstRender.current) { updateLobbyPreferences(); }
        isFirstRender.current = false;
    }, [isHost, updateLobbyPreferences]);

    return (
        <div>
            { <PlacesLoader setLoading={setLoading}/> }
            <div>
                { 
                    /* ~ "If the host + Places Loader completed..." ~ */
                    isHost && !isLoading && 
                    <LocationSearchInput
                        coordinates={coordinates}
                        setCoordinates={setCoordinates} /> 
                }
                { 
                    /* ~ "If not the host..." ~ */
                    !isHost && 
                    <input
                        disabled={true}
                        type="search"
                        value={coordinates["name"]} />
                }
            </div>

            {       /* ~ Note: Using dropdowns.map() causes unoptimal component rerendering ~ */      }
            <div>
                {   /* ~ Number of results dropdown... ~ */   }
                    <LobbyDropdown
                        key = { dropdowns[0].prefix }
                        modifiable= { isHost }
                        option = { numResults }
                        setOption = { dropdowns[0].handler }
                        heading = { dropdowns[0].heading }
                        prefix = { dropdowns[0].prefix }
                        minVal = { dropdowns[0].minRange }
                        maxVal = { dropdowns[0].maxRange }
                        increment = { dropdowns[0].incVal } />

                {   /* ~ Price range dropdown... ~ */   }
                <LobbyDropdown
                    key = { dropdowns[1].prefix }
                    modifiable= { isHost }
                    option = { priceRange }
                    setOption = { dropdowns[1].handler }
                    heading = { dropdowns[1].heading }
                    prefix = { dropdowns[1].prefix }
                    minVal = { dropdowns[1].minRange }
                    maxVal = { dropdowns[1].maxRange }
                    increment = { dropdowns[1].incVal } />

                {   /* ~ Drive radius dropdown... ~ */   }
                    <LobbyDropdown
                    key = { dropdowns[2].prefix }
                    modifiable= { isHost }
                    option = { driveRadius }
                    setOption = { dropdowns[2].handler }
                    heading = { dropdowns[2].heading }
                    prefix = { dropdowns[2].prefix }
                    minVal = { dropdowns[2].minRange }
                    maxVal = { dropdowns[2].maxRange }
                    increment = { dropdowns[2].incVal } />
                
            </div>
            <div>
                {   /* ~ Host determines completion of Lobby Phase ~ */ }
                { isHost && <button id="readyBtn" onClick={readyBtnOnClick}> Ready! </button> }
                <button id="homeBtn" onClick={homeBtnOnClick}>HomePage</button>
            </div>
        </div>
    );
}

export default SetupPage;