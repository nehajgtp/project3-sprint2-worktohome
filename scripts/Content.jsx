import * as React from 'react';
import { useHistory } from 'react-router-dom';

import SearchEngine from './SearchEngine';
import SearchListings from './SearchListings';

export default function Content() {
  const history = useHistory();
  if (window.sessionStorage.getItem('name') == null) {
    history.push('/');
  }

  return (
    <div>
      <h1>Work to Home</h1>
      <hr />
      <SearchEngine />
      <SearchListings />
    </div>

  );
}
