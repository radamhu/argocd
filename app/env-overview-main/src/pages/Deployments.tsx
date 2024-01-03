import React, { useEffect, useState } from "react";
import axios from "axios";
import { useStateWithCallbackLazy } from "use-state-with-callback";
import { css } from "@emotion/react";
import Tables from "../components/Tables";
import Head from "../components/Head";
import { BarLoader } from "react-spinners";

const baseURL = process.env.REACT_APP_API_URL + "/api/all";

export default function Deployments() {
  const [items, setItems] = useState(null);
  const [environmentFilteredItems, setEnvironmentFilteredItems] =
    useStateWithCallbackLazy(items);
  const [filteredItems, setFilteredItems] = useState(environmentFilteredItems);
  const [filterInput, setFilterInput] = useState({
    selector: "All Environments",
    filter: "",
  });
  const [crawlerTimestamp, setCrawlerTimestamp] = useState(null);

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
      const { data } = await axios.get(baseURL);
      setItems(data.envs);
      setFilteredItems(data.envs);
      setEnvironmentFilteredItems(data.envs, () => {
        console.log("data", data);
      });
      setCrawlerTimestamp(data.accounts);
    };

    fetchData();
  }, []);

  const renderPage = (data) => {
    const handleSelectorChange = (event) => {
      setFilterInput({
        selector: event.target.value,
        filter: filterInput.filter,
      });

      const updateFilteredItems = (envFilteredItems) => {
        const mappedItems = envFilteredItems.map((element) => {
          return {
            ...element,
            apps: element.apps.filter((subElement) =>
              subElement.name.includes(filterInput.filter)
            ),
          };
        });
        setFilteredItems(mappedItems);
      };

      if (event.target.value !== "All Environments") {
        const mappedItems = items.filter((element) => {
          return element.env_name == event.target.value;
        });
        setEnvironmentFilteredItems(mappedItems, () => {
          updateFilteredItems(mappedItems);
        });
      } else {
        setEnvironmentFilteredItems(items, () => {
          updateFilteredItems(items);
        });
      }
    };

    const handleInputChange = (event) => {
      setFilterInput({
        selector: filterInput.selector,
        filter: event.target.value,
      });

      const mappedItems = environmentFilteredItems.map((element) => {
        return {
          ...element,
          apps: element.apps.filter((subElement) =>
            subElement.name.includes(event.target.value)
          ),
        };
      });

      setFilteredItems(mappedItems);
    };

    const handleSubmit = (event) => {
      event.preventDefault();
    };

    return (
      <>
        <div
          style={{
            paddingLeft: "100px",
            paddingRight: "100px",
            display: "flex",
          }}
        >
          <div>
            <label htmlFor="selector" style={{ fontSize: "22px" }}>
              Filter
            </label>
            <form onSubmit={handleSubmit}>
              <select
                name="selector"
                id="selector"
                value={filterInput.selector}
                onChange={handleSelectorChange}
              >
                <option value="All Environments">All Environments</option>
                {items.map((item) =>
                  item.apps.length > 0 ? (
                    <option key={item.env_name} value={item.env_name}>
                      {item.env_name}
                    </option>
                  ) : null
                )}
              </select>
              <input
                style={{ marginLeft: 5, paddingLeft: 5 }}
                placeholder="Applications"
                type="text"
                id="filter"
                name="filter"
                value={filterInput.filter}
                onChange={handleInputChange}
              />
            </form>
          </div>
          <div style={{ marginLeft: "auto", paddingTop: "18px" }}>
            {crawlerTimestamp !== null && (
              <>
                <h6>
                  TEST updated{" "}
                  {modifyDate(
                    crawlerTimestamp.filter((obj) => obj.account === "test")[0].updateTime
                  )}
                </h6>
                <h6>
                  PROD updated{" "}
                  {modifyDate(
                    crawlerTimestamp.filter((obj) => obj.account === "prod")[0].updateTime, "on "
                  )}
                </h6>
              </>
            )}
          </div>
        </div>

        {renderItems(data)}
      </>
    );
  };

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
    const modifiedData = data.map((object) => ({
      ...object,
      apps: object.apps.map((element) => ({
        ...element,
        lastUpdated: modifyDate(element.lastUpdated),
      })),
    }));

    return modifiedData.map((element) =>
      element.apps.length <= 0 ? (
        <div key={element.id}>{null}</div>
      ) : (
        <div id="tables-div" key={element.id}>
          <Head
            env={element.env_name}
            owner={element.owner}
            objective={element.objective}
            location={element.aws_location}
          />
          <Tables data={element.apps} />
        </div>
      )
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

  return (
    <div>{filteredItems ? renderPage(filteredItems) : renderLoading()}</div>
  );
}
