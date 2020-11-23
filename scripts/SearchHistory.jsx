import * as React from 'react';
import { Socket } from './Socket';
import { useHistory } from 'react-router-dom';


export default function SearchHistory(){
    const [list, changeList] = new React.useState([]);
    const [boolean, changeBoolean] = new React.useState(false);
    const history = useHistory();
    

    function goToHistory(){
        changeBoolean(true);
        console.log("Before waiting on socket.")
        Socket.on("received database info", (data) => {
            changeList(data);
        });
    }
    
    function goToSearchEngine(){
        history.push("/content");
    }
    
    if(boolean == false){
        console.log("Before emit.")
        Socket.emit("request search history", 1);
        console.log("Before call to goToHistory")
        goToHistory();
    }
    console.log("Going to display.")
    var objects = list;
    //console.log(objects)
    if(objects.length != 0){
        return <div>
        <h1>List of all searches</h1>
        {   
            objects.map(
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
        <button type="button" onClick={goToSearchEngine}>Go back to search page.</button>
        </div>;
    }
    else {
        return <div>
        <h1>No searches for this user.</h1>
        <button type="button" onClick={goToSearchEngine}>Go back to search page.</button>
        </div>;
    }
}