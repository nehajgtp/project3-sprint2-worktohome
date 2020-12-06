import * as React from 'react';
import { useHistory } from 'react-router-dom';
import { BeatLoader } from 'react-spinners';
import SearchEngine from './SearchEngine';
import SearchListings from './SearchListings';
import useScrollTrigger from '@material-ui/core/useScrollTrigger';
import PropTypes from 'prop-types';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import IconButton from "@material-ui/core/IconButton";
import MenuItem from "@material-ui/core/MenuItem";
import Menu from "@material-ui/core/Menu";

const useStyles = makeStyles({
  appbar: {
    background: '#8F90FA'
  },
  icon: {
    width: '40px',
  },
  header: {
    marginLeft: '50%',
    marginRight: '43%'
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
  const [anchorEl, setAnchorEl] = React.useState(null);
  
  function routHistory(){
    history.push("/history");
  }
  
  function logout() {
    history.push('/');
  }
  
  function scrollUp() {
   window.scrollTo({top: 0, behavior: 'smooth'});
  };
  
  if (window.sessionStorage.getItem('name') == null) {
    history.push('/');
  }
  const [loading, setLoading] = React.useState(false);

  function changeLoadtoTrue() {
    setLoading(true);
  }

  function changeLoadtoFalse() {
    setLoading(false);
  }
  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };
  
  return (
    <div className="theContent">
      <ElevationScroll {...props}>
        <AppBar className={classes.appbar}>
          <Toolbar>
            <Typography variant="h6" component="div" align="center" className={classes.header}>
              <img className={classes.icon}src="https://i.imgur.com/Zlaf5hk.png" align="center" onClick={scrollUp}></img>
            </Typography>
            {(
            <div>
              <IconButton
                id={classes.menu}
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={handleMenu}
                color="inherit"
              >
                <img src="https://i.imgur.com/p9kJLoE.png"/>
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorEl}
                anchorOrigin={{
                  vertical: "top",
                  horizontal: "right"
                }}
                keepMounted
                transformOrigin={{
                  vertical: "top",
                  horizontal: "right"
                }}
                open={Boolean(anchorEl)}
                onClose={handleClose}
              >
                <MenuItem onClick={routHistory}>Search History</MenuItem>
                <MenuItem onClick={logout}>Logout</MenuItem>
              </Menu>
            </div>
          )}
          </Toolbar>
        </AppBar>
      </ElevationScroll>
      <SearchEngine changeLoad={changeLoadtoTrue}/>
      <SearchListings changeLoad={changeLoadtoFalse}/>
      <div align="center">{loading ? <BeatLoader align="center"/>: null}</div>
    </div>

  );
}
