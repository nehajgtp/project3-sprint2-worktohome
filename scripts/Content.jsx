import * as React from 'react';
import { useHistory } from 'react-router-dom';
import SearchEngine from './SearchEngine';
import SearchListings from './SearchListings';
import { BeatLoader } from 'react-spinners';
import useScrollTrigger from '@material-ui/core/useScrollTrigger';
import PropTypes from 'prop-types';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';


const useStyles = makeStyles({
  appbar: {
    background: '#8F90FA'
  },
  icon: {
    width: '40px',
  },
  header: {
    marginLeft: '50%'
  }
  }
);

function ElevationScroll(props) {
  const { children, window } = props;
  const trigger = useScrollTrigger({
    disableHysteresis: true,
    threshold: 0,
    target: window ? window() : undefined,
  });

  return React.cloneElement(children, {
    elevation: trigger ? 4 : 0,
  });
}

ElevationScroll.propTypes = {
  children: PropTypes.element.isRequired,
  window: PropTypes.func,
};

export default function Content(props) {
  const classes = useStyles();
  const history = useHistory();
  if (window.sessionStorage.getItem('name') == null) {
    history.push('/');
  }
  const [loading, setLoading] = React.useState(false);
  function changeLoadtoTrue(){
    console.log("Hello")
    setLoading(true)
  }
  function changeLoadtoFalse(){
    setLoading(false)
  }
  return (
    <div>
      <ElevationScroll {...props}>
        <AppBar className={classes.appbar}>
          <Toolbar>
            <Typography variant="h6" component="div" align="center" className={classes.header}>
              <img className={classes.icon}src="https://i.imgur.com/Zlaf5hk.png" align="center"></img>
            </Typography>
          </Toolbar>
        </AppBar>
      </ElevationScroll>
      <SearchEngine changeLoad={changeLoadtoTrue}/>
      <SearchListings changeLoad={changeLoadtoFalse}/>
      {loading ? <BeatLoader/>: null}
    </div>

  );
}
