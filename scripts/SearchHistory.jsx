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
    history.push('/content')
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
