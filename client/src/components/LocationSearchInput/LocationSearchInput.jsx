import { useMemo, useState } from 'react';
import { useCombobox } from 'downshift';
import SearchErrorMessage from './SearchErrorMessage';
import styles from './LocationSearchInput.module.css'


function stringFormatter(string) {
    return string.length > 40 ? string.slice(0,38) + '...' : string;
}

// Ref: https://medium.com/100-days-in-kyoto-to-create-a-web-app-with-google/day-25-adding-google-maps-autocomplete-search-to-a-react-app-8d238aa07288
function boldUserText({ length, offset, string }) {
    if (length === 0 && offset === 0) {
      return string;
    }
    string = stringFormatter(string);
    const userText = string.substring(offset, offset + length);
    const stringBefore = string.substring(0, offset);
    const stringAfter = string.substring(offset + length);
    return `${stringBefore}<b>${userText}</b>${stringAfter}`;
}

function LocationSearchInput({ coordinates, setCoordinates, isHost}) {
    const [showSuggestions, setShowSuggestions] = useState(true)
    const [selectedItem, setSelectedItem] = useState({
        name: "",
        address: ""
    })
    const [searchResult, setSearchResult] = useState({
        autocompleteSuggestions: [],    // Array of Autocomplete Prediction Objects
        status: '',                     // Status of the API call
    });

    // API related vars
    const google = window.google;
    const service = new google.maps.places.AutocompleteService();
    const geocoder = new google.maps.Geocoder();
    const sessionToken = useMemo(       // useMemo() saves the session token between rerenders
        () => new google.maps.places.AutocompleteSessionToken(),
        [google.maps.places.AutocompleteSessionToken],
    );

    const handleSelect = (item) => {
        setShowSuggestions(false)
        setSelectedItem({
            name: item.name.string,
            address: item.address.string
        })
        // Use Google Geocoder API w/ Google Places to find the coordinate of selected location
        geocoder.geocode(
            { 'placeId': item.id }, 
            function(results, status) {
                switch(status) {
                    case google.maps.GeocoderStatus.OK:
                        let countryCode = ""
                        for (const components of results[0].address_components) {
                            const { short_name="", types=[] } = components;
                            if (types.includes('country')) {
                                countryCode = short_name;
                                break;
                            }
                        }
                        const newCoordinates = {
                            latitude: results[0].geometry.location.lat(),
                            longitude: results[0].geometry.location.lng(),
                            country: countryCode,
                            name: item.name.string
                        }
                        if (coordinates !== newCoordinates) {
                            setCoordinates(newCoordinates);
                        }
                        break;
                    case google.maps.GeocoderStatus.ZERO_RESULTS:
                    case google.maps.GeocoderStatus.INVALID_REQUEST:
                        console.log(`ERROR: Experienced ${status} while geocoding`)
                        setCoordinates({
                            latitude: 91,
                            longitude: 181,
                            country: "",
                            name: ""
                        });
                        break;
                    default:
                        console.log(`ERROR: Experienced server issue ${status} while geocoding`)
                        setCoordinates({
                            latitude: 91,
                            longitude: 181,
                            country: "",
                            name: ""
                        });
                        break;
                }
             }
        );
    }
    
    // WAI-ARIA powered by Downshift
    const {
        getInputProps,
        getItemProps,
        getMenuProps,
    } = useCombobox({   // NOTE: Downshift docs reports breaking changes in past 2 versions (may need code migration in the future)
        items: searchResult.autocompleteSuggestions,
        onInputValueChange: ({ inputValue }) => {
            // If User clears the search bar, reset state
            if (inputValue === '' || !showSuggestions) {          
                setSearchResult({
                    autocompleteSuggestions: [],
                    status: '',                 
                });
                setShowSuggestions(true);
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
            }
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
                className={styles.locationInput}
                type="search"
                placeholder="central location"
                disabled={!isHost}
                {...getInputProps()}
            />
            <ul className={styles.suggestions} {...getMenuProps()}>
                { searchResult.autocompleteSuggestions.length > 0
                    ? searchResult.autocompleteSuggestions.map((item, index) => {
                        return item.address.string ? (
                            <li
                                key={item.id}
                                className={styles.suggestion}
                                {...getItemProps({
                                    item,
                                    index
                                })}
                            >
                                {/* TODO: Use DOMPurify or any other XSS-preventitive library */}
                                <p dangerouslySetInnerHTML={{__html: boldUserText(item.name)}} />
                                <p>{stringFormatter(item.address.string)}</p>
                            </li>
                        ) : null ;
                    })
                    : null }
            </ul>
            { !selectedItem.name && <SearchErrorMessage status={searchResult.status} />}
        </div>
    )
};

export default LocationSearchInput;