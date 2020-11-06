import * as React from 'react';

export function SearchListings() {
    var dict = [{
        address: "1600 Pennsylvania Ave, Washington, DC",
        image: "https://d3g9pb5nvr3u7.cloudfront.net/sites/54e605552720c85d64735cc5/-911839127/256.png"
    }, 
    {
        address: "1600 Pennsylvania Ave, Washington, DC",
        image: "https://d3g9pb5nvr3u7.cloudfront.net/sites/54e605552720c85d64735cc5/-911839127/256.png"
    }];
    const [listings, setListings] = React.useState(dict)
    
    return (
        <div>
            <hr></hr>
            <h2>Listings</h2>
            {
                listings.map(
                    (listing, index) => <p>
                                            <img id="house" src={listing.image} />
                                            {listing.address}
                                            <hr></hr>                                        
                                        </p>
                )
            }
        </div>
    );
}