import * as React from 'react';
import { GoogleLogin } from 'react-google-login';
import { useHistory } from 'react-router-dom';

export function GoogleButton(){
    const history = useHistory();
    function handleSubmit(response){
        console.log(response)
        const { name } = response.profileObj;
        window.sessionStorage.setItem('name', name);
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
