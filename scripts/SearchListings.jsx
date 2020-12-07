import * as React from 'react';

import Iframe from 'react-iframe';
import { useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import CssBaseline from '@material-ui/core/CssBaseline';
import Divider from '@material-ui/core/Divider';
import Link from '@material-ui/core/Link';
import { Socket } from './Socket';

const useStyles = makeStyles({
  header: {
    fontSize: '2.8rem',
    margin: '2rem',
  },
  formControl: {
    width: 140,
    marginLeft: '5%',
  },
  result1: {
    color: '#5c5d9e',
  },

  result2: {
    color: '#c93e4a',
  },

  price: {
    fontWeight: 'bold',
    margin: '3px',
  },
  bedbath: {
    marginTop: '15px',
  },
  walkscore: {
    marginTop: '5px',
  },

  walkscore_info: {
    fontSize: '15px',
  },
  walkscore_desc: {
    display: 'inline-block',
    fontSize: '17px',
  },
  iframe: {
    marginTop: '20px',
    marginBottom: '40px',
  },
});

export default function SearchListings(props) {
  const classes = useStyles();

  const [listings, setListings] = React.useState(false);

  const [result, setResult] = React.useState('');

  function onSearch() {
    Socket.on('sending listing', (data) => {
      if ((data.length === 0)) {
        setListings('None Found');
        props.changeLoad();
      } else { setListings(data); }
    });
  }

  onSearch();

  function sortListings(event) {
    if (event.target.value === 'low_high' && listings !== []) {
      const sortedLowHigh = listings.sort((a, b) => parseInt(a.home_price, 10) - parseInt(b.home_price, 10));
      Socket.emit('sort listings', sortedLowHigh);
    } else if (event.target.value === 'high_low' && listings !== []) {
      const sortedHighLow = listings.sort((a, b) => parseInt(a.home_price, 10) - parseInt(b.home_price, 10)).reverse();
      Socket.emit('sort listings', sortedHighLow);
    }
  }

  function sortedListings() {
    Socket.on('sorted listings', (returnedListings) => {
      setListings(returnedListings);
    });
  }

  sortedListings();
  function results() {
    if (listings === false) {
      setResult(
        <div>
          <CssBaseline />
          <Typography variant="h5" className={classes.result1} component="div" align="center">
            Enter a search!
          </Typography>
        </div>,
      );
    } else if (listings === 'None Found') {
      setResult(
        <div>
          <CssBaseline />
          <Typography variant="h5" className={classes.result2} component="div" align="center">
            No results found!
          </Typography>
        </div>,
      );
    } else {
      setResult(
        <div>
          <CssBaseline />
          <ul>
            {
          listings.map(
            (listing) => (
              <p align="center">
                <Typography variant="h5" component="div" align="center">
                  {listing.home_street}
                  ,
                  {listing.home_city}
                  ,
                  {listing.home_state_code}
                </Typography>
                <Typography variant="h5" className={classes.price} component="div" align="center">
                  $
                  {listing.home_price.toLocaleString()}
                </Typography>
                <img id="house" alt="" src={listing.home_image} />
                <br />
                <Typography variant="h6" className={classes.bedbath} component="div" align="center">
                  {listing.home_beds}
                  {' '}
                  Bed(s),
                  {listing.home_baths}
                  {' '}
                  Bath(s)
                </Typography>
                <Link href={listing.walkscore_more_info_link} target="_blank">
                  <img alt="" className={classes.walkscore} src={listing.walkscore_logo} />
                </Link>
                {' '}
                <div className={classes.walkscore_desc}>
                  {listing.home_walkscore}
                  {' '}
                  (
                  {listing.walkscore_description}
                  )
                </div>
                <br />
                <Link href={listing.home_walkscore_link} target="_blank">
                  More Walkscore info about listing
                </Link>
                <Iframe
                  url={listing.iframe_url}
                  width="400px"
                  height="400px"
                  className={classes.iframe}
                />
                <Divider variant="middle" />
              </p>
            ),
          )
      }
          </ul>
        </div>,
      );
    }
  }

  useEffect(() => {
    results();
    props.changeLoad();
  }, [listings]);

  return (
    <div>
      <CssBaseline />
      <Typography variant="h2" component="div" align="center" className={classes.header}>
        Listings
      </Typography>
      <FormControl className={classes.formControl}>
        <InputLabel id="">Sort Price By</InputLabel>
        <Select
          labelId=""
          id=""
          onChange={sortListings}
          autoWidth
        >
          <MenuItem value="">
            <em>Sort price</em>
          </MenuItem>
          <MenuItem value="low_high">Low to High</MenuItem>
          <MenuItem value="high_low">High to Low</MenuItem>
        </Select>
      </FormControl>
      {result}
    </div>
  );
}
