import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import BTable from "react-bootstrap/Table";
import { useTable } from "react-table";
import axios from "axios";
//import { useHistory } from "react-router-dom";
import {useNavigate} from 'react-router-dom';

const baseURL = process.env.REACT_APP_API_URL;

function Table({ columns, data }) {
  // Use the state and functions returned from useTable to build your UI
  const { getTableProps, headerGroups, rows, prepareRow } = useTable({
    columns,
    data,
  });

  // Render the UI for your table
  return (
    <BTable striped bordered hover size="sm" {...getTableProps()}>
      <thead>
        {headerGroups.map((headerGroup) => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map((column) => (
              <th {...column.getHeaderProps()}>{column.render("Header")}</th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody>
        {rows.map((row, i) => {
          prepareRow(row);
          return (
            <tr {...row.getRowProps()}>
              {row.cells.map((cell) => {
                return <td {...cell.getCellProps()}>{cell.render("Cell")}</td>;
              })}
            </tr>
          );
        })}
      </tbody>
    </BTable>
  );
}

function StatusTable(props) {
  //const history = useHistory();
  const navigate = useNavigate();

  const onClick = (statusId) => {
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
      .delete(baseURL + "/api/status/" + statusId)
      .then((response) => {
        console.log(response.data);
        //history.go(0);
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

  const columns = React.useMemo(
    () => [
      {
        Header: "NAME",
        accessor: "name",
      },
      {
        Header: "ENVIRONMENT",
        accessor: "environment",
      },
      {
        Header: "VERSION",
        accessor: "version",
      },
      {
        Header: "TYPE",
        accessor: "statusType",
      },
      {
        Header: "MESSAGE",
        accessor: "message",
      },
      {
        Header: "LAST UPDATED",
        accessor: "lastUpdated",
      },
      {
        Header: "DELETE",
        accessor: "statusId",
        Cell: ({ row }) => {
          console.log(row.original);
          return (
            <button
              // type="submit"
              onClick={() => onClick(row.original.statusId)}
              style={{
                backgroundColor: "#E60000",
                color: "white",
                padding: "4px 8px",
                border: "none",
                borderRadius: "4px",
                cursor: "pointer",
                // fontWeight: "bold",
                // marginTop: "5px",
              }}
            >
              Delete
            </button>
            // <Link to={`/app/${row.original.id}`}>{row.original.name}</Link>
          );
        },
      },
    ],
    []
  );

  return (
    <div
      style={
        props.data.length > 0
          ? {}
          : {
              pointerEvents: "none",
              opacity: "0.0",
              width: "0px",
              height: "0px",
            }
      }
      id="table-div"
    >
      <Table columns={columns} data={props.data} />
      <hr />
    </div>
  );
}

export default StatusTable;
