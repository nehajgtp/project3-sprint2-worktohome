import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { useState } from 'react';
import { Content } from './Content';
import { GuestGreeting } from './GuestGreeting'
import { BrowserRouter as Router, Switch, Route} from 'react-router-dom'


function Greeting(){
    return (
        <div>
            <Router>
                <Switch>
                <Route exact path="/" component={GuestGreeting}/>
                <Route path="/content" component={Content}/>
                </Switch>
            </Router>
        </div>
    );
}


ReactDOM.render(
    <Greeting/>, 
    document.getElementById('content')
    );
