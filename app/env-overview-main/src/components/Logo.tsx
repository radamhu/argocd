import React from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';

export default props => (
      <div id="image-container">
            <img id="vdf-image" src={`${process.env.PUBLIC_URL}/vdf_logo.svg`} alt="Vodafone Logo"/>
            <h4>Applications Overview</h4>
            <h5>EDD Germany</h5>
      </div>
);

