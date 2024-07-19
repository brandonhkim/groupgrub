import { useCallback, useContext, useEffect, useState } from "react"
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { SocketContext } from '../../context/socket';
import { getLobbyRequest, getSessionRequest, getYelpRequest, postLobbyRequest } from "../../utils/fetches";
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
    const [sessionInfo, setSessioninfo] = useState()
    const [timestamp, setTimestamp] = useState();
    const [myCategories, setMyCategories] = useState(new Set());    // Primarily used to limit # of categories per socket
    const [allCategories, setAllCategories] = useState([]);
    const [coordinates, setCoordinates] = useState();

    /* ~ Socket event handlers ~ */
    const handleSocketAccepted = useCallback(async () => { 
        const sessionInfo = await getSessionRequest("info");
        setSessioninfo(sessionInfo);
        socket.emit("JOIN_ROOM_REQUEST", lobbyID, sessionInfo) 
    }, [lobbyID, socket]);
    const handleCategoryOrganization = useCallback(async () => {
        const categories = await getLobbyRequest(lobbyID, "categories");
        const filteredCategories = new Set();
        for (let i=0; i<categories.length; i++) {
            const { name, sockets } = categories[i]
            if (sockets.includes(sessionInfo)) {
                filteredCategories.add(name);
            }
        }
        setMyCategories(filteredCategories);
        setAllCategories(categories);
    }, [lobbyID]);
    const handleRoomCompletion =  useCallback(async () => { 
        socket.emit("LEAVE_ROOM_REQUEST", lobbyID, sessionInfo)
        navigate(`/home`, { state: { "errorMessage": "Host closed the room"}, replace: true }); 
    }, [socket, navigate]);
    const handleCategoryChange = useCallback(async () => {
        const categories = await getLobbyRequest(lobbyID, "categories");
        setAllCategories(categories);
    }, [lobbyID]);
    const handleCategoriesFinalized = useCallback((path, message = "") => { 
        let state = {};
        if (message !== "") {
            state = { state: { "errorMessage": message } };
        }
        navigate(path, message, { replace: true });
    }, [navigate]);

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

    /* ~ On page load, synchronize timer in the lobby + populate lobby's categories ~ */
    useEffect(() => {
        if (state && "errorMessage" in state) { toast(state["errorMessage"]); }
        const synchronizeTimestamp = async () => {
            let response = await getLobbyRequest(lobbyID, "timestamp");
            if (!response) {
                console.log("ERROR: problem while getting lobby timestamp");
                return;
            }
            setTimestamp(response)
        }
        const setupCoordinates = async () => {
            const { coordinates } = await getLobbyRequest(lobbyID, "preferences");
            setCoordinates(coordinates);
        }
        setupCoordinates();
        handleCategoryChange();
        synchronizeTimestamp();
    }, [lobbyID, state])

    /* ~ CountdownTimer completion handler ~ */
    const handleCategoriesComplete = useCallback(async () => {
        if (isHost) {
            await postLobbyRequest(lobbyID, "timestamp", null);

            // First, fetch businesses from Yelp + update database w/ new data
            const preferences = await getLobbyRequest(lobbyID, "preferences");   // Get necessary data first
            const categories = await getLobbyRequest(lobbyID, "categories");
            if (!categories || !preferences) { console.log(`ERROR: problem while getting lobby ${!preferences ? "preferences" : "categories"}`); }
            const { coordinates, priceRange, numResults, driveRadius} = preferences;  // Deconstruct object
            const yelpSelection = await getYelpRequest(coordinates, categories, priceRange, numResults, driveRadius);
            console.log(yelpSelection, "RESULTS")

            // Then if there are enough businesses, update the database + communicate phase progression
            if (yelpSelection && yelpSelection.length === parseInt(numResults)) {
                await postLobbyRequest(lobbyID, "businesses", yelpSelection);
                await postLobbyRequest(lobbyID, "phase", "swiping");
                socket.emit("LOBBY_NAVIGATION_UPDATE", lobbyID, `/lobby/${lobbyID}/swiping`, "")
            }
            // Otherwise, communicate phase regression and try again
            else {
                await postLobbyRequest(lobbyID, "phase", "setup");
                socket.emit("LOBBY_NAVIGATION_UPDATE", lobbyID, `/lobby/${lobbyID}/setup`, "Not enough results, please adjust parameters")
            }
        }
    }, [isHost])

    useEffect(() => {
        console.log("my categories", myCategories)
    }, [myCategories])

    return (
        <div>
            <CategorySelectorOutput 
                myCategories={myCategories}
                setMyCategories={setMyCategories}
                sessionInfo={sessionInfo}
                allCategories={allCategories}
                setAllCategories={setAllCategories}
                lobbyID={lobbyID} />
            <CategorySelectorInput 
                lobbyID={lobbyID}
                sessionInfo={sessionInfo}
                coordinates={coordinates}
                myCategories={myCategories}
                setMyCategories={setMyCategories}
                setAllCategories={setAllCategories} />
            <CountdownTimer 
                initialTime={ timestamp } 
                timeLimit={10} 
                timeoutFunction={handleCategoriesComplete} 
                warningMessage={"Sending to swiping game..."} />
        </div>
    );
}

export default CategoriesPage


