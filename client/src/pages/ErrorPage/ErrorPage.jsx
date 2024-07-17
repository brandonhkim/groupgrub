import { useNavigate } from "react-router-dom";

function ErrorPage() {
    const navigate = useNavigate();
    const homeBtnOnClick = () => {
        navigate(`/`, { replace: true });
    }

    return (
        <div>
            <p>404: Either the room or page you were trying to access does not exist!</p>
            <button id="homeBtn" onClick={homeBtnOnClick}>HomePage</button>
        </div>
    );
}

export default ErrorPage;