import * as React from 'react';
import Iframe from 'react-iframe'

import { useEffect } from 'react';
import { Socket } from './Socket';

export default function SearchListings(props) {
  const [listings, setListings] = React.useState(false);
  const [result, setResult] = React.useState("");

  function onSearch() {
    Socket.on('sending listing', (data) => {
      console.log(data)
      if((data.length === 0)){
        setListings("None Found")
      }
      else{setListings(data);}
      console.log(data)
    });
  }
  
  onSearch();

  function sortListings(event) {
    if (event.target.value === 'low_high' && listings !== []) {
      const sortedLowHigh = listings.sort((a, b) => parseInt(a.home_price, 10) - parseInt(b.home_price, 10));
      Socket.emit('sort listings', sortedLowHigh);
    } else if (event.target.value === 'high_low' && listings !== []) {
      const sortedHighLow = listings.sort((a, b) => parseInt(a.home_price, 10) - parseInt(b.home_price, 10)).reverse();
      Socket.emit('sort listings', sortedHighLow);
    }
  }

  function sortedListings() {
    Socket.on('sorted listings', (returnedListings) => {
      setListings(returnedListings);
    });
  }

  sortedListings();

  function results(){
    console.log(listings)
    if(listings === false){
      setResult(<span>Enter an Address</span>)
    }
    else if(listings === "None Found"){
      setResult(<span>No Listings Found</span>)
    }
    else{
      setResult(
        <ul>{
          listings.map(
                  (listing) => (
                    <p>
                      Address:
                      {' '}
                      {listing.home_street}
                      ,
                      {' '}
                      {listing.home_city}
                      ,
                      {' '}
                      {listing.home_state_code}
                      <br />
                      <img id="house" alt="" src={listing.home_image}/>
                      <br />
                      Price: $
                      {listing.home_price}
                      <br />
                      Beds:
                      {' '}
                      {listing.home_baths}
                      <br />
                      Baths:
                      {' '}
                      {listing.home_beds}
                      <br />
                      <a href={listing.walkscore_more_info_link}>
                        <img alt="" src={listing.walkscore_logo} />
                      </a>
                      {listing.home_walkscore}
                      <br />
                      Description:
                      {' '}
                      {listing.walkscore_description}
                      <br />
                      <a href={listing.home_walkscore_link} target="_blank">More Walkscore info about listing</a>
                      <br />
                      Commute Time: {listing.commute_time}
                      <Iframe url={listing.iframe_url}
                        width="400px"
                        height="400px"
                        />
                      <hr />
                    </p>
                  ),
                )
      }</ul>)
    }
  }
  
  useEffect(() => {
    results()
    props.changeLoad()
  }, [listings]);
  
  return (
    <div>
      <h2>Listings</h2>
      <label htmlFor="Sort By">Sort By:</label>
      <select onChange={sortListings}>
        <option value="">---- Select option -----</option>
        <option value="low_high">Low to High</option>
        <option value="high_low">High to Low</option>
      </select>
      {result}
    </div>
  );
}
