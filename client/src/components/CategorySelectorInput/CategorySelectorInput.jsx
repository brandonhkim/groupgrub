import { useContext, useState, useRef } from 'react';
import { useCombobox } from 'downshift';
import { SocketContext } from '../../context/socket';
import CategoryTree from '../../utils/CategoryTree'
import { requestAddCategory, requestGetSessionID } from '../../utils/FetchRequests';

function CategorySelectorInput({ sessionID, myCategories, setMyCategories, allCategories, setAllCategories, lobbyID }) {
    const socket = useContext(SocketContext);
    const categoryTree = useRef(new CategoryTree())
    const [showSuggestions, setShowSuggestions] = useState(true)
    const [suggestions, setSuggestions] = useState([]);
    const [selectedItem, setSelectedItem] = useState({
        name: "",
        code: ""
    })

    // Helper function used to reformat allCategories (state var) after inclusion of category
    const formattedAllCategories = (updatedCategory) => {
        const newCategories = allCategories ? [...allCategories] : [];
        let found = false;
        for (let i=0; i<newCategories.length; i++) {
            const {name, sockets} = newCategories[i]
            if (name === updatedCategory) {
                if (!sockets.includes(sessionID)) {
                    newCategories[i]["sockets"].push(sessionID);
                }
                found = true;
                break;
            }
        }
        if (!found) {
            newCategories.push({
                "name": updatedCategory,
                "sockets": [sessionID]
            });
        }
        return newCategories
    }
    
    const handleSelect = (item) => {
        if(myCategories[item.name]) {
            return
        }
        const fetchRequest = async () => {
            await requestAddCategory(lobbyID, sessionID, item.name);
            socket.emit("ROOM_CATEGORY_CHANGE", lobbyID);
        }
        fetchRequest();

        // Update state locally instead of fetching AGAIN from backend
        setAllCategories(formattedAllCategories(item.name))
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
            // TODO: Get country code from geolocation
            const matches = categoryTree.current.beginsWith("US", inputValue);
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

