import * as React from 'react';
import GoogleButton from './GoogleButton';
import FacebookButton from './FacebookButton';

export default function GuestGreeting() {
  return (
    <div>
      <h2> Work to Home </h2>
      <p>Make your home search more convenient to your commute!</p>
      <GoogleButton />
      <FacebookButton />
    </div>
  );
}
