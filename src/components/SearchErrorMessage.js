// Ref: https://medium.com/100-days-in-kyoto-to-create-a-web-app-with-google/day-25-adding-google-maps-autocomplete-search-to-a-react-app-8d238aa07288
function SearchErrorMessage({status}) {
    return status === '' || status === 'OK' ? null : (
      <div role="alert">
        {
          status === 'ZERO_RESULTS' || status === 'INVALID_REQUEST' || status === 'NOT_FOUND' ? (
            <p>
              Sorry, no results were found. … Check your spelling. Try more general words. Try different words that mean the same thing.
            </p>
          
          ) : status === 'OVER_QUERY_LIMIT' || status === 'REQUEST_DENIED' ? (
            <p>
              GroupGrub is currently unable to use Google Maps search. Please contact us so we can fix the problem.
            </p>
          ) : (
            <p>
              Google Maps server is down. <a href="https://status.cloud.google.com/maps-platform/products/i3CZYPyLB1zevsm2AV6M/history" target="_blank" rel="noreferrer">Please check its status</a>, and try again once they fix the problem (usually within a few hours).
            </p>
          )
        }
      </div>
    )
}

export default SearchErrorMessage;