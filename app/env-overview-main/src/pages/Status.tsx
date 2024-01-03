import React, { useEffect, useState } from "react";
import axios from "axios";
import { css } from "@emotion/react";
import { BarLoader } from "react-spinners";
import StatusTable from "../components/StatusTable";

const baseURL = process.env.REACT_APP_API_URL;

export default function Status() {
  const [items, setItems] = useState(null);

  useEffect(() => {
    axios.defaults.headers.common["Content-Type"] =
      "application/json;charset=utf-8";
    axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
    axios.defaults.headers.common["Access-Control-Allow-Headers"] =
      "Origin, X-Requested-With, Content-Type, Accept";
    // axios.defaults.headers.common['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS';
    axios.defaults.headers.common = {
      "X-API-Key": process.env.REACT_APP_API_KEY,
    };

    const fetchData = async () => {
      const { data } = await axios.get(baseURL + "/api/apps/status");
      setItems(data);
    };

    fetchData();
  }, []);

  const modifyDate = (date, fullDatePrefix = "") => {
    const now = new Date();
    const k8sDate = new Date(date); //create Date object from date string
    // const germanDate = offsetTime(k8sDate, 1); //add an hour to k8s date

    if (k8sDate.toDateString() === now.toDateString()) {
      //date is today
      const modifiedDate = k8sDate.toLocaleTimeString("de-DE", {
        hour: "numeric",
        minute: "numeric",
      }); // turn date into hh:mm

      return `today at ${modifiedDate}`;
    } else {
      const modifiedDate = k8sDate.toLocaleDateString("de-DE", {
        month: "numeric",
        day: "numeric",
        year: "numeric",
        hour: "numeric",
        minute: "numeric",
      }); // turn date into "dd.mm, hh:mmm" format

      return `${fullDatePrefix}${modifiedDate}`;
    }
  };

  const renderItems = (data) => {
    const modifiedData = data
      .filter((object) => object.STATUSes.length > 0)
      .map((object) => ({
        ...object,
        lastUpdated: modifyDate(object.lastUpdated),
        environment: object.ENVIRONMENT.env_name,
        statusType: object.STATUSes[object.STATUSes.length - 1].type,
        message: object.STATUSes[object.STATUSes.length - 1].message,
        statusId: object.STATUSes[object.STATUSes.length - 1].id,
      }));

    return (
      <div id="tables-div" key="status-table">
        <StatusTable data={modifiedData} />
      </div>
    );
  };

  const renderLoading = () => {
    return (
      <div className="sweet-loading">
        <BarLoader
          color="red"
          loading={true}
          height={10}
          width={240}
          speedMultiplier={0.8}
        />
      </div>
    );
  };

  return <div>{items ? renderItems(items) : renderLoading()}</div>;
}
