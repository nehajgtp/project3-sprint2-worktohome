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
    marginLeft: 50,
    marginRight: 50,
    maxWidth: 1400,
    minHeight: 100,
    marginBottom: 50,
    backgroundColor: "#f2f2fc",
    align: 'center'
  },
  pos: {
    fontSize:'2rem'
  },
  name: {
    padding: 2,
    minWidth: 200,
    minHeight: 620,
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
  },
  steps: {
    minHeight: 600,
    minWidth: 100
  },
  stepsmedia: {
    width: '100%'
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
        <Grid container spacing={3} id="stepsCards" justify="center">
        <Grid item xs={6} sm={3}>
          <Card className={classes.steps} align="center">
            <CardMedia
              component="img"
              className={classes.stepsmedia}
              image="https://i.imgur.com/9CHbWtY.png"
            />
            <CardContent>
              <Typography className={classes.pos} align="center">
                Log in to begin search
              </Typography>
              <Typography
                variant="h4"
                component="div"
                align="center"
                className={classes.desc}
              ></Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card className={classes.steps} align="center">
            <CardMedia
              component="img"
              className={classes.stepsmedia}
              image="https://i.imgur.com/joUKKrJ.png"
            />
            <CardContent>
              <Typography className={classes.pos} align="center">
                Make a search with commute location and housing preferences
              </Typography>
              <Typography
                variant="h4"
                component="div"
                align="center"
                className={classes.desc}
              ></Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Card className={classes.steps} align="center">
            <CardMedia
              component="img"
              className={classes.stepsmedia}
              image="https://i.imgur.com/L3BycJs.png"
            />
            <CardContent>
              <Typography className={classes.pos} align="center">
                Get property listings!
              </Typography>
              <Typography
                variant="h4"
                component="div"
                align="center"
                className={classes.desc}
              ></Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
        <Divider />
        <Typography variant="h1" component="div" align="center" className={classes.header}>
        Creation of Our App
        </Typography>
        <Card className={classes.box}>
          <CardContent>
          <Typography className={classes.pos} align="center">
          <li>Frontend: For the frontend, our project contains a landing page, a page to look up real estate, and a page to look up a user’s search history. The frontend was mainly written in <b>React</b> and styled using <b>MaterialUI</b> and <b>CSS</b>. On the landing page, we used Google and Facebook login buttons as a form of <b>OAuth</b>, so that a user could easily login without needing to create a new account. </li>
          <li>Backend: For our project, we decided to implement the Python microframework <b>Flask</b> to run the server. In addition, we created functions that would call the various <b>APIs (Realtor API, Google Maps API, Walkscore API)</b> used in our project. In order to send information between the client and server, we used <b>Socket.io</b> to send information bi-directionally.</li>
          <li>Unit Testing: We created unit tests to make sure that the program is running correctly and could handle edge cases. We created unit tests to test the backend Python code. To create them, we used a Python library called <b>unittest.</b></li>
          <li>Linting: In order to style our code according to coding patterns and avoid bugs, we used a code analysis tool called <b>ESLint</b> to lint our Javascript code following Airbnb’s ESLint Rules. We also used <b>PyLint</b> and <b>Black</b> to lint our Python code.</li>
          <li>Version Control: We used <b>Git</b> to track changes to our source code. Generally, each group member created their own branches to make different changes, and then we made pull requests in order to merge our code to the main branch. We used <b>GitHub</b> to remotely host our code repository. </li>
          <li>CI/CD: We used <b>Heroku</b> to deploy our project live. We also used <b>CircleCI</b> in order to continuously test our code whenever a change was made to the remote repository. If a bug was detected by CircleCI, we would instantly be notified of it and make necessary changes to our code. </li>
          <li>Agile development: To iteratively develop our project, we used agile development practices in order to track our progress. This included creating a <b>Kanban board</b> on GitHub Projects to track the status of each tasks required for completion and track each members’ contribution. </li>
          </Typography>
          </CardContent>
        </Card>
        <Divider />
        <Typography variant="h1" component="div" align="center" className={classes.header}>
        Links
          <Card className={classes.box}>
            <CardContent>
            <Typography className={classes.pos} align="center">
              Website: <a href="https://worktohome-sprint2.herokuapp.com/">Link</a> 
              <br />
              Source Code: <a href="https://github.com/nehajgtp/project3-sprint2-worktohome">Link</a>  
            </Typography>
            </CardContent>
          </Card>
        </Typography>
        <Divider />
        <Typography variant="h1" component="div" align="center" className={classes.header}>
        Made By
        </Typography>
        <Grid container spacing={3}>
        <Grid item xs={6} sm={3}>
        <Card className={classes.name} align="center">
          <CardMedia
            component="img"
            className={classes.media}
            image="https://i.imgur.com/H4Or1pB.png"
          />
          <CardContent>
          <Typography className={classes.pos} align="center">
            Ali Alkhateeb 
          </Typography>
          <Link className={classes.link} href="https://github.com/alialkhateeb99" target="_blank">
            <img className={classes.github}src="https://cdn.iconscout.com/icon/free/png-256/github-153-675523.png"></img>
          </Link>
          <Typography variant="h4" component="div" align="center" className={classes.desc}>
            Hello! My name is Ali Alkhateeb and I am computer science student at NJIT. We built this project for purpose of finding new homes for commuters. We hope you enjoy it!
          </Typography>
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
