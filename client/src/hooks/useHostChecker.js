import { useEffect, useState } from "react";
import { getLobbyRequest, getSessionRequest } from "../utils/fetches";
import sessionInfoEquals from "../utils/sessionInfoEquals";

function useHostChecker(lobbyID) {
    const [isHost, setIsHost] = useState(false);
    useEffect(() => {
        const determineHost = async () => {
            const sessionInfo = await getSessionRequest("info");
            const lobbyHost = await getLobbyRequest(lobbyID, "host");
            setIsHost(sessionInfoEquals(lobbyHost, sessionInfo));
        }
        determineHost();
    }, [lobbyID]);

    return isHost;
}

export default useHostChecker;