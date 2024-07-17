import { useEffect, useState } from 'react';

const BUFFER_TIME = 3000;   // 3s
const ROUTING_DELAY = 3; // 3s
function CountdownTimer({ initialTime, timeLimit, timeoutFunction, override=false, warningMessage=""}) {
    const [countdown, setCountdown] = useState(null);
    const [baseTime, setBaseTime] = useState(null);

    useEffect(() => {
        if (initialTime) { setBaseTime(new Date(initialTime).getTime()); }
    }, [initialTime])

    useEffect(() => {
    /*  Formula:
        timeLimit + (baseTime - currentTime) = bufferTime
        baseTime = bufferTime + currentTime - timeLimit   */
        if (override) {
            const newBaseTime = BUFFER_TIME + new Date().getTime() - timeLimit * 1000;
            if (newBaseTime < baseTime) {
                setBaseTime(BUFFER_TIME + new Date().getTime() - timeLimit * 1000);
            }
        }
    }, [override, timeLimit]);

    useEffect(() => {
        const interval = setInterval(() => {
            const current = new Date().getTime();
            const timeRemaining = timeLimit + Math.ceil((baseTime - current) / 1000);
            if (timeRemaining <= -1 * ROUTING_DELAY) {
                clearInterval(interval);
                timeoutFunction();
            }
            if (baseTime) { setCountdown(timeRemaining); }
        }, 200);
        return () => clearInterval(interval);
    }, [baseTime, timeLimit, timeoutFunction]);

    return (
      <div>
        <p>{baseTime && countdown && Math.max(0, countdown)}</p>
        <p>{(countdown < 0) && warningMessage}</p>
      </div>
    );
};

export default CountdownTimer;