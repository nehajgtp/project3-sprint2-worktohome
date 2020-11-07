import * as React from 'react';
import { GoogleLogin } from 'react-google-login';
import { useHistory } from 'react-router-dom';

export function GoogleButton(props){
    const history = useHistory();
    function handleSubmit(response){
        const { name } = response.profileObj;
        const { email } = response.profileObj
        window.sessionStorage.setItem('name', name);
        window.sessionStorage.setItem('email', email);
        history.push("/content");
        return true;
    }
    return (
        <GoogleLogin
            clientId="1034127712778-v6qvk1ma6ilbg141bvuitipumnvklo4j.apps.googleusercontent.com"
            buttonText ="Login"
            onSuccess={handleSubmit}
            cookiePolicy="single_host_origin"
        />
    );
}
