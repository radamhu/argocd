import React, { useState } from "react";
import axios from "axios";
//import { useParams, useHistory } from "react-router-dom";
import {useParams, useNavigate} from 'react-router-dom';



const baseURL = process.env.REACT_APP_API_URL;

export default function Application() {
  const navigate = useNavigate();
  const params = useParams();
  //const history = useHistory();
  const [type, setType] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    axios.defaults.headers.common["Content-Type"] =
      "application/json;charset=utf-8";
    axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
    axios.defaults.headers.common["Access-Control-Allow-Headers"] =
      "Origin, X-Requested-With, Content-Type, Accept";
    // axios.defaults.headers.common['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS';
    axios.defaults.headers.common = {
      "X-API-Key": process.env.REACT_APP_API_KEY,
    };

    axios
      .post(baseURL + "/api/status/" + params.id, { type, message })
      .then((response) => {
        console.log(response.data);
        //history.push("/status");
        navigate('/');
        //navigate('/',{replace: true});
        //Go back
        //navigate(-1)
        //Go forward
        //navigate(1)
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <div style={{ display: "flex", justifyContent: "center" }}>
      <form
        onSubmit={handleSubmit}
        style={{
          width: "50%",
          backgroundColor: "#F4F4F4",
          padding: "20px",
          borderRadius: "10px",
        }}
      >
        <h5 style={{ marginBottom: "10px" }}>
          Add a new status message to this app
        </h5>
        <label style={{ color: "#E60000", fontWeight: "bold" }}>
          Type:
          <select
            value={type}
            onChange={(event) => setType(event.target.value)}
            style={{
              marginLeft: "10px",
              padding: "5px",
              border: "none",
              borderRadius: "4px",
            }}
          >
            <option value="">Select an option</option>
            <option value="incident">Incident</option>
            <option value="outage">Outage</option>
          </select>
        </label>
        <br />
        <label style={{ color: "#E60000", fontWeight: "bold", width: "100%" }}>
          Message:
          <textarea
            style={{
              width: "100%",
              height: "100px",
              marginTop: "5px",
              padding: "10px",
              border: "none",
              borderRadius: "4px",
            }}
            value={message}
            onChange={(event) => setMessage(event.target.value)}
          />
        </label>
        <br />
        <button
          type="submit"
          style={{
            backgroundColor: "#E60000",
            color: "white",
            padding: "10px 20px",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
            fontWeight: "bold",
            marginTop: "5px",
          }}
        >
          Submit
        </button>
      </form>
    </div>
  );
}
