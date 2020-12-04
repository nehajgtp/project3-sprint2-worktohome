import * as React from 'react';
import GoogleButton from './GoogleButton';
import FacebookButton from './FacebookButton';

import './GuestGreeting.css';

import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Grid from '@material-ui/core/Grid';
import Link from '@material-ui/core/Link';

const useStyles = makeStyles({
  title: {
    width: '100%',
    maxWidth: 2000,
    
  },
  header: {
    fontSize: '3rem',
    margin: "2rem"
  },
  box: {
    minWidth: 275,
    minHeight: 100,
    backgroundColor: "#f2f2fc"
  },
  pos: {
    fontSize:'2rem'
  },
  name: {
    padding: 2,
    minWidth: 200,
    minHeight: 120,
    backgroundColor: "#f2f2fc"
  },
  link: {
    fontSize: '1.5rem'
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
        <Card className={classes.box}>
          <CardContent>
          <Typography className={classes.pos} align="center">
            Our website tailors your home search to your specific commute, providing information about the commute from each listing to your desired destination.
          </Typography>
          </CardContent>
        </Card>
        <Divider />
        <Typography variant="h1" component="div" align="center" className={classes.header}>
        Technologies Used
        </Typography>
        <Card className={classes.box}>
          <CardContent>
          <Typography className={classes.pos} align="center">
            React, Python, PostgreSQL, MaterialUI, Heroku, Git, CircleCI, Rapid API (Realtor), Google Maps API, ESLint, PyLint
          </Typography>
          </CardContent>
        </Card>
        <Divider />
        <Typography variant="h1" component="div" align="center" className={classes.header}>
        Made By
        </Typography>
        <Grid container spacing={3}>
        <Grid item xs={6} sm={3}>
        <Card className={classes.name} align="center">
          <CardContent>
          <Typography className={classes.pos} align="center">
            Ali Alkhateeb 
          </Typography>
          <Link className={classes.link} href="https://github.com/alialkhateeb99" target="_blank">
            GitHub
          </Link>
          </CardContent>
        </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
        <Card className={classes.name} align="center">
          <CardContent>
          <Typography className={classes.pos} align="center">
            Neha Jagtap
          </Typography>
          <Link className={classes.link} href="https://github.com/nehajgtp" target="_blank">
            GitHub
          </Link>
          </CardContent>
        </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
        <Card className={classes.name} align="center">
          <CardContent>
          <Typography className={classes.pos} align="center">
            Matthew Meeh
          </Typography>
          <Link className={classes.link} href="https://github.com/Matthew-J-M" target="_blank">
            GitHub
          </Link>
          </CardContent>
        </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
        <Card className={classes.name} align="center">
          <CardContent>
          <Typography className={classes.pos} align="center">
            Kevin Ng
          </Typography>
          <Link className={classes.link} href="https://github.com/kevinng250" target="_blank">
            GitHub
          </Link>
          </CardContent>
        </Card>
        </Grid>
        </Grid>
      </div>
    </div>
    </html>
  );
}
