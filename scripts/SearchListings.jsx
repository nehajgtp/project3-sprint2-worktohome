import * as React from 'react';
import Iframe from 'react-iframe'

import { useEffect } from 'react';
import { Socket } from './Socket';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import CssBaseline from "@material-ui/core/CssBaseline";

const useStyles = makeStyles({
  header: {
    fontSize: '2.8rem',
    margin: "2rem"
  },
  formControl: {
    width: 140,
    marginLeft: '5%'
  },
  result1: {
    color: '#5c5d9e'
  },
  
  result2: {
    color: '#c93e4a'
  }
});

export default function SearchListings(props) {
  const classes = useStyles();

  const [listings, setListings] = React.useState(false);
  const [result, setResult] = React.useState("");

  function onSearch() {
    Socket.on('sending listing', (data) => {
      console.log(data)
      if((data.length === 0)){
        setListings("None Found")
      }
      else{setListings(data);}
      console.log(data)
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

  function results(){
    console.log(listings)
    if(listings === false){
      setResult(
        <div>
        <CssBaseline />
        <Typography variant="h5" className={classes.result1} component="div" align="center">
          Enter a search!
        </Typography>
        </div>
      )
    }
    else if(listings === "None Found"){
      setResult(
      <div>
        <CssBaseline />
        <Typography variant="h5" className={classes.result2} component="div" align="center">
          No results found!
        </Typography>
      </div>
      )
    }
    else{
      setResult(
        <ul>{
          listings.map(
                  (listing) => (
                    <p>
                      Address:
                      {' '}
                      {listing.home_street}
                      ,
                      {' '}
                      {listing.home_city}
                      ,
                      {' '}
                      {listing.home_state_code}
                      <br />
                      <img id="house" alt="" src={listing.home_image}/>
                      <br />
                      Price: $
                      {listing.home_price}
                      <br />
                      Beds:
                      {' '}
                      {listing.home_baths}
                      <br />
                      Baths:
                      {' '}
                      {listing.home_beds}
                      <br />
                      <a href={listing.walkscore_more_info_link}>
                        <img alt="" src={listing.walkscore_logo} />
                      </a>
                      {listing.home_walkscore}
                      <br />
                      Description:
                      {' '}
                      {listing.walkscore_description}
                      <br />
                      <a href={listing.home_walkscore_link} target="_blank">More Walkscore info about listing</a>
                      <br />
                      Commute Time: {listing.commute_time}
                      <Iframe url={listing.iframe_url}
                        width="400px"
                        height="400px"
                        />
                      <hr />
                    </p>
                  ),
                )
      }</ul>
      )
    }
  }
  
  useEffect(() => {
    results()
    props.changeLoad()
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
          <MenuItem value={"low_high"}>Low to High</MenuItem>
          <MenuItem value={"high_low"}>High to Low</MenuItem>
        </Select>
      </FormControl>  
      {result}
    </div>
  );
}
