function unpack(rows, key) {
    console.log(rows)
      return rows.map(function(row) {
          console.log(row[key])
        return row[key];
      });
    }
          d3.csv("../static/data/KOSPI.csv", function(err, rows) {
            var trace1 = {
              type: "scatter",
              mode: "lines",
              name: 'actual',
              x: unpack(rows, 'date'),
              y: unpack(rows, 'actual'),
              line: {
                color: '#17BECF'
              }
            }
            var trace2 = {
              type: "scatter",
              mode: "lines",
              name: 'prediction',
              x: unpack(rows, 'date'),
              y: unpack(rows, 'prediction'),
              line: {
                color: '#7F7F7F'
              }
            }
            var data = [trace1, trace2];
            var layout = {
              title: 'test',
            };
            Plotly.newPlot('myDiv', data, layout);
          });



