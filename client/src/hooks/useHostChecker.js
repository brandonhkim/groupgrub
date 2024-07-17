import { useEffect, useState } from "react";
import {
    requestGetHost,
    requestGetSessionID
} from '../utils/FetchRequests';

function useHostChecker(lobbyID) {
    const [isHost, setIsHost] = useState(false);
    useEffect(() => {
        const determineHost = async () => {
            const sessionID = await requestGetSessionID();
            const lobbyHost = await requestGetHost(lobbyID);
            console.log("isHost:", sessionID, "===", lobbyHost);
            setIsHost(sessionID === lobbyHost);
        }
        determineHost();
    }, [lobbyID]);

    return isHost;
}

export default useHostChecker;