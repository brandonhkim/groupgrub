import { useMemo, useState } from 'react';
import { useCombobox } from 'downshift';
import SearchErrorMessage from './SearchErrorMessage';

// Ref: https://medium.com/100-days-in-kyoto-to-create-a-web-app-with-google/day-25-adding-google-maps-autocomplete-search-to-a-react-app-8d238aa07288
function boldUserText({ length, offset, string }) {
    if (length === 0 && offset === 0) {
      return string;
    }
    const userText = string.substring(offset, offset + length);
    const stringBefore = string.substring(0, offset);
    const stringAfter = string.substring(offset + length);
    return `${stringBefore}<b>${userText}</b>${stringAfter}`;
}

// TODO: ensure that sessionToken persists for the entirety of the session
function LocationSearchInput(){
    const [searchResult, setSearchResult] = useState({
        autocompleteSuggestions: [],    // Array of Autocomplete Prediction Objects
        status: '',                     // Status of the API call
    });

    // API related vars
    const google = window.google;
    const service = new google.maps.places.AutocompleteService();
    const sessionToken = useMemo(       // useMemo() saves the session token between rerenders
        () => new google.maps.places.AutocompleteSessionToken(),
        [google.maps.places.AutocompleteSessionToken],
    );
    console.log(sessionToken)
    
    // WAI-ARIA powered by Downshift
    const {
        getInputProps,
        getItemProps,
        getMenuProps,
    } = useCombobox({   // NOTE: Downshift docs reports breaking changes in past 2 versions (may need code migration in the future)
        items: searchResult.autocompleteSuggestions,
        onInputValueChange: ({ inputValue }) => {
        
        // If User clears the search bar, reset state
        if (inputValue === '') {          
            setSearchResult({
            autocompleteSuggestions: [],
            status: '',                 
            });
            return;
        }
        
        // Otherwise, call Places API to get autocomplete predictions
        service.getPlacePredictions({
            input: inputValue,         
            sessionToken: sessionToken,
            }, handlePredictions       
        );   
        
        // Reformat API responses to display ready objects
        function handlePredictions(predictions, status) {
            switch(status) {
                case 'OK':
                    const autocompleteSuggestions = predictions.map((prediction) => {
                        return {
                        id: prediction.place_id,
                        name: {
                            string: prediction.structured_formatting.main_text,
                            length: prediction.structured_formatting.main_text_matched_substrings[0].length,
                            offset: prediction.structured_formatting.main_text_matched_substrings[0].offset,
                        },
                        address: {
                            string: prediction.structured_formatting.secondary_text,
                        },
                        };
                    });
                    // Update state with API's response
                    setSearchResult({
                        autocompleteSuggestions: autocompleteSuggestions,
                        status: 'OK',
                    })
                    break;

                default:
                    setSearchResult({
                        autocompleteSuggestions: [],
                        status: status,             
                    });
                    break;
            }
        }}
    });

    return (
        <div>
            <input 
                type="search"
                {...getInputProps()}
            />
            <ul {...getMenuProps()}>
                { searchResult.autocompleteSuggestions.length > 0
                    ? searchResult.autocompleteSuggestions.map((item, index) => {
                        return (
                            <li
                            key={item.id}
                            {...getItemProps({
                                item,
                                index
                            })}
                            >
                                {/* TODO: Use DOMPurify or any other XSS-preventitive library */}
                                <p dangerouslySetInnerHTML={{__html: boldUserText(item.name)}} />
                                <p>{item.address.string}</p>
                            </li>
                        );
                    })
                    : null }
            </ul>
            <SearchErrorMessage status={searchResult.status} />
        </div>
    )
};

export default LocationSearchInput;