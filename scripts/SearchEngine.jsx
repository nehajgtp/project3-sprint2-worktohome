import * as React from 'react';
import { Socket } from './Socket';
import { useHistory } from 'react-router-dom';


export default function SearchEngine(props) {
  const history = useHistory();
    
  const [address, setAddress] = React.useState('');
  const [city, setCity] = React.useState('');
  const [statecode, setStateCode] = React.useState('');
  const [maxCommute, setMaxCommute] = React.useState(50);
  const [minPrice, setMinPrice] = React.useState(0);
  const [maxPrice, setMaxPrice] = React.useState(10000);
  const [purchaseType, setPurchaseType] = React.useState('rent');

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

  function handleMaxCommuteChange(event) {
    setMaxCommute(event.target.value);
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
    if (Number.isInteger(parseInt(maxCommute, 10)) === false) {
      inputErrors.push(`Max commute distance is not a number${maxCommute}`);
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
        max_commute: parseInt(maxCommute, 10),
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
    <div>
      <h3>Commute Location</h3>
      Address:
      {' '}
      <input onChange={handleAddressChange} />
      City:
      {' '}
      <input onChange={handleCityChange} />
      <label htmlFor="state">State:</label>
      <select onChange={handleStateChange}>
        <option value=""> -- Select state -- </option>
        <option value="AL">Alabama</option>
        <option value="AK">Alaska</option>
        <option value="AZ">Arizona</option>
        <option value="AR">Arkansas</option>
        <option value="CA">California</option>
        <option value="CO">Colorado</option>
        <option value="CT">Connecticut</option>
        <option value="DE">Delaware</option>
        <option value="DC">District Of Columbia</option>
        <option value="FL">Florida</option>
        <option value="GA">Georgia</option>
        <option value="HI">Hawaii</option>
        <option value="ID">Idaho</option>
        <option value="IL">Illinois</option>
        <option value="IN">Indiana</option>
        <option value="IA">Iowa</option>
        <option value="KS">Kansas</option>
        <option value="KY">Kentucky</option>
        <option value="LA">Louisiana</option>
        <option value="ME">Maine</option>
        <option value="MD">Maryland</option>
        <option value="MA">Massachusetts</option>
        <option value="MI">Michigan</option>
        <option value="MN">Minnesota</option>
        <option value="MS">Mississippi</option>
        <option value="MO">Missouri</option>
        <option value="MT">Montana</option>
        <option value="NE">Nebraska</option>
        <option value="NV">Nevada</option>
        <option value="NH">New Hampshire</option>
        <option value="NJ">New Jersey</option>
        <option value="NM">New Mexico</option>
        <option value="NY">New York</option>
        <option value="NC">North Carolina</option>
        <option value="ND">North Dakota</option>
        <option value="OH">Ohio</option>
        <option value="OK">Oklahoma</option>
        <option value="OR">Oregon</option>
        <option value="PA">Pennsylvania</option>
        <option value="RI">Rhode Island</option>
        <option value="SC">South Carolina</option>
        <option value="SD">South Dakota</option>
        <option value="TN">Tennessee</option>
        <option value="TX">Texas</option>
        <option value="UT">Utah</option>
        <option value="VT">Vermont</option>
        <option value="VA">Virginia</option>
        <option value="WA">Washington</option>
        <option value="WV">West Virginia</option>
        <option value="WI">Wisconsin</option>
        <option value="WY">Wyoming</option>
      </select>
      <label htmlFor="purchase-type">Purchase Type:</label>
      <select onChange={handlePurchaseTypeChange}>
        <option value="rent">For Rent</option>
        <option value="sale">For Sale</option>
      </select>
      <h3>Housing Preferences</h3>
      Maximum Commute Distance (miles):
      <input placeholder="Max Commute" onChange={handleMaxCommuteChange} />
      Price:
      <input placeholder="Min Price" onChange={handleMinPriceChange} />
      <input placeholder="Max Price" onChange={handleMaxPriceChange} />
      <br />
      <button type="submit" onClick={handleSubmit}>Search</button>
      <br />
     <button type="button" onClick={routHistory}>Search History</button>
      <hr />
    </div>
  );
}
