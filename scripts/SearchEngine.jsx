import * as React from 'react';

export function SearchEngine() {
    const [statecode, setStateCode] = React.useState("");
    
    function handleStateChange(event) {
        setStateCode(event.target.value);
    }
    
    function handleSubmit() {
        alert(statecode);
    }
    
    return (<div>
                Address: <input></input>
                City: <input></input>
                <label for="state">State:</label>
                <select onChange={handleStateChange}>
                	<option value="AL">Alabama</option>
                	<option value="AK">Alaska</option>
                	<option value="AZ">Arizona</option>
                </select> 
                <button onClick={handleSubmit}>Submit</button>
                <hr></hr>
            </div>);
}