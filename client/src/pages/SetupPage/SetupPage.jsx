import { useCallback, useContext, useEffect, useRef, useState } from "react"
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { getDropdownValues } from "../../utils/DropdownValues";
import { SocketContext } from '../../context/socket';
import { getLobbyRequest, getSessionRequest, postLobbyRequest, postSessionRequest } from "../../utils/fetches";

import toast from 'react-hot-toast';
import PlacesLoader from "../../components/PlacesLoader/PlacesLoader";
import LocationSearchInput from "../../components/LocationSearchInput/LocationSearchInput";
import LobbyDropdown from "../../components/LobbyDropdown/LobbyDropdown"
import useHostChecker from "../../hooks/useHostChecker";
import styles from "./SetupPage.module.css"

function SetupPage() {
    const socket = useContext(SocketContext);
    const navigate = useNavigate()
    const { lobbyID } = useParams();
    const { state = {} } = useLocation();
    const isHost = useHostChecker(lobbyID);
    const isFirstRender = useRef(true); // Used to prevent useEffect on first render

    /* ~ State variables + setters ~ */
    const [sessionInfo, setSessionInfo] = useState()
    const [isLoading, setLoading] = useState(true);     // Tracks completion of Google Place JS Loader
    const [sockets, setSockets] = useState([]);
    const [numResults, setNumResults] = useState(10);   // Query Parameters vvvv
    const [priceRange, setPriceRange] = useState("$");
    const [driveRadius, setDriveRadius] = useState(5);
    const [coordinates, setCoordinates] = useState({
        latitude: 91,
        longitude: 181,
        country: "",
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
        await postLobbyRequest(lobbyID, "timestamp", null);
        await postLobbyRequest(lobbyID, "joinable", false);
        socket.emit("ROOM_CLOSE_EARLY", lobbyID)
    }

    /* ~ Updates lobby's database entry w/ new Preferences + socket communication ~ */
    const updateLobbyPreferences = useCallback(async () => {
        await postLobbyRequest(lobbyID, "preferences", {
            "numResults": numResults,
            "priceRange": priceRange,
            "driveRadius": driveRadius,
            "coordinates": coordinates
        });
        socket.emit("ROOM_PREFERENCES_CHANGE", lobbyID);
    }, [lobbyID, socket, numResults, priceRange, driveRadius, coordinates]);

    /* ~ Socket event handlers ~ */
    const handleSocketAccepted = useCallback(async () => { 
        const sessionInfo = await getSessionRequest("info");
        setSessionInfo(sessionInfo);
        socket.emit("JOIN_ROOM_REQUEST", lobbyID, sessionInfo) 
    }, [lobbyID, socket]);
    const handleRoomCompletion = useCallback(async () => { 
        socket.emit("LEAVE_ROOM_REQUEST", lobbyID, sessionInfo)
        navigate(`/home`, { state: { "errorMessage": "Host closed the room"}, replace: true }); 
    }, [socket, navigate]);
    const handleSocketChange = useCallback(async () => {
        const sessionInformation = await getLobbyRequest(lobbyID, "sessions");
        for (const socketInfo in sessionInformation) {
            const [name, session_ID] = socketInfo;
        }
    }, []);
    const handlePreferencesChange = useCallback(async () => {
        const updatedPreferences = await getLobbyRequest(lobbyID, "preferences");
        if (!updatedPreferences) { console.log("Error: problem while receiving preferences") }  // TODO: catch error
        for (const [k, v] of Object.entries(updatedPreferences)) {
            if (k === "numResults") { setNumResults(v) }
            if (k === "priceRange") { setPriceRange(v) }
            if (k === "driveRadius") { setDriveRadius(v) }
            if (k === "coordinates") { setCoordinates(v) }
        }}, [lobbyID]);
    const handlePreferencesFinalized = useCallback((path, message = "") => { 
        let state = {};
        if (message !== "") {
            state = { state: { "errorMessage": message } };
        }
        navigate(path, message, { replace: true });
    }, [navigate]);

    /* ~ Button event handlers ~ */
    const readyBtnOnClick = () => {
        // Prepare and notify sockets to move to next phase
        const lobbyCategorySetup = async () => {
            await postLobbyRequest(lobbyID, "timestamp", null);
            await postLobbyRequest(lobbyID, "joinable", false);
            await postLobbyRequest(lobbyID, "phase", "categories");
            socket.emit("LOBBY_NAVIGATION_UPDATE", lobbyID, `/lobby/${lobbyID}/categories`, "")
        }
        if (coordinates.name !== "") { lobbyCategorySetup(); }
        else { toast("Please provide a starting location!") }
    }
    const homeBtnOnClick = () => {
        if (isHost) { lobbyEarlyTeardown(); }           // Update DB info + communicate room to leave   
        socket.emit("LEAVE_ROOM_REQUEST", lobbyID, sessionInfo);     // Leave room yourself
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
            await postSessionRequest("index", null);     // Upon entering SwipingPate in the route,
            await postSessionRequest("votes", null);     // component will use null values to determine a new session
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
            <div className={styles.container}>
                <div>

                </div>
                { 
                    /* ~ "If Places Loader is loaded..." ~ */
                    isHost && !isLoading && 
                    <LocationSearchInput
                        coordinates={coordinates}
                        setCoordinates={setCoordinates} 
                        isHost={isHost} /> 
                }
                

            {       /* ~ Note: Using dropdowns.map() causes unoptimal component rerendering ~ */      }
                <div className={styles.dropdownContainer}>
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
                <div className={styles.buttonContainer}>
                    {   /* ~ Host determines completion of Lobby Phase ~ */ }
                    <button className={styles.btn} id="homeBtn" onClick={homeBtnOnClick}>home</button>
                    { isHost && <button className={styles.btn} id="readyBtn" onClick={readyBtnOnClick}> ready </button> }
                </div>
            </div>
        </div>
    );
}

export default SetupPage;