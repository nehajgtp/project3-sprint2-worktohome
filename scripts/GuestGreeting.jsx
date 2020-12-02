import * as React from 'react';
import GoogleButton from './GoogleButton';
import FacebookButton from './FacebookButton';

import './GuestGreeting.css';

export default function GuestGreeting() {
  return (
    <div>
      <div className="title">
        <img alt="" id="logo" src="https://i.imgur.com/Zi1Oxa7.png" width="350" height="350" />
        <p>Find the best home for your commute!</p>
        <GoogleButton />
        <FacebookButton />
      </div>
      <div className="about">
        <div id="about-section">
          Our website tailors your home search to your specific commute,
          providing information about the commute from each listing to your desired destination.
        </div>
      </div>
    </div>
  );
}
