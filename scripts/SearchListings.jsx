import * as React from 'react';
import { useEffect } from 'react';
import { Socket } from './Socket';

export default function SearchListings() {
  const [listings, setListings] = React.useState([]);
  // const [result, setResult] = React.useState("");

  function onSearch() {
    Socket.on('sending listing', (data) => {
      console.log(data)
      setListings(data);
      // if(data.length === 0){
      //   setResult(<h2>"No Listings Found"</h2>)
      // }
      // else{
      //   setResult((
      //     <div>{
      //       listings.map(
      //         (listing) => (
      //           <p>
      //             Address: {listing.home_street}, {listing.home_city}, {listing.home_state_code}
      //             <br />
      //             <img id="house" alt="" src={listing.home_image} />
      //             <br />
      //             Price: ${listing.home_price}
      //             <br />
      //             Beds: {listing.home_baths}
      //             <br />
      //             Baths: {listing.home_beds}
      //             <hr />
      //           </p>
      //         ),
      //       )
      //     }</div>))
      //   }
      // console.log(result)
    });
  }
  // function results(){
  //   console.log("hi")
  //   if(listings === [] ){
  //     return (<span>No Listings found</span>)
  //   }
  //   return (
  //     <div>{
  //       listings.map(
  //         (listing) => (
  //           <p>
  //             Address: {listing.home_street}, {listing.home_city}, {listing.home_state_code}
  //             <br />
  //             <img id="house" alt="" src={listing.home_image} />
  //             <br />
  //             Price: ${listing.home_price}
  //             <br />
  //             Beds: {listing.home_baths}
  //             <br />
  //             Baths: {listing.home_beds}
  //             <hr />
  //           </p>
  //         ),
  //       )
  //   }</div>)
  // }
  // useEffect(() => {
  //   results()
  // }, [listings]);
  onSearch();
  // results();
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
