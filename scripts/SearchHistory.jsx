import * as React from 'react';
import { Socket } from './Socket';

export default function SearchHistory(){
    const [list, changeList] = new React.useState([]);
    
    function goToHistory(){
        Socket.on("received database info", (data) => {
            changeList(data);
        });
    }
    Socket.emit("request search history", 1);
    
    goToHistory();
    return <div>
    <h1>List of all searches</h1>
    {   
        list.map(
                  (listing) => (
                    <p>
                      Address: {listing.address}
                      <br />
                      <img id="house" alt="" src={listing.home_image} />
                      <br />
                      Low Price: ${listing.price_low}
                      <br />
                      High Price: {listing.price_high}
                      <br />
                      Distance from Address: {listing.distance}
                      <hr />
                    </p>
                  ),
                )
    }
    </div>;
}