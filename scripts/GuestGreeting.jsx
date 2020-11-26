import * as React from 'react';
import GoogleButton from './GoogleButton';

import './GuestGreeting.css';

export default function GuestGreeting() {
  return (
    <div class="title">
      <img id="logo" src="https://i.imgur.com/Zi1Oxa7.png" width="350" height="350" />
      <p>Find the best home for your commute!</p>
      <GoogleButton />
    </div>
  );
}
