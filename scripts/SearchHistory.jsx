import * as React from 'react';
import { useHistory } from 'react-router-dom';
import { Socket } from './Socket';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles({
  table: {
    maxWidth: 1100,
    margin: 'auto'
  },
  header: {
    fontSize: '40px',
    margin: 'auto',
    marginTop: 20,
    marginBottom: 20
  }
});

export default function SearchHistory() {
  const [List, changeList] = new React.useState([]);
  const [Happened, changeHappened] = new React.useState(false);
  const history = useHistory();
  const classes = useStyles();

  function goToHistory() {
    changeHappened(true);
    Socket.on('received database info', (data) => {
      changeList(data);
    });
  }
  function search(listing){
    // console.log(address)
    history.push("/content")
    Socket.emit('send search history parameters', {
      address: listing.address, 
      city: listing.city, 
      state: listing.state, 
      max_commute: listing.distance, 
      min_price: listing.price_low, 
      max_price: listing.price_high,
      purchase_type: listing.purchase_type
    });
  }
  function goToSearchEngine() {
    history.push('/content');
  }

  if (Happened === false) {
    Socket.emit('request search history');
    goToHistory();
  }
  const objects = List;
  if (objects.length !== 0) {
    return (
      <div>
      <Typography variant="h2" component="div" align="center" className={classes.header}>
        Search History
        </Typography>
      <TableContainer className={classes.table} component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell><b>Address</b></TableCell>
              <TableCell align="center"><b>Minimum Price</b></TableCell>
              <TableCell align="center"><b>Maximum Price</b></TableCell>
              <TableCell align="center"><b>Purchase Type</b></TableCell>
              <TableCell align="center"><b>Search Again</b></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
          {objects.map((listing) => (
            <TableRow>
              <TableCell component="th" scope="row">
                {listing.address}
              </TableCell>
              <TableCell align="center">${listing.price_low.toLocaleString()}</TableCell>
              <TableCell align="center">${listing.price_high.toLocaleString()}</TableCell>
              <TableCell align="center">{listing.purchase_type.charAt(0).toUpperCase() + listing.purchase_type.slice(1)}</TableCell>
              <TableCell align="center"><Button id="searchButton" variant="contained" onClick={() => {search(listing)}}>Search</Button></TableCell>
            </TableRow>
              ),
            )
        }
            </TableBody>
          </Table>
        </TableContainer>
      </div>
    );
  }

  return (
    <div>
      <h1>No searches for this user.</h1>
      <button type="button" onClick={goToSearchEngine}>Go back to search page.</button>
    </div>
  );
}
