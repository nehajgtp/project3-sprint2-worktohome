import * as React from 'react';

import { Socket } from './Socket';

export default function SearchListings() {
  const [listings, setListings] = React.useState([]);

  function onSearch() {
    Socket.on('sending listing', (data) => {
      setListings(data);
    });
  }

  onSearch();

  return (
    <div>
      <h2>Listings</h2>
      {
                listings.map(
                  (listing) => (
                    <p>
                      Address: {listing.HOME_STREET}, {listing.HOME_CITY}, {listing.HOME_STATE_CODE}
                      <br />
                      <img id="house" alt="" src={listing.HOME_IMAGE} />
                      <br />
                      Price: ${listing.HOME_PRICE}
                      <br />
                      Beds: {listing.HOME_BATHS}
                      <br />
                      Baths: {listing.HOME_BEDS}
                      <hr />
                    </p>
                  ),
                )
            }
    </div>
  );
}
