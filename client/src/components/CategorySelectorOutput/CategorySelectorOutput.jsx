import { useContext } from 'react';
import { SocketContext } from '../../context/socket';
import CategoryCard from '.././CategoryCard/CategoryCard';
import { requestRemoveCategory } from '../../utils/FetchRequests';

function CategorySelectorOutput({ allCategories, setAllCategories, lobbyID, sessionID }) {
    const socket = useContext(SocketContext);

    const removeFromAllCategories = (index) => {
        const newCategories = allCategories ? [...allCategories] : [];
        const removalIndex = newCategories[index]["sockets"].indexOf(sessionID);
        if (removalIndex > -1) { 
            newCategories[index]["sockets"].splice(removalIndex, 1); 
        }
        if (newCategories[index]["sockets"].length === 0) {
            newCategories.splice(index, 1);
        }
        return newCategories;
    }

    const deleteSocketCategory = (index, categoryName) => {
        const fetchRequest = async () => {
            await requestRemoveCategory(lobbyID, sessionID, categoryName, index);
            socket.emit("ROOM_CATEGORY_CHANGE", lobbyID);
        }
        fetchRequest()
        
        // Update state locally instead of fetching
        setAllCategories(removeFromAllCategories(index))
    }
    
    return (
        <div>
            {
                allCategories && allCategories.map((obj, i) => {
                    const name = obj["name"]
                    const sockets = obj["sockets"]
                    return (
                        <CategoryCard 
                            key={name + 'Card'} 
                            lobbyID={lobbyID}
                            categoryName={name} 
                            categoryIsMine={sockets && sockets.includes(sessionID)} 
                            deleteSocketCategory={deleteSocketCategory}
                            index={i} />
                    )
                })
            }
        </div>
    );
};

export default CategorySelectorOutput;