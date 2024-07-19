import { useCallback, useContext, useEffect, useState } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { useSwipeable } from 'react-swipeable';
import { SocketContext } from '../../context/socket';

import BusinessCard from '../../components/BusinessCard/BusinessCard';
import CountdownTimer from '../../components/CountdownTimer/CountdownTimer';
import useHostChecker from '../../hooks/useHostChecker';
import toast from 'react-hot-toast';
import styles from './SwipingPage.module.css';
import { getLobbyRequest, getSessionRequest, postLobbyRequest, postSessionRequest, updateLobbySession } from '../../utils/fetches';

function SwipingPage() {
    const socket = useContext(SocketContext);
    const navigate = useNavigate();
    const { state } = useLocation();
    const { lobbyID } = useParams();
    const isHost = useHostChecker(lobbyID);

    /* ~ State variables + setters ~ */
    const [sessionInfo, setSessionInfo] = useState()
    const [isLoading, setIsLoading] = useState(true);
    const [isLobbyFinished, setIsLobbyFinished] = useState(false);
    const [timestamp, setTimestamp] = useState(new Date());     // Temporary Date obj for Countdown Timer initialization
    const [votes, setVotes] = useState([]);
    const [swipeIndex, setSwipeIndex] = useState(-1);
    const [businesses, setBusinesses] = useState([]);

    /* ~ State helper functions ~ */
    const incrementedVote = (i) => {
        const newVotes = [...votes];
        newVotes[i] += 1;
        return newVotes; }

    /* ~ Setup for gesture handlers ~ */
    const handlers = useSwipeable({
        onSwipedLeft: async () => { 
            await postSessionRequest("index", swipeIndex+1);
            setSwipeIndex(swipeIndex + 1);
        },   
        onSwipedRight: async () => {
            const newVotes = incrementedVote(swipeIndex);
            await postSessionRequest("index", swipeIndex+1);
            await postSessionRequest("votes", newVotes);
            setSwipeIndex(swipeIndex + 1);
            setVotes(newVotes);
        },
        swipeDuration: 500,
        preventScrollOnSwipe: true,
        trackMouse: true
    });

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
    const handleLobbyFinishedSwiping = useCallback(() => setIsLobbyFinished(true), [])
    const handleSwipingComplete = useCallback((path, message = "") => { 
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
        socket.on("LEAVE_ROOM_EARLY", handleRoomCompletion);
        socket.on("LOBBY_FINISHED_SWIPING", handleLobbyFinishedSwiping);
        socket.on("ROOM_PROGRESS_NAVIGATION", handleSwipingComplete);


        return () => {
            // Unbind event handler before component destruction
            socket.off("JOIN_SOCKET_ACCEPTED", handleSocketAccepted);
            socket.off("LEAVE_ROOM_EARLY", handleRoomCompletion);
            socket.off("LOBBY_FINISHED_SWIPING", handleLobbyFinishedSwiping);
            socket.off("ROOM_PROGRESS_NAVIGATION", handleSwipingComplete);   
        }
    }, [socket, handleSocketAccepted, handleRoomCompletion, handleLobbyFinishedSwiping, handleSwipingComplete]);

    /* ~ On page load, fetch businesses from database ~ */
    useEffect(() => {
        if (state && "errorMessage" in state) { toast(state["errorMessage"]); }
        // Get businesses from database
        const getBusinessesFromHost = async () => {
            const yelpSelection = await getLobbyRequest(lobbyID, "businesses");
            // True iff Host socket has fetched + populated the database w/ a valid Business selection
            if (yelpSelection && yelpSelection.length > 0) {
                const session_index = await getSessionRequest("index");   // Determine whether session data exists...
                const session_votes = await getSessionRequest("votes");
                const persisted_index = session_index ? session_index : 0;
                const persisted_votes = session_votes && session_votes.length > 0 ? session_votes : new Array(yelpSelection.length).fill(0)
                
                // ... then update state variables w/ default values or session data
                setBusinesses(yelpSelection);
                setSwipeIndex(persisted_index);
                setVotes(persisted_votes);
                setIsLoading(false);
        }}
        // Synchronize timer in the lobby
        const synchronizeTimestamp = async () => {
            let response = await getLobbyRequest(lobbyID, "timestamp");
            if (!response) {
                console.log("ERROR: problem while getting lobby timestamp");
                return;
            }
            setTimestamp(response);
        }
        getBusinessesFromHost();
        synchronizeTimestamp();
    }, [lobbyID, state]);

    /* ~ CountdownTimer completion handler ~ */
    const handlePhaseComplete = useCallback(async () => {
        // Update lobby votes if user did not finish within time limit
        if (swipeIndex < businesses.length) {
            await postLobbyRequest(lobbyID, "votes", votes);
            socket.emit("LATE_FINISHED_SWIPING", lobbyID)
        }
        if (isHost) {
            await postLobbyRequest(lobbyID, "timestamp", null);
            await postLobbyRequest(lobbyID, "phase", 'results')
            socket.emit("LOBBY_NAVIGATION_UPDATE", lobbyID, `/lobby/${lobbyID}/results`, "")
        }
    }, [isHost, lobbyID, socket, businesses, swipeIndex, votes]);

    // Update database w/ socket's completion + votes iff socket is finished swiping before timer termination
    useEffect(() => {
        if (swipeIndex !== -1 && swipeIndex === businesses.length) {
            const sendVotes = async () => {
                await postLobbyRequest(lobbyID, "votes", votes);
                const lobbyState = await updateLobbySession(lobbyID, sessionInfo);  
                if (lobbyState) {   // True iff this socket is the last to finish
                    socket.emit("LOBBY_FINISHED_SWIPING", lobbyID);
                    setIsLobbyFinished(lobbyState);
                }
            }
            sendVotes(); }
    }, [lobbyID, socket, businesses, swipeIndex, votes]);

    return (
        <div className={styles.container}> 
            <div>
                {   
                    /* ~ "If there are Businesses to be swiped through..." ~ */
                    !isLoading && swipeIndex < businesses.length && 
                    <div {...handlers} className={styles.draggableWindow}>
                        <BusinessCard {...businesses[swipeIndex]} />
                    </div>
                }
            </div>
            <div>
                {   
                    /* ~ "If socket finishes swiping early..." ~ */
                    swipeIndex >= businesses.length && 
                    <p>Waiting for everyone to finish!</p>
                }
            </div>
            <div>
                <CountdownTimer 
                    initialTime={timestamp}
                    timeLimit={10} 
                    timeoutFunction={handlePhaseComplete} 
                    warningMessage={"Sending to results page..."}
                    override={isLobbyFinished} />
            </div>
        </div>
    )
}

export default SwipingPage;