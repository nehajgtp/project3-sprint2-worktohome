    
import * as React from 'react';
import { useHistory } from 'react-router-dom'
import { Button } from './Button';
import { Socket } from './Socket';

export function Content() {
    const history = useHistory();
    if(window.sessionStorage.getItem('name') == null){
        history.push("/")
    }
    return (
        <div>
            <h1>{window.sessionStorage.getItem('name')}</h1>
            <h1>{window.sessionStorage.getItem('email')}</h1>
        </div>
    );
}
