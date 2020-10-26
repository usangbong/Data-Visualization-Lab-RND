import React from 'react';
import styled from 'styled-components';

const Table = styled.table`
  font-size: .8em;
`;
const TH = styled.th`
  padding: 2px 5px;
  font-weight: bold;
`;
const TD = styled.th`
  padding: 2px 5px;
  text-align: left;
`;

function DataTable(props) {
  const { columnNames, data } = props;

  return (
    <>
    {data.length > 0 &&
      <Table>
        <thead>
          <tr>
            {columnNames.map((columnName, columnIndex) => 
              <TH key={columnIndex}>{columnName}</TH>
            )}
          </tr>
        </thead>
        <tbody>
            {data.map((row, rowIndex) =>
              <tr key={rowIndex}>
                {columnNames.map((columnName, columnIndex) =>
                  <TD key={columnIndex}>{row[columnName]}</TD>
                )}
              </tr>
            )}
        </tbody>
      </Table>
    }
    </>
  );
}

export default DataTable;
