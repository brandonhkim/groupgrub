import { useCallback, useContext, useEffect, useState } from "react"
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { SocketContext } from '../../context/socket';
import { 
    requestGetCategories, 
    requestGetPreferences,
    requestGetSessionID,
    requestGetTimestamp, 
    requestUpdateBusinesses,
    requestUpdatePhase, 
    requestUpdateTimestamp, 
    requestYelpBusinesses } from "../../utils/FetchRequests";
import CategorySelectorInput from "../../components/CategorySelectorInput/CategorySelectorInput";
import CategorySelectorOutput from "../../components/CategorySelectorOutput/CategorySelectorOutput";
import CountdownTimer from "../../components/CountdownTimer/CountdownTimer";
import useHostChecker from "../../hooks/useHostChecker";
import toast from 'react-hot-toast';

function CategoriesPage() {
    const socket = useContext(SocketContext);
    const navigate = useNavigate()
    const { state } = useLocation();
    const { lobbyID } = useParams();
    const isHost = useHostChecker(lobbyID);

    /* ~ State variables + setters ~ */
    const [sessionID, setSessionID] = useState()
    const [timestamp, setTimestamp] = useState();
    const [myCategories, setMyCategories] = useState(new Set());    // Primarily used to limit # of categories per socket
    const [allCategories, setAllCategories] = useState([]);

    /* ~ Socket event handlers ~ */
    const handleSocketAccepted = useCallback(async () => { 
        const fetchSessionID = await requestGetSessionID();
        socket.emit("JOIN_ROOM_REQUEST", lobbyID, fetchSessionID) 
    }, [lobbyID, socket]);
    const handleCategoryOrganization = useCallback(async () => {
        const fetchSessionID = await requestGetSessionID();
        const categories = await requestGetCategories(lobbyID);

        const filteredCategories = new Set();
        for (let i=0; i<categories.length; i++) {
            const {name, sockets} = categories[i]
            if (sockets.includes(fetchSessionID)) {
                filteredCategories.add(name);
            }
        }
        setSessionID(fetchSessionID)
        setMyCategories(filteredCategories);
        setAllCategories(categories);
    }, [lobbyID]);
    const handleRoomCompletion =  useCallback(async () => { 
        const sessionID = await requestGetSessionID();
        socket.emit("LEAVE_ROOM_REQUEST", lobbyID, sessionID)
        navigate(`/home`, { state: { "errorMessage": "Host closed the room"}, replace: true }); 
    }, [socket, navigate]);
    const handleCategoryChange = useCallback(async () => {
        const categories = await requestGetCategories(lobbyID);
        setAllCategories(categories);
    }, [lobbyID]);
    const handleCategoriesFinalized = useCallback((path) => {
        navigate(path, { replace: true })}, [navigate]);

    /* ~ Setup + Teardown for socket communication ~ */
    useEffect(() => {
        // Emit to server a new connection
        socket.emit("USER_ONLINE", "userID"); 
    
        // Receive event from server, subscribe to prerequisite socket events
        socket.on("JOIN_SOCKET_ACCEPTED", handleSocketAccepted); 
        socket.on("JOIN_ROOM_ACCEPTED", handleCategoryOrganization);
        socket.on("LEAVE_ROOM_EARLY", handleRoomCompletion);
        socket.on("ROOM_CATEGORY_CHANGE", handleCategoryChange);
        socket.on("ROOM_PROGRESS_NAVIGATION", handleCategoriesFinalized);
        return () => {
            // Unbind event handler before component destruction
            socket.off("JOIN_SOCKET_ACCEPTED", handleSocketAccepted);
            socket.off("JOIN_ROOM_ACCEPTED", handleCategoryChange);
            socket.off("LEAVE_ROOM_EARLY", handleRoomCompletion);
            socket.off("ROOM_CATEGORY_CHANGE", handleCategoryChange);
            socket.off("ROOM_PROGRESS_NAVIGATION", handleCategoriesFinalized);
        };
    }, [socket, handleSocketAccepted, handleCategoryChange, handleRoomCompletion, handleCategoriesFinalized]);

    /* ~ On page load, synchronize timer in the lobby ~ */
    useEffect(() => {
        if (state && "errorMessage" in state) { toast(state["errorMessage"]); }
        const synchronizeTimestamp = async () => {
            let response = await requestGetTimestamp(lobbyID)
            if (!response) {
                console.log("ERROR: problem while getting lobby timestamp");
                return;
            }
            setTimestamp(response)
        }
        handleCategoryChange();
        synchronizeTimestamp();
    }, [lobbyID, state])

    /* ~ CountdownTimer completion handler ~ */
    const handleCategoriesComplete = useCallback(async () => {
        if (isHost) {
            await requestUpdateTimestamp(lobbyID);

            // First, fetch businesses from Yelp + update database w/ new data
            const preferences = await requestGetPreferences(lobbyID);   // Get necessary data first
            const categories = await requestGetCategories(lobbyID);
            if (!categories || !preferences) { console.log(`ERROR: problem while getting lobby ${!preferences ? "preferences" : "categories"}`); }
            let { coordinates, priceRange, numResults, driveRadius} = preferences;  // Deconstruct object
            const yelpSelection = await requestYelpBusinesses(coordinates, categories, priceRange, numResults, driveRadius);
            console.log(yelpSelection, numResults)
            // Then if there are enough businesses, update the database + communicate phase progression
            if (yelpSelection && yelpSelection.length === parseInt(numResults)) {
                await requestUpdateBusinesses(lobbyID, yelpSelection);
                await requestUpdatePhase(lobbyID, "swiping");
                socket.emit("LOBBY_NAVIGATION_UPDATE", lobbyID, `/lobby/${lobbyID}/swiping`)
            }
            // Otherwise, communicate phase regression and try again
            else {
                await requestUpdatePhase(lobbyID, "setup");
                socket.emit("LOBBY_NAVIGATION_UPDATE", lobbyID, `/lobby/${lobbyID}/setup`)
            }
        }
    }, [isHost])

    return (
        <div>
            <CategorySelectorOutput 
                sessionID={sessionID}
                allCategories={allCategories}
                setAllCategories={setAllCategories}
                lobbyID={lobbyID} />
            <CategorySelectorInput 
                sessionID={sessionID}
                myCategories={myCategories}
                setMyCategories={setMyCategories}
                allCategories={allCategories}
                setAllCategories={setAllCategories}
                lobbyID={lobbyID} />
            <CountdownTimer 
                initialTime={ timestamp } 
                timeLimit={10} 
                timeoutFunction={handleCategoriesComplete} 
                warningMessage={"Sending to swiping game..."} />
        </div>
    );
}

export default CategoriesPage


