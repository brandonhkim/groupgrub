import { useEffect, useState } from "react";
import { requestGetJoinable, requestGetPhase, requestGetSessionID, requestGetSockets, requestGetTimestamp } from "../../utils/FetchRequests"
import { Navigate, useParams } from 'react-router-dom';

/** A more specific variation */
const ConditionalLobbyRoute = (Component, phase) => {
    return function CoinditionSetup() {
        const { lobbyID } = useParams();
        const [sessionID, setSessionID] = useState()
        const [isLoading, setIsLoading] = useState(true);
        const [isJoinable, setIsJoinable] = useState();
        const [hasStarted, setHasStarted] = useState();
        const [DBPhase, setDBPhase] = useState();
    
        useEffect(() => {
            const fetchJoinable = async () => {
                const joinable = await requestGetJoinable(lobbyID);
                const newPhase = await requestGetPhase(lobbyID);
                const sessions = await requestGetSockets(lobbyID);
                const timestamp = await requestGetTimestamp(lobbyID);
                const ID = await requestGetSessionID();
                const alive = (new Date().getTime() - new Date(timestamp).getTime());
                console.log("ID", ID)
                setDBPhase(newPhase) 
                setIsJoinable(joinable || (sessions && ID in sessions) );
                setSessionID(ID);
                setHasStarted(alive <  900000);
                setIsLoading(false);

            }
            fetchJoinable();
        }, [lobbyID]);
        return (
            <div>
                {
                    /* ~ "If still fetching..." ~ */
                    isLoading ? <div></div> : 

                    /* ~ "If sessionID is null..." ~ */
                    !sessionID ? <Navigate to={`/`} replace state={{"errorMessage" : "Please choose a nickname"}} /> :

                    /* ~ "If lobby is unjoinable..." ~ */
                    !isJoinable ? <Navigate to={`/home`} replace state={{"errorMessage" : "Lobby does not exist"}} /> :

                    /* ~ "If lobby has already started" ~ */
                    !isJoinable && !hasStarted ? <Navigate to={`/home`} replace state={{"errorMessage" : "Lobby has already started"}} /> :

                    /* ~ "If client phase does not match server's..." ~ */
                    phase !== DBPhase ? <Navigate to={`/lobby/${lobbyID}/${DBPhase}`} replace state={{"errorMessage" : `Rerouted to ${DBPhase}`}} /> :

                    /* ~ "If all conditions are met..." ~ */
                    <Component />
                }
            </div>

        )
                
    }
}

export default ConditionalLobbyRoute