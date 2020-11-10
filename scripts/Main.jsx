import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Content from './Content';
import GuestGreeting from './GuestGreeting';

function Greeting() {
  return (
    <div>
      <Router>
        <Switch>
          <Route exact path="/" component={GuestGreeting} />
          <Route path="/content" component={Content} />
        </Switch>
      </Router>
    </div>
  );
}

ReactDOM.render(
  <Greeting />,
  document.getElementById('content'),
);
