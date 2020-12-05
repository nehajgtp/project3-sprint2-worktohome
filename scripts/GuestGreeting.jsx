import * as React from 'react';
import GoogleButton from './GoogleButton';
import FacebookButton from './FacebookButton';

import './GuestGreeting.css';

import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Grid from '@material-ui/core/Grid';
import Link from '@material-ui/core/Link';
import CssBaseline from "@material-ui/core/CssBaseline";


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
    minHeight: 600,
    backgroundColor: "#f2f2fc"
  },
  link: {
    fontSize: '1.2rem'
  },
  media: {
    height: 300,
  },
  desc: {
    fontSize: '1.2rem'
  },
  github: {
    width: '25px',
    margin: '3px'
  }
  }
);

export default function GuestGreeting() {
  const classes = useStyles();
  
  return (
    <html>
    <div className="guestGreet">
    <CssBaseline />
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
            <p>Our website tailors your home search to your specific commute, providing information about the commute from each listing to 
            your desired destination. 
            </p>
            <p>Traveling to work is a major factor in the decision to purchase or rent a property for many home owners and renters. However,
            other real estate websites do not provide enough information about this.
            Therefore, we built this website so that could help those customers to conveniently access commute information for each property listing 
            on a single website.</p>
            
          </Typography>
          </CardContent>
        </Card>
        <Divider />
        <Typography variant="h1" component="div" align="center" className={classes.header}>
        Steps
        </Typography>
        <Card className={classes.box}>
          <CardContent>
          <Typography className={classes.pos} align="center">
            <ol type="1">
            <li>Log in</li>
            <li>Search for the location where you will commute to</li>
            <li>Get listings for homes nearby (each listing has info about travel routes, Walkscore scores, and commute times!)</li>
            </ol>
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
            <ul>
            <li>React</li>
            <li>Python</li>
            <li>PostgreSQL</li>
            <li>MaterialUI</li>
            <li>Heroku</li>
            <li>Git</li>
            <li>CircleCI</li>
            <li>Rapid API (Realtor)</li>
            <li>Google Maps API</li>
            <li>ESLint</li>
            <li>PyLint</li>
            </ul>
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
            <img className={classes.github}src="https://cdn.iconscout.com/icon/free/png-256/github-153-675523.png"></img>
          </Link>
          </CardContent>
        </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
        <Card className={classes.name} align="center">
          <CardMedia
            component="img"
            className={classes.media}
            image="https://i.imgur.com/t1RSRAD.jpeg"
          />
          <CardContent>
          <Typography className={classes.pos} align="center">
            Neha Jagtap
          </Typography>
          <Link className={classes.link} href="https://github.com/nehajgtp" target="_blank">
            <img className={classes.github}src="https://cdn.iconscout.com/icon/free/png-256/github-153-675523.png"></img>
          </Link>
          <Typography variant="h4" component="div" align="center" className={classes.desc}>
            As a Computer Science major about to enter the workforce, being in CS 490 was a great opportunity. 
            Not only did I learn a lot of new technologies, but I also have a better understanding what it takes to
            develop complex software programs as part of a team. 
          </Typography>
          </CardContent>
        </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
        <Card className={classes.name} align="center">
          <CardMedia
            component="img"
            className={classes.media}
            image="https://i.imgur.com/2zo7dCR.jpg"
          />
          <CardContent>
          <Typography className={classes.pos} align="center">
            Matthew Meeh
          </Typography>
          <Link className={classes.link} href="https://github.com/Matthew-J-M" target="_blank">
            <img className={classes.github}src="https://cdn.iconscout.com/icon/free/png-256/github-153-675523.png"></img>
          </Link>
          <Typography variant="h4" component="div" align="center" className={classes.desc}>
            Hello, I am Matthew Meeh. I love video games especially platform fighters. My plan is to work in industry as a software engineer. 
            I hope you enjoy using our CS490 project.
          </Typography>
          </CardContent>
        </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
        <Card className={classes.name} align="center">
          <CardMedia
            component="img"
            className={classes.media}
            image="https://i.imgur.com/AqXgJS5.png"
          />
          <CardContent>
          <Typography className={classes.pos} align="center">
            Kevin Ng
          </Typography>
          <Link className={classes.link} href="https://github.com/kevinng250" target="_blank">
            <img className={classes.github}src="https://cdn.iconscout.com/icon/free/png-256/github-153-675523.png"></img>
          </Link>
          <Typography variant="h4" component="div" align="center" className={classes.desc}>
            Hello, my name is Kevin Ng. I’m a senior studying computer science at NJIT. 
            Work to Home is our CS490 Project and we hope you guys like it!
          </Typography>
          </CardContent>
        </Card>
        </Grid>
        </Grid>
      </div>
    </div>
    </html>
  );
}
