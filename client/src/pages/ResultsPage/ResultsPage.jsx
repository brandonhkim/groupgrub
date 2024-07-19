import { useCallback, useContext, useEffect, useState } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { SocketContext } from '../../context/socket';

import toast from 'react-hot-toast';
import Podium from '../../components/Podium/Podium';
import useHostChecker from '../../hooks/useHostChecker';
import { getLobbyRequest, getSessionRequest, postLobbyRequest } from '../../utils/fetches';

function ResultsPage() {
    const socket = useContext(SocketContext);
    const navigate = useNavigate();
    const { state } = useLocation();
    const { lobbyID } = useParams();
    const isHost = useHostChecker(lobbyID);

    /* ~ State variables + setters ~ */
    const [sessionInfo, setSessionInfo] = useState()
    const [isLoading, setIsLoading] = useState(true);
    const [businesses, setBusinesses] = useState([]);

    /* ~ Teardown for lobby's database entry + socket communication ~ */
    const lobbyEarlyTeardown = async () => {
        await postLobbyRequest(lobbyID, "timestamp", null);
        await postLobbyRequest(lobbyID, "joinable", false);
        socket.emit("ROOM_CLOSE_EARLY", lobbyID)
    }

    /* ~ Button event handlers ~ */
    const homeBtnOnClick = () => {
        if (isHost) { lobbyEarlyTeardown(); }           // Update DB info + communicate room to leave   
        socket.emit("LEAVE_ROOM_REQUEST", lobbyID);     // Leave room yourself
        navigate(`/`, { replace: true });
    }

    /* ~ Socket event handlers ~ */
    const handleSocketAccepted = useCallback(async () => { 
        const sessionInfo = await getSessionRequest("info");
        setSessionInfo(sessionInfo)
        socket.emit("JOIN_ROOM_REQUEST", lobbyID, sessionInfo) 
    }, [lobbyID, socket]);
    const handleRoomCompletion = useCallback(async () => { 
        socket.emit("LEAVE_ROOM_REQUEST", lobbyID, sessionInfo)
        navigate(`/`, { state: { "errorMessage": "Host closed the room"}, replace: true }); 
    }, [socket, navigate]);
    
    const handleLobbyVotes = useCallback(async () => {
        try {
            // First, fetch the lobby's compiled votes
            const votes = await getLobbyRequest(lobbyID, "votes");
            if (!votes) { console.log("ERROR: problem while getting lobby votes"); }
            const lobbyBusinesses = await getLobbyRequest(lobbyID, "businesses");
            if (!lobbyBusinesses) { console.log("ERROR: problem while getting lobby votes"); }
            
            // Then, process and organize the data into visual components
            const topBusinesses = lobbyBusinesses.map((business, ind) => [business, votes[ind]])
            const compareVotes = (a, b) => b[1] - a[1]; // descending order
            topBusinesses.sort(compareVotes)
            setBusinesses(topBusinesses)
            setIsLoading(false);
        } catch (error) {
            console.error(error);
        }
    }, [lobbyID]);

    /* ~ Setup + Teardown for socket communication ~ */
    useEffect(() => {
        // Emit to server a new connection
        socket.emit("USER_ONLINE", "userID"); 
    
        // Receive event from server, subscribe to prerequisite socket events
        socket.on("JOIN_SOCKET_ACCEPTED", handleSocketAccepted); 
        socket.on("ROOM_VOTE_UPDATE", handleLobbyVotes);
        socket.on("LEAVE_ROOM_EARLY", handleRoomCompletion);

        return () => {
            // Unbind event handler before component destruction
            socket.off("JOIN_SOCKET_ACCEPTED", handleSocketAccepted); 
            socket.off("ROOM_VOTE_UPDATE", handleLobbyVotes);
            socket.off("LEAVE_ROOM_EARLY", handleRoomCompletion);
        }
    }, [socket, handleSocketAccepted, handleLobbyVotes, handleRoomCompletion]);

    /* ~ On page load, organize lobby votes ~ */
    useEffect(() => {  
        if (state && "errorMessage" in state) { toast(state["errorMessage"]); }
        handleLobbyVotes(); 
    }, [handleLobbyVotes, state])
    
    return (
        <div>
            <div> 
                {
                    /* ~ "If data is finished processing..." ~ */
                    !isLoading &&
                    <Podium topBusinesses={businesses} />
                }
            </div>
            <button id="homeBtn" onClick={homeBtnOnClick}>HomePage</button>
            <div>
                {
                    /* ~ Iteratively render vote count... ~ */
                    <ol>
                        { businesses.map(element => 
                            <li key={`${element[0].name}${element[1]}`}>{element[0].name} {element[1]}</li>
                        )}
                    </ol>
                }
            </div>
        </div>
    );
}

export default ResultsPage;