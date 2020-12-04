import * as React from 'react';
import { useHistory } from 'react-router-dom';
import { BeatLoader } from 'react-spinners';
import SearchEngine from './SearchEngine';
import SearchListings from './SearchListings';

export default function Content() {
  const history = useHistory();
  if (window.sessionStorage.getItem('name') == null) {
    history.push('/');
  }
  const [loading, setLoading] = React.useState(false);

  function changeLoadtoTrue() {
    setLoading(true);
  }
  function changeLoadtoFalse() {
    setLoading(false);

  }
  return (
    <div>
      <h1>Work to Home</h1>
      <hr />
      <SearchEngine changeLoad={changeLoadtoTrue} />
      <SearchListings changeLoad={changeLoadtoFalse} />
      {loading ? <BeatLoader /> : null}
    </div>

  );
}
