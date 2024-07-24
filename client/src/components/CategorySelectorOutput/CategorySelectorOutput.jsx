import { useContext, useEffect } from 'react';
import { SocketContext } from '../../context/socket';
import { updateLobbyCategory } from '../../utils/fetches';
import CategoryCard from '.././CategoryCard/CategoryCard';
import styles from './CategorySelectorOutput.module.css';


function CategorySelectorOutput({ myCategories, setMyCategories, allCategories, setAllCategories, lobbyID, sessionInfo }) {
    const socket = useContext(SocketContext);

    const deleteSocketCategory = async (index, categoryName) => {
        const { updated_categories=[], is_unused=false } = await updateLobbyCategory(lobbyID, sessionInfo, categoryName, false, index);
        socket.emit("ROOM_CATEGORY_CHANGE", lobbyID);
        const newCategories = new Set(myCategories)
        newCategories.delete(categoryName);
        setMyCategories(newCategories);

        if (is_unused) {

        }
        setAllCategories(updated_categories)
    }
    
    return (
        <div className={styles.container}>
            {
                allCategories && allCategories.map((obj, i) => {
                    const name = obj["category"]
                    const sessions = obj["sessions"]
                    let isMine = false;
                    for (const session of sessions) {
                        if (sessionInfo && session["nickname"] === sessionInfo["nickname"] && session["session_ID"] === sessionInfo["session_ID"]) {
                            isMine = true;
                            break;
                        }
                    }
                    return (
                        <CategoryCard 
                            key={name + 'Card'} 
                            lobbyID={lobbyID}
                            categoryName={name} 
                            categoryIsMine={isMine} 
                            deleteSocketCategory={deleteSocketCategory}
                            index={i} />
                    )
                })
            }
        </div>
    );
};

export default CategorySelectorOutput;