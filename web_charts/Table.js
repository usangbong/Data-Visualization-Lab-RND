import React from 'react';
import { DataGrid } from '@material-ui/data-grid';

function LineChart(props) {
  const { data } = props;
  
  const columns = Object.keys(data[0]).map(key => {
    return {
      field: key,
      headerName: key
    };
  });

  let id = 1;
  const rows = data.map(row => {
    const returns = {};
    returns.id = id++;
    for (let key in row)
      returns[key] = row[key];
    return returns;
  })

  console.log(columns);
  console.log(rows);

  return (
    <>
      {typeof data === 'object' && data.length > 0 &&
        <div style={{ width: 1000, height: 500 }}>
          <DataGrid columns={columns} rows={rows} pageSize={10} checkBoxSelection />
        </div>
      }
    </>
  );
}

export default LineChart;
