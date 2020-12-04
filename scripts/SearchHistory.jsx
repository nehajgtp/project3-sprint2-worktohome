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
  function search(){
    history.push("/content")
    Socket.emit('send search history parameters', {
      address: "26 Wilton Street", 
      city: "New Hyde Park", 
      state: "NY", 
      max_commute: "10", 
      min_price:0, 
      max_price:1000000,
      purchase_type: "sale"
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
                  Distance from Address:
                  {' '}
                  {listing.distance}
                  <hr />
                </p>
                <button type="button" onClick={search}>Search</button>
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
