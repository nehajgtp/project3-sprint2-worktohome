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
                  <hr />
                </p>
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
