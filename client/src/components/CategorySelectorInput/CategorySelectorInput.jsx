import { useContext, useState, useRef } from 'react';
import { useCombobox } from 'downshift';
import { SocketContext } from '../../context/socket';
import { updateLobbyCategory } from '../../utils/fetches';
import CategoryTree from '../../utils/CategoryTree'

function CategorySelectorInput({ lobbyID, sessionInfo, coordinates, myCategories, setMyCategories, setAllCategories }) {
    const socket = useContext(SocketContext);
    const categoryTree = useRef(new CategoryTree())
    const [showSuggestions, setShowSuggestions] = useState(true)
    const [suggestions, setSuggestions] = useState([]);
    const [selectedItem, setSelectedItem] = useState({
        name: "",
        code: ""
    })
    
    const handleSelect = async (item) => {
        if(myCategories[item.name]) {
            return
        }
        const { updated_categories=[], is_new=false } = await updateLobbyCategory(lobbyID, sessionInfo, item.name, true);
        socket.emit("ROOM_CATEGORY_CHANGE", lobbyID);

        if (is_new) {
            // TODO: make 2 socket events - ROOM_CATEGORY_ADDITION DELETION, animate if new addition or deletion
        }

        // Update state locally instead of fetching AGAIN from backend
        setAllCategories(updated_categories)
        setMyCategories(myCategories.union(new Set([item.name])))
        setShowSuggestions(false);    
        setSelectedItem({
            name: item.name,
            code: item.code
        })        
    }
    
    // WAI-ARIA powered by Downshift
    const {
        getInputProps,
        getItemProps,
        getMenuProps,
    } = useCombobox({   // NOTE: Downshift docs reports breaking changes in past 2 versions (may need code migration in the future)
        items: suggestions,
        onInputValueChange: ({ inputValue }) => {
            // If User clears the search bar, reset state
            if (inputValue === '' || !showSuggestions) {  
                setShowSuggestions(true);        
                setSuggestions([]);
                return;
            }
    
            // Get autocomplete suggestions and update state
            const country = "country" in coordinates ? coordinates["country"] : "US"
            const matches = categoryTree.current.beginsWith(country, inputValue);
            setSuggestions(matches);
            
        },
        selectedItem,
        itemToString(item) {
            return item ? item.name : ''
          },
        onSelectedItemChange: ({selectedItem: newSelectedItem}) =>
            handleSelect(newSelectedItem),
    });
    return (
        <div>
            <input
                type="search"
                id="categoryInput"
                disabled = {myCategories.length >= 5}
                {...getInputProps()}
            />
            <ul {...getMenuProps()}>
                { suggestions.length > 0
                    ? suggestions.map((item, index) => {
                        return (
                            <li
                                key={item.code}
                                {...getItemProps({
                                    item,
                                    index
                                })} >
                                <p>{item.name}</p>
                            </li>
                        );
                    })
                    : null }
            </ul>
        </div>
    )
};

export default CategorySelectorInput;    

