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
  
  function sortListings(event) {
    if (event.target.value === "low_high" && listings !== []) {
      var sortedLowHigh = listings.sort((a, b) => parseInt(a.home_price) - parseInt(b.home_price))
      Socket.emit('sort listings', sortedLowHigh)
    }
    
    else if (event.target.value == "high_low" && listings !== []) {
      var sortedHighLow = listings.sort((a, b) => parseInt(a.home_price) - parseInt(b.home_price)).reverse()
      Socket.emit('sort listings', sortedHighLow)
    }
  }
  
  function sortedListings() {
    Socket.on('sorted listings', (listings) => {
      setListings(listings)
    })
  }
  
  sortedListings()

  return (
    <div>
      <h2>Listings</h2>
      <label htmlFor="Sort By">Sort By:</label>
      <select onChange={sortListings}>
        <option value="">---- Select option -----</option>
        <option value="low_high">Low to High</option>
        <option value="high_low">High to Low</option>
      </select>
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
                      <br />
                      <a href={listing.walkscore_more_info_link}><img src={listing.walkscore_logo} /></a>
                      {listing.home_walkscore}
                      <br />
                      Description: {listing.walkscore_description}
                      <br />
                      <a href={listing.home_walkscore_link}>More Walkscore info about listing</a>
                      <hr />
                    </p>
                  ),
                )
            }
    </div>
  );
}
