import { useEffect, useState } from "react";
import { requestGetSessionID } from "../../utils/FetchRequests"
import { Navigate, useParams } from 'react-router-dom';

/** A more specific variation */
const ConditionalHomeRoute = (Component) => {
    return function ConditionSetup() {
        const { lobbyID } = useParams();
        const [isLoading, setIsLoading] = useState(true);
        const [doesPass, setDoesPass] = useState();
    
        useEffect(() => {
            const checkSessionID = async () => {
                const sessionID = await requestGetSessionID();
                setDoesPass(sessionID);
                setIsLoading(false);
            }
            checkSessionID();
        }, [lobbyID]);
            
        return ( 
            <div>
                {
                    /* ~ "If still fetching..." ~ */
                    isLoading ? <div></div> : 

                    /* ~ "If user has no session..." ~ */
                    !doesPass ? <Navigate to={`/`} replace state={{"errorMessage" : "Choose a nickname"}}/> :

                    /* ~ "If all conditions are met..." ~ */
                    <Component />
                }
            </div>

        )
                
    }
}

export default ConditionalHomeRoute;
