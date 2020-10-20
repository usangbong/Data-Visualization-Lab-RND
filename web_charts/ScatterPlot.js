import React, { useEffect, useRef } from 'react';

function ScatterPlot(props) {
  const { width, height, data } = props;
  const svgRef = useRef();
  const d3 = window.d3;

  useEffect(() => {
    if (typeof data !== 'object' || data.length === 0)
      return;
    
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 30, bottom: 30, left: 60},
    drawWidth = width - margin.left - margin.right,
    drawHeight = height - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select(svgRef.current)
    .html('')
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");
    
    // Add X axis
    var xMin = d3.min(data, (d => parseInt(d.x)));
    var xMax = d3.max(data, (d => parseInt(d.x)));
    var x = d3.scaleLinear()
    .domain([xMin, xMax])
    .range([ 0, drawWidth ]);
    svg.append("g")
    .attr("transform", "translate(0," + drawHeight + ")")
    .call(d3.axisBottom(x));

    // Add Y axis
    var yMin = d3.min(data, (d => parseInt(d.y)));
    var yMax = d3.max(data, (d => parseInt(d.y)));
    yMax += yMax / 10;
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
      .attr("cx", function (d) { return x(d.x); } )
      .attr("cy", function (d) { return y(d.y); } )
      .attr("r", 1.5)
      .style("fill", "#69b3a2");
  });

  return (
    <>
      {typeof data === 'object' && data.length > 0 &&
        <svg ref={svgRef}>
        </svg>
      }
    </>
  );
}

export default ScatterPlot;
