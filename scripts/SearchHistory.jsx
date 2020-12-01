import * as React from 'react';
import { useHistory } from 'react-router-dom';
import { Socket } from './Socket';

export default function SearchHistory(props) {
  const [List, changeList] = new React.useState([]);
  const [Happened, changeHappened] = new React.useState(false);
  const history = useHistory();

  function goToHistory() {
    changeHappened(true);
    Socket.on('received database info', (data) => {
      changeList(data);
    });
  }
  function handleSubmit(){
    const address = "26 Wilton Street";
    const city = "New Hyde Park";
    const state = "NY";
    const maxCommute = "10";
    const minPrice = "0";
    const maxPrice ="1000000";
    window.sessionStorage.setItem('address', address);
    window.sessionStorage.setItem('city', city);
    window.sessionStorage.setItem('state', state);
    window.sessionStorage.setItem('maxCommute', maxCommute)
    window.sessionStorage.setItem('minPrice', minPrice)
    window.sessionStorage.setItem('maxPrice', maxPrice)
    history.push('/content', {historyState: false, address: "26 Wilton Street", city: "New Hyde Park", statecode: "NY", maxCommute: "10", minPrice:"0", maxPrice:"1000000"})
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
        <h1>List of all searches</h1>
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
                <button type="submit" onClick={handleSubmit}>Search</button>
                </div>
              ),
            )
        }
        <button type="button" onClick={goToSearchEngine}>Go back to search page.</button>
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
