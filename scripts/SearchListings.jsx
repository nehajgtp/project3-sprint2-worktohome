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
import Divider from '@material-ui/core/Divider';
import Link from '@material-ui/core/Link';


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
  },
  
  price: {
    fontWeight: 'bold',
    margin: '3px'
  },
  bedbath: {
    marginTop: '15px'
  },
  walkscore: {
    marginTop: '5px'
  },
  
  walkscore_info: {
    fontSize: '15px',
  },
  iframe: {
    marginTop: '20px',
    marginBottom: '40px'
  }
});

export default function SearchListings(props) {
  const classes = useStyles();
  
  var fake_listings = [{
    'home_city': 'Charlotte',
    'home_street': '8800 Meadow Vista Rd', 
    'home_postal_code': '28213', 
    'home_state_code': 'NC', 
    'home_state': 'North Carolina', 
    'home_price': 925, 
    'home_baths': 1, 
    'home_beds': 1, 
    'home_image': 'https://ar.rdcpix.com/34426878/bf8c86062332425fc1a5601f3a722574c-f0o.jpg', 
    'home_lon': -80.7373, 
    'home_lat': 35.29486, 
    'iframe_url': 'https://www.google.com/maps/embed/v1/directions?origin=place_id:EikyMCBTIENvbGxlZ2UgU3QsIENoYXJsb3R0ZSwgTkMgMjgyMDIsIFVTQSIaEhgKFAoSCTPOS_MloFaIEVBSj5h8cZIeEBQ&destination=place_id:ChIJ1dVho6YeVIgR-vjqxUGPe8U&key=AIzaSyDOqSBvo9oME1LGougkz6O3hQxuwcDIWP0', 
    'commute_time': '19 mins', 
    'home_walkscore': 34, 
    'walkscore_description': 'Car-Dependent', 
    'walkscore_logo': 'https://cdn.walk.sc/images/api-logo.png', 
    'walkscore_more_info_link': 'https://www.redfin.com/how-walk-score-works', 
    'home_walkscore_link': 'https://www.walkscore.com/score/8800-Meadow-Vista-Rd-Charlotte-NC/lat=35.29486/lng=-80.7373/?utm_source=worktohome-sprint2.herokuapp.com&utm_medium=ws_api&utm_campaign=ws_api'
    },
    {
     'home_city': 'Charlotte', 
     'home_street': '2002 Laysan Teal Ln', 
     'home_postal_code': '28262', 
     'home_state_code': 'NC', 
     'home_state': 'North Carolina', 
     'home_price': 935, 
     'home_baths': 1, 
     'home_beds': 1, 
     'home_image': 'https://ar.rdcpix.com/1181656421/e5d47393908c1639704112d8979e2aecc-f0o.jpg', 
     'home_lon': -80.7378, 
     'home_lat': 35.33261, 
     'iframe_url': 'https://www.google.com/maps/embed/v1/directions?origin=place_id:EikyMCBTIENvbGxlZ2UgU3QsIENoYXJsb3R0ZSwgTkMgMjgyMDIsIFVTQSIaEhgKFAoSCTPOS_MloFaIEVBSj5h8cZIeEBQ&destination=place_id:ChIJxxrl-mUcVIgRB-NHxBdPFfY&key=AIzaSyDOqSBvo9oME1LGougkz6O3hQxuwcDIWP0', 
     'commute_time': '16 mins', 
     'home_walkscore': 34, 
     'walkscore_description': 'Car-Dependent', 
     'walkscore_logo': 'https://cdn.walk.sc/images/api-logo.png', 
     'walkscore_more_info_link': 'https://www.redfin.com/how-walk-score-works', 
     'home_walkscore_link': 'https://www.walkscore.com/score/2002-Laysan-Teal-Ln-Charlotte-NC/lat=35.33261/lng=-80.7378/?utm_source=worktohome-sprint2.herokuapp.com&utm_medium=ws_api&utm_campaign=ws_api' 
    }]

  const [listings, setListings] = React.useState(fake_listings);
  const [result, setResult] = React.useState("");

  function onSearch() {
    Socket.on('sending listing', (data) => {
      console.log(data)
      if((data.length === 0)){
        setListings("None Found")
      }
      else{setListings(data);}
      console.log(listings)
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
        <div>
        <CssBaseline />
        <ul>{
          listings.map(
                  (listing) => (
                    <p align="center">
                      <Typography variant="h5" component="div" align="center">
                        {listing.home_street}, {listing.home_city}, {listing.home_state_code}
                      </Typography>
                      <Typography variant="h5" className={classes.price} component="div" align="center">
                        ${listing.home_price.toLocaleString()}
                      </Typography>
                      <img id="house" alt="" src={listing.home_image}/>
                      <br />
                      <Typography variant="h6" className={classes.bedbath} component="div" align="center">
                        {listing.home_beds} Bed(s), {listing.home_baths} Bath(s)
                      </Typography>
                      <Link href={listing.walkscore_more_info_link} target="_blank">
                        <img className={classes.walkscore} src={listing.walkscore_logo}></img>
                      </Link> ({listing.walkscore_description})
                      <br />
                      <Link href={listing.home_walkscore_link} target="_blank">
                        More Walkscore info about listing
                      </Link>
                      <Iframe url={listing.iframe_url}
                        width="400px"
                        height="400px"
                        className={classes.iframe}
                        />
                      <Divider variant="middle" />
                    </p>
                  ),
                )
      }</ul></div>
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
