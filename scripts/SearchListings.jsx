import * as React from 'react';
import { useEffect } from 'react';
import { Socket } from './Socket';

export default function SearchListings(props) {
  const [listings, setListings] = React.useState(false);
  const [result, setResult] = React.useState("");

  function onSearch() {
    Socket.on('sending listing', (data) => {
      console.log(data)
      if(data.length == 0){
        setListings("None Found")
      }
      else{setListings(data);}
      
    });
  }
  
  onSearch();
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
            <li key = {listing}>
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
                </p>
              </li>
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
      {result}
    </div>
  );
}
