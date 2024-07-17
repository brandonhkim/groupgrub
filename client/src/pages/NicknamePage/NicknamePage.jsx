import { useCallback, useContext, useEffect, useState } from "react"
import { SocketContext } from '../../context/socket';
import { useLocation, useNavigate } from "react-router-dom"
import { requestSetSessionID } from "../../utils/FetchRequests";
import toast from 'react-hot-toast';

function NicknamePage() {
    const socket = useContext(SocketContext);
    const navigate = useNavigate()
    const { state = {} } = useLocation();
    const [nickname, setNickname] = useState('');

    /* ~ Socket event handlers ~ */
    const handleInviteAccepted = useCallback(() => {
        console.log("Accepted by socket")
    }, []);

    /* ~ Button event handlers ~ */
    const readyBtnOnClick = () => {
        const proceedToHome = async () => {
            const sessionID = await requestSetSessionID(nickname + socket.id);
            if (sessionID) { navigate(`/home`); }
        }
        if (3 <= nickname.length && nickname.length <= 12) {
            proceedToHome();
        }
        else {
            toast("Nicknames should be 3-12 characters long!")
        }
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
            <p>Nickname:</p>

            <div>
                <input
                    value={nickname} 
                    maxLength={12}
                    onChange={e => setNickname(e.target.value)}
                    placeholder="Nickname" />
                <button id="readyBtn" onClick={readyBtnOnClick}> Ready! </button>
            </div>
        </div>
    );
}   

export default NicknamePage 

