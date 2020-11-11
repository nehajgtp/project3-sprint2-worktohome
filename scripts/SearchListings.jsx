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
                      Address: {listing.home_street}, {listing.home_city}, {listing.home_state_code}
                      <br />
                      <img id="house" alt="" src={listing.home_image} />
                      <br />
                      Price: ${listing.home_price}
                      <br />
                      Beds: {listing.home_baths}
                      <br />
                      Baths: {listing.home_beds}
                      <hr />
                    </p>
                  ),
                )
            }
    </div>
  );
}
