import { useEffect, useState } from "react";
import { Navigate, useParams } from 'react-router-dom';
import { getLobbyRequest, getSessionRequest } from "../../utils/fetches";
import sessionInfoEquals from "../../utils/sessionInfoEquals";

const MAXIMUM_LOBBY_AGE = 900000 // 15 minutes

const ConditionalLobbyRoute = (Component, destination) => {
    return function CoinditionSetup() {
        const { lobbyID } = useParams();
        const [hasCookies, setHasCookies] = useState();
        const [isRoomOpen, setIsRoomOpen] = useState();
        const [isRoomExpired, setIsRoomExpired] = useState();
        const [doesPhaseMatch, setDoesPhaseMatch] = useState();
        const [lobbyPhase, setLobbyPhase] = useState();
        const [isLoading, setIsLoading] = useState(true);
    
        useEffect(() => {
            const fetchJoinable = async () => {
                const sessionInfo = await getSessionRequest("info");
                const sessions = await getLobbyRequest(lobbyID, "sessions");
                const joinable = await getLobbyRequest(lobbyID, "joinable");
                const timestamp = await getLobbyRequest(lobbyID, "timestamp");
                const alive = timestamp ? (new Date().getTime() - new Date(timestamp).getTime()) : MAXIMUM_LOBBY_AGE + 1;
                const phase = await getLobbyRequest(lobbyID, "phase");

                setHasCookies(sessionInfo);
                setIsRoomOpen(joinable || sessions.some(sessionInfoEquals.bind(sessionInfo)));
                setIsRoomExpired(!joinable && alive > MAXIMUM_LOBBY_AGE);
                setDoesPhaseMatch(destination === phase);
                setLobbyPhase(phase);
                setIsLoading(false);
            }
            fetchJoinable();
        }, [lobbyID]);

        return (
            <div>
                {
                    /* ~ "If still fetching..." ~ */
                    isLoading ? <div></div> : 

                    /* ~ "If sessionInfo was never set..." ~ */
                    !hasCookies ? <Navigate to={`/`} replace state={{"errorMessage" : "Please choose a nickname"}} /> :

                    /* ~ "If lobby is closed or expired" ~ */
                    isRoomExpired ? <Navigate to={`/`} replace state={{"errorMessage" : "Lobby does not exist"}} /> :

                    /* ~ "If lobby is unjoinable and session was not invited..." ~ */
                    !isRoomOpen ? <Navigate to={`/`} replace state={{"errorMessage" : "Lobby has already started"}} /> :

                    /* ~ "If lobby phase does not match client's..." ~ */
                    !doesPhaseMatch ? <Navigate to={`/lobby/${lobbyID}/${lobbyPhase}`} replace state={{"errorMessage" : `Rerouted to ${lobbyPhase}`}} /> :

                    /* ~ "If all conditions are met..." ~ */
                    <Component />
                }
            </div>
        )        
    }
}

export default ConditionalLobbyRoute