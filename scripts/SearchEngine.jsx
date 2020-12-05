import * as React from 'react';
import { Socket } from './Socket';
import { useHistory } from 'react-router-dom';
import './SearchEngine.css';
import TextField from '@material-ui/core/TextField';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import PropTypes from "prop-types";
import NumberFormat from "react-number-format";
import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: '2.7rem',
    minWidth: 200,
  },
  address: {
    margin: '2.7rem',
    width: '50ch'
  },
  city: {
    margin: '2.7rem',
    width: '30ch'
  },
  price: {
    margin: '1.5rem',
  }
}));

const NumberFormatCustom = React.forwardRef(function NumberFormatCustom(props,ref) 
{
  const { onChange, ...other } = props;

  return (
    <NumberFormat
      {...other}
      getInputRef={ref}
      onValueChange={(values) => {
        onChange({
          target: {
            name: props.name,
            value: values.value
          }
        });
      }}
      thousandSeparator
      isNumericString
      prefix="$"
    />
  );
});

NumberFormatCustom.propTypes = {
  name: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired
};


export default function SearchEngine(props) {
  const history = useHistory();
  const classes = useStyles();

  const [address, setAddress] = React.useState('');
  const [city, setCity] = React.useState('');
  const [statecode, setStateCode] = React.useState('');
  const [minPrice, setMinPrice] = React.useState({
    numberformat: ""
  });
  const [maxPrice, setMaxPrice] = React.useState({
    numberformat: ""
  });
  const [purchaseType, setPurchaseType] = React.useState('');

  function routHistory(){
    history.push("/history");
  }
  
  function handleAddressChange(event) {
    setAddress(event.target.value);
  }

  function handleCityChange(event) {
    setCity(event.target.value);
  }

  function handleStateChange(event) {
    setStateCode(event.target.value);
  }

  function handleMinPriceChange(event) {
    setMinPrice(event.target.value);
  }

  function handleMaxPriceChange(event) {
    setMaxPrice(event.target.value);
  }

  function handlePurchaseTypeChange(event) {
    setPurchaseType(event.target.value);
  }

  function handleSubmit() {
    const inputErrors = [];

    if (address === '') {
      inputErrors.push('Please enter an address')
    }
    
    if (city === '') {
      inputErrors.push('Please enter a city')
    }
    
    if (statecode === '') {
      inputErrors.push('Please enter a state')
    }
    
    if (purchaseType === '') {
      inputErrors.push('Please enter a purchase type')
    }
    
    if (Number.isInteger(parseInt(minPrice, 10)) === false) {
      inputErrors.push('Min price is not a number');
    }

    if (Number.isInteger(parseInt(maxPrice, 10)) === false) {
      inputErrors.push('Max price is not a number');
    }

    if (inputErrors.length > 0) {
      alert(inputErrors);
    }

    if (inputErrors.length === 0) {
      Socket.emit('send search parameters', {
        address,
        city,
        state: statecode,
        min_price: parseInt(minPrice, 10),
        max_price: parseInt(maxPrice, 10),
        purchase_type: purchaseType,
      });
    }

    Socket.on('Invalid search input', (invalidInputErrors) => {
      alert(invalidInputErrors);
    });
    props.changeLoad()
  }

  return (
    <div className="searchPart">
      <TextField
        className={classes.address}
          id=""
          label="Address"
          placeholder="Enter work address"
          multiline
          onChange={handleAddressChange}
        />
        <TextField
          className={classes.city}
          id=""
          label="City"
          placeholder="Enter work city"
          multiline
          onChange={handleCityChange}
        />
        
      <FormControl className={classes.formControl}>
        <InputLabel id="">State</InputLabel>
        <Select
          labelId=""
          id=""
          value={statecode}
          onChange={handleStateChange}
          autoWidth
        >
          <MenuItem value="">
            <em>Select state</em>
          </MenuItem>
          <MenuItem value={"AL"}>Alabama</MenuItem>
          <MenuItem value={"AK"}>Alaska</MenuItem>
          <MenuItem value={"AZ"}>Arizona</MenuItem>
          <MenuItem value={"AR"}>Arkansas</MenuItem>
          <MenuItem value={"CA"}>California</MenuItem>
          <MenuItem value={"CO"}>Colorado</MenuItem>
          <MenuItem value={"CT"}>Connecticut</MenuItem>
          <MenuItem value={"DE"}>Delaware</MenuItem>
          <MenuItem value={"DC"}>District Of Columbia</MenuItem>
          <MenuItem value={"FL"}>Florida</MenuItem>
          <MenuItem value={"GA"}>Georgia</MenuItem>
          <MenuItem value={"HI"}>Hawaii</MenuItem>
          <MenuItem value={"ID"}>Idaho</MenuItem>
          <MenuItem value={"IL"}>Illinois</MenuItem>
          <MenuItem value={"IN"}>Indiana</MenuItem>
          <MenuItem value={"IA"}>Iowa</MenuItem>
          <MenuItem value={"KS"}>Kansas</MenuItem>
          <MenuItem value={"KY"}>Kentucky</MenuItem>
          <MenuItem value={"LA"}>Louisiana</MenuItem>
          <MenuItem value={"ME"}>Maine</MenuItem>
          <MenuItem value={"MD"}>Maryland</MenuItem>
          <MenuItem value={"MA"}>Massachusetts</MenuItem>
          <MenuItem value={"MI"}>Michigan</MenuItem>
          <MenuItem value={"MN"}>Minnesota</MenuItem>
          <MenuItem value={"MS"}>Mississippi</MenuItem>
          <MenuItem value={"MO"}>Missouri</MenuItem>
          <MenuItem value={"MT"}>Montana</MenuItem>
          <MenuItem value={"NE"}>Nebraska</MenuItem>
          <MenuItem value={"NV"}>Nevada</MenuItem>
          <MenuItem value={"NH"}>New Hampshire</MenuItem>
          <MenuItem value={"NJ"}>New Jersey</MenuItem>
          <MenuItem value={"NM"}>New Mexico</MenuItem>
          <MenuItem value={"NY"}>New York</MenuItem>
          <MenuItem value={"NC"}>North Carolina</MenuItem>
          <MenuItem value={"ND"}>North Dakota</MenuItem>
          <MenuItem value={"OH"}>Ohio</MenuItem>
          <MenuItem value={"OK"}>Oklahoma</MenuItem>
          <MenuItem value={"OR"}>Oregon</MenuItem>
          <MenuItem value={"PA"}>Pennsylvania</MenuItem>
          <MenuItem value={"RI"}>Rhode Island</MenuItem>
          <MenuItem value={"SC"}>South Carolina</MenuItem>
          <MenuItem value={"SD"}>South Dakota</MenuItem>
          <MenuItem value={"TN"}>Tennessee</MenuItem>
          <MenuItem value={"TX"}>Texas</MenuItem>
          <MenuItem value={"UT"}>Utah</MenuItem>
          <MenuItem value={"VT"}>Vermont</MenuItem>
          <MenuItem value={"VA"}>Virginia</MenuItem>
          <MenuItem value={"WA"}>Washington</MenuItem>
          <MenuItem value={"WV"}>West Virginia</MenuItem>
          <MenuItem value={"WI"}>Wisconsin</MenuItem>
          <MenuItem value={"WY"}>Wyoming</MenuItem>
        </Select>
      </FormControl>
      <FormControl className={classes.formControl}>
        <InputLabel id="">Rent/Sale</InputLabel>
        <Select
          labelId=""
          id=""
          value={purchaseType}
          onChange={handlePurchaseTypeChange}
          autoWidth
        >
          <MenuItem value="">
            <em>Select purchase type</em>
          </MenuItem>
          <MenuItem value={"rent"}>For Rent</MenuItem>
          <MenuItem value={"sale"}>For Sale</MenuItem>
        </Select>
      </FormControl>
      <div id="price">
      <TextField
        className={classes.price}
        label="Minimum Price"
        value={minPrice.numberformat}
        onChange={handleMinPriceChange}
        name=""
        id=""
        placeholder="Enter numerical value"
        InputProps={{
          inputComponent: NumberFormatCustom
        }}
      />
      <TextField
        className={classes.price}
        label="Maximum Price"
        value={maxPrice.numberformat}
        onChange={handleMaxPriceChange}
        name=""
        id=""
        placeholder="Enter numerical value"
        inputProps={{style: { textAlign: 'center' }}}
        InputProps={{
          inputComponent: NumberFormatCustom,
        }}
      />
      </div>
      <Button id="searchButton" variant="contained" onClick={handleSubmit}>Search</Button>
      <Divider />
    </div>
  );
}
