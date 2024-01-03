import React from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';

export default props => (
      <div>
            <hr style={props.env || props.owner ? {} : { pointerEvents: "none", opacity: "0.0", width: "0px", height: "0px" }} id="hr-ruler" />
            <div id="header-div">
                  <h5 style={props.env ? {} : { pointerEvents: "none", opacity: "0.0", width: "0px", height: "0px" }} className="h5-head"> Environment: </h5> {props.env} <br />
                  <h5 style={props.owner ? {} : { pointerEvents: "none", opacity: "0.0", width: "0px", height: "0px" }} className="h5-head"> Owner: </h5> {props.owner} <br />
                  <h5 style={props.objective ? {} : { pointerEvents: "none", opacity: "0.0", width: "0px", height: "0px" }} className="h5-head"> Objective: </h5> {props.objective} <br />
                  <h5 style={props.location ? {} : { pointerEvents: "none", opacity: "0.0", width: "0px", height: "0px" }} className="h5-head"> Location: </h5> {props.location} <br />
            </div>
      </div>
);

