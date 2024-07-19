import { useContext, useEffect, useState } from "react"
import { SocketContext } from '../../context/socket';
import { useLocation, useNavigate } from "react-router-dom"
import { createLobby, joinLobby, setSessionInfo, postLobbyRequest } from "../../utils/fetches";
import toast from 'react-hot-toast';
import styles from './HomePage.module.css'

function HomePage() {
    const navigate = useNavigate()
    const { state = {} } = useLocation();
    const socket = useContext(SocketContext);

    /* ~ State variables + setters ~ */
    const [nickname, setNickname] = useState('');
    const [lobbyCode, setLobbyCode] = useState('');

    /* ~ Button event handlers ~ */
    const hostBtnOnClick = () => {
        const setupLobby = async () => {
            const sessionInfo = await setSessionInfo(nickname, socket.id);
            const lobbyID = await createLobby(sessionInfo);
            console.log(lobbyID)
            await postLobbyRequest(lobbyID, "phase", "setup");
            if (lobbyID) { navigate(`/lobby/${lobbyID}/setup`, { state: { isHost: true } }); }
        }
        if (3 <= nickname.length && nickname.length <= 12) { setupLobby(); }
        else if (nickname.length === 0) { toast("Please provide a nickname!"); }
        else { toast("Nicknames should be 3-12 characters long!") }
    }
    const joinBtnOnClick = () => {
        const setupLobby = async () => {
            const sessionInfo = await setSessionInfo(nickname, socket.id);
            const lobbyID = await joinLobby(lobbyCode);
            if (lobbyID) { navigate(`/lobby/${lobbyID}/setup`, { state: { isHost: false } }); }
        }
        if (3 <= nickname.length && nickname.length <= 12) { setupLobby(); }
        else if (nickname.length === 0) { toast("Please provide a nickname!"); }
        else { toast("Nicknames should be 3-12 characters long!") }
    }

    /* ~ Setup + Teardown for socket communication ~ */
    useEffect(() => {
        // Emit to server a new connection
        socket.emit("USER_ONLINE", "userID");   // NOTE: can integrate friends list in the future w/ userID
    }, [socket]);

    /* ~ On page load, check for error message ~ */
    useEffect(() => { 
        if (state && "errorMessage" in state) { toast(state["errorMessage"]); }
    }, []);

    return (
        <div className={styles.container}>
            <div className={styles.titleContainer}>
                <h1 className={styles.intro}>Welcome to</h1>
                <h1 className={styles.logo}>GroupGrub</h1>
            </div>
            <div className={styles.inputContainer}>
                <input
                        className={styles.nameInput}
                        value={nickname} 
                        maxLength={12}
                        onChange={e => setNickname(e.target.value)}
                        placeholder="nickname" />

                <button className={styles.hostBtn} id="hostBtn" onClick={hostBtnOnClick}> host a room </button>

                <input
                    className={styles.guestInput}
                    value={lobbyCode} 
                    onChange={e => setLobbyCode(e.target.value)}
                    placeholder="join a room" />
                <button
                    className={styles.guestBtn}
                    styles={{display: lobbyCode.length > 0 ? "block" : "none"}}
                    id="joinBtn" 
                    onClick={joinBtnOnClick}> join </button>
            </div>
    
        </div>
    );
}   

export default HomePage 

