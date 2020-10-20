import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const TH = styled.th`
  padding: 2px 5px;
  font-weight: bold;
`;
const TD = styled.th`
  padding: 2px 5px;
  text-align: left;
`;

function Analytics(props) {
  const { data } = props;
  const [analyticsData, setAnalyticsData] = useState({});

  useEffect(() => {
    const analytics = {};

    Object.keys(data[0]).forEach(column => {
      let sum = 0;
      const arr = data.map(row => {
        sum += parseFloat(row[column]);
        return parseFloat(row[column]);
      });

      analytics[column] = {
        max: Math.max(...arr),
        min: Math.min(...arr),
        median: arr[Math.floor(arr.length / 2)],
        average: sum / arr.length
      };
    });

    setAnalyticsData(analytics);
  }, [data]);

  return (
    <table>
      <thead>
        <tr>
          <TH>필드</TH>
          <TH>최소</TH>
          <TH>최대</TH>
          <TH>중앙</TH>
          <TH>평균</TH>
        </tr>
      </thead>
      <tbody>
        {Object.keys(analyticsData).length > 0 && Object.keys(analyticsData).map((column, index) => 
          <tr key={index}>
            <TD>{column}</TD>
            <TD>{analyticsData[column].min}</TD>
            <TD>{analyticsData[column].max}</TD>
            <TD>{analyticsData[column].median}</TD>
            <TD>{analyticsData[column].average}</TD>
          </tr>
        )}
      </tbody>
    </table>
  );
}

export default Analytics;
