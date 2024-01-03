import React from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import BTable from "react-bootstrap/Table";
import { useTable } from "react-table";

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

function Tables(props) {
  const columns = React.useMemo(
    () => [
      {
        Header: "NAME",
        accessor: "name",
        Cell: ({ row }) => {
          return (
            <Link to={`/app/${row.original.id}`}>{row.original.name}</Link>
          );
        },
      },
      {
        Header: "VERSION",
        accessor: "version",
      },
      {
        Header: "ENDPOINT",
        accessor: "endpoint",
      },
      {
        Header: "LAST UPDATED",
        accessor: "lastUpdated",
      },
      {
        Header: "GIT HASH",
        accessor: "gitHash",
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

export default Tables;
