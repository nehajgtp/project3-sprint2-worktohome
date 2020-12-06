import * as React from 'react';
import { useHistory } from 'react-router-dom';
import { Socket } from './Socket';

export default function SearchHistory() {
  const [List, changeList] = new React.useState([]);
  const [Happened, changeHappened] = new React.useState(false);
  const history = useHistory();

  function goToHistory() {
    changeHappened(true);
    Socket.on('received database info', (data) => {
      changeList(data);
    });
  }
  function search(listing){
    // console.log(address)
    history.push("/content")
    Socket.emit('send search history parameters', {
      address: listing.address, 
      city: listing.city, 
      state: listing.state, 
      max_commute: listing.distance, 
      min_price: listing.price_low, 
      max_price: listing.price_high,
      purchase_type: listing.purchase_type
    });
  }
  function goToSearchEngine() {
    history.push('/content');
  }

  if (Happened === false) {
    Socket.emit('request search history');
    goToHistory();
  }
  const objects = List;
  if (objects.length !== 0) {
    return (
      <div>
        <h1>Search History</h1>
        <button type="button" onClick={goToSearchEngine}>Go back to search page</button>
        {
            objects.map(
              (listing) => (
              <div>
                <p>
                  Address:
                  {' '}
                  {listing.address}
                  <br />
                  Low Price: $
                  {listing.price_low}
                  <br />
                  High Price:
                  {' '}
                  {listing.price_high}
                  <br />
                  Purchase Type:
                  {' '}
                  {listing.purchae_type}
                  <hr />
                </p>
                <button type="button" onClick={() => {search(listing)} }>Search</button>
              </div>
              ),
            )
        }
      </div>
    );
  }

  return (
    <div>
      <h1>No searches for this user.</h1>
      <button type="button" onClick={goToSearchEngine}>Go back to search page.</button>
    </div>
  );
}
