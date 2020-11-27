import React, { useEffect, useRef } from 'react';
// import axios from 'axios';

function ScatterPlot(props) {
  const { width, height, dataURL, axis } = props;
  const svgRef = useRef();
  const d3 = window.d3;
  
  useEffect(() => {
    if(typeof dataURL !== 'string' || dataURL.length === 0 || axis.length === 0)
      return;

    d3.select(svgRef.current).selectAll("*").remove();
    
      // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 60},
    drawWidth = 460 - margin.left - margin.right,
    drawHeight = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select(svgRef.current)
    .attr("width", drawWidth + margin.left + margin.right)
    .attr("height", drawHeight + margin.top + margin.bottom)
    .append("svg")
    .attr("width", drawWidth + margin.left + margin.right)
    .attr("height", drawHeight + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

    //Read the data
    d3.csv(dataURL, function(data) {
      // Add X axis
      var xMin = d3.min(data, (d => parseFloat(d[axis[0]])));
      var xMax = d3.max(data, (d => parseFloat(d[axis[0]])));
      var x = d3.scaleLinear()
      .domain([xMin, xMax])
      .range([ 0, drawWidth ]);
      svg.append("g")
      .attr("transform", "translate(0," + drawHeight + ")")
      .call(d3.axisBottom(x));

      // Add Y axis
      var yMin = d3.min(data, (d => parseFloat(d[axis[1]])));
      var yMax = d3.max(data, (d => parseFloat(d[axis[1]])));
      var y = d3.scaleLinear()
      .domain([yMin, yMax])
      .range([ drawHeight, 0]);
      svg.append("g")
      .call(d3.axisLeft(y));

      // Add dots
      svg.append('g')
      .selectAll("dot")
      .data(data)
      .enter()
      .append("circle")
        .attr("cx", function (d) { return x(d[axis[0]]); } )
        .attr("cy", function (d) { return y(d[axis[1]]); } )
        .attr("r", 1.5)
        .style("fill", "#69b3a2")
    })
  }, [, props.axis]);

  return (
    <>
      {typeof dataURL === 'string' && dataURL.length !== 0 && axis.length !== 0 &&
        <svg ref={svgRef}>
        </svg>
      }
    </>
  );
}

export default ScatterPlot;
