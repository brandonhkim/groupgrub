import { useCallback, useContext, useEffect, useState } from "react"
import { SocketContext } from '../../context/socket';
import { useLocation, useNavigate } from "react-router-dom"
import { requestCreateLobby, requestGetSessionID, requestJoinLobby, requestUpdatePhase } from "../../utils/FetchRequests";
import toast from 'react-hot-toast';

function HomePage() {
    const navigate = useNavigate()
    const { state = {} } = useLocation();
    const socket = useContext(SocketContext);
    const [lobbyCode, setLobbyCode] = useState('');

    /* ~ Socket event handlers ~ */
    const handleInviteAccepted = useCallback(() => {
        console.log("Accepted by socket")
    }, []);

    /* ~ Button event handlers ~ */
    const hostBtnOnClick = () => {
        const createLobby = async () => {
            const sessionID = await requestGetSessionID();
            const lobbyID = await requestCreateLobby(sessionID);
            await requestUpdatePhase(lobbyID, "setup");
            if (lobbyID) { navigate(`/lobby/${lobbyID}/setup`, { state: { isHost: true } }); }
        }
        createLobby();
    }
    const joinBtnOnClick = () => {
        const joinLobby = async () => {
            const lobbyID = await requestJoinLobby(lobbyCode);
            if (lobbyID) { navigate(`/lobby/${lobbyID}/setup`, { state: { isHost: false } }); }
        }
        joinLobby();
    }

    /* ~ Setup + Teardown for socket communication ~ */
    useEffect(() => {
        // Emit to server a new connection
        socket.emit("USER_ONLINE", "userID");   // NOTE: can integrate friends list in the future w/ userID

        // Receive event from server, subscribe to socket events
        socket.on("JOIN_SOCKET_ACCEPTED", handleInviteAccepted); 
    
        return () => {
            // Unbind all event handlers before component destruction
            socket.off("JOIN_SOCKET_ACCEPTED", handleInviteAccepted);
        };
    }, [socket, handleInviteAccepted]);

    /* ~ On page load, check for error message ~ */
    useEffect(() => { 
        if (state && "errorMessage" in state) { toast(state["errorMessage"]); }
    }, []);

    return (
        <div>
            <button id="hostBtn" onClick={hostBtnOnClick}> Host a new room </button>

            <div>
                <input
                    value={lobbyCode} 
                    onChange={e => setLobbyCode(e.target.value)}
                    placeholder="Lobby code" />
                <button id="joinBtn" onClick={joinBtnOnClick}> Join an existing room </button>
            </div>
        </div>
    );
}   

export default HomePage 

