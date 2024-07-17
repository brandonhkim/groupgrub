import { useEffect, useRef } from "react";
import { Loader } from '@googlemaps/js-api-loader'

// maidenless since 2021
const SAL_ADDRESS = {
    lat:   34.02116,
    lng: -118.287132
}

function PlacesLoader({ setLoading }) {
    const googlemap = useRef(null);

    // Ref: https://developers.google.com/maps/documentation/javascript/load-maps-js-api
    useEffect(() => { 
        const loader = new Loader({
            apiKey: process.env.REACT_APP_MAPS_KEY,
            version: 'weekly',
        });
        loader.importLibrary('places').then(() => {
            // Attaches the loader via the #map div (i think :b)
            new window.google.maps.Map(
                googlemap.current, {
                    center: SAL_ADDRESS,
                    zoom: 8,
                }
            );
            setLoading(false);  // LocationSearchInput should only be available AFTER the API Loader is ready
        });
    }, [setLoading]); // Empty dependency array => useEffect() runs only once (in theory)
    
    return (
        <div id="map" ref={ googlemap } />
    )
}

export default PlacesLoader