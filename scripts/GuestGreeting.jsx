import * as React from 'react';
import GoogleButton from './GoogleButton';
import FacebookButton from './FacebookButton';

import './GuestGreeting.css';

import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';


const useStyles = makeStyles({
  title: {
    width: '100%',
    maxWidth: 2000,
    
  },
  header: {
    fontSize: '4rem',
    margin: "4.3rem"
  }
  }
);

export default function GuestGreeting() {
  const classes = useStyles();
  
  return (
    <html>
    <div className="guestGreet">
      <div className="desc">
        <img alt="" id="logo" src="https://i.imgur.com/o6qLeN4.png" width="350" height="350" />
        <p>Find the best home for your commute!</p>
        <FacebookButton />
        <GoogleButton />
      </div>
      <div className={classes.title}>
        <Divider />
        <Typography variant="h1" component="div" align="center" className={classes.header}>
        About
        </Typography>
        <Divider />
        <Typography variant="h1" component="div" align="center" className={classes.header}>
        Technologies Used
        </Typography>
      </div>
    </div>
    </html>
  );
}
