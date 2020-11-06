    
import * as React from 'react';

import { SearchEngine } from './SearchEngine';
import { SearchListings } from './SearchListings';


export function Content() {
    return (
        <div>
            <h1>Work to Home</h1>
            <hr></hr>
            <SearchEngine></SearchEngine>
            <SearchListings></SearchListings>
        </div>

    );
}
