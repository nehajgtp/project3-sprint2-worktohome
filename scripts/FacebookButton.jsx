import * as React from 'react';
import FacebookLogin from 'react-facebook-login';
import { useHistory } from 'react-router-dom';
import { Socket } from './Socket';

export default function FacebookButton() {
  const history = useHistory();
  function handleSubmit(response) {
    const { name } = response;
    const { email } = response;
    const imageUrl = response.picture.data.url;
    window.sessionStorage.setItem('name', name);
    window.sessionStorage.setItem('email', email);
    Socket.emit('New Logged In User', {
      name, email, imageUrl,
    });
    history.push('/content');
    return true;
  }
  return (
    <FacebookLogin
      appId="135144214710282"
      fields="name,email,picture"
      callback={handleSubmit}
    />
  );
}
