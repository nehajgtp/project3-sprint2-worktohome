import * as React from 'react';

import { Socket } from './Socket';

export default function SearchListings() {
  const dict = [{
    address: '1600 Pennsylvania Ave, Washington, DC',
    image: 'https://d3g9pb5nvr3u7.cloudfront.net/sites/54e605552720c85d64735cc5/-911839127/256.png',
  },
  {
    address: 'Elvis Presley Blvd, Memphis, TN 38116',
    image: 'https://upload.wikimedia.org/wikipedia/commons/5/54/Graceland_Memphis_Tennessee.jpg',
  }];
  const [listings, setListings] = React.useState(dict);

  function onSearch() {
    Socket.on('receive listings', (data) => {
      setListings(data.listings);
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
                      {listing.address}
                      <br />
                      <img id="house" alt="House" src={listing.image} />
                      <hr />
                    </p>
                  ),
                )
            }
    </div>
  );
}
