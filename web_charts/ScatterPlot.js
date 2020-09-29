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
    .attr("width", drawWidth + margin.left + margin.right)
    .attr("height", drawHeight + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");
    
    // Add X axis
    var x = d3.scaleLinear()
    .domain([0, 4000])
    .range([ 0, drawWidth ]);
    svg.append("g")
    .attr("transform", "translate(0," + drawHeight + ")")
    .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
    .domain([0, 500000])
    .range([ drawHeight, 0]);
    svg.append("g")
    .call(d3.axisLeft(y));

    // Add dots
    svg.append('g')
    .selectAll("dot")
    .data(data)
    .enter()
    .append("circle")
      .attr("cx", function (d) { return x(d.GrLivArea); } )
      .attr("cy", function (d) { return y(d.SalePrice); } )
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
