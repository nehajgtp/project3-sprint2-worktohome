import * as React from 'react';
import { useHistory } from 'react-router-dom';
import SearchEngine from './SearchEngine';
import SearchListings from './SearchListings';
import { BeatLoader } from 'react-spinners'

export default function Content() {
  const history = useHistory();
  if (window.sessionStorage.getItem('name') == null) {
    history.push('/');
  }
  const [loading, setLoading] = React.useState(false);
  function changeLoadtoTrue(){
    console.log("damn")
    setLoading(true)
  }
  function changeLoadtoFalse(){
    console.log("dude")
    setLoading(false)
  }
  return (
    <div>
      <h1>Work to Home</h1>
      <hr />
      <SearchEngine changeLoad={changeLoadtoTrue}/>
      <SearchListings changeLoad={changeLoadtoFalse}/>
      {loading ? <BeatLoader/>: null}
    </div>

  );
}
