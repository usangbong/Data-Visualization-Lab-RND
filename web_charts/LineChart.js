import React, { useEffect, useRef } from 'react';

function LineChart(props) {
  const { width, height, data } = props;
  const svgRef = useRef();
  const d3 = window.d3;

  useEffect(() => {
    if (typeof data !== 'object' || data.length === 0)
      return;
    
    var margin = {top: 10, right: 30, bottom: 20, left: 60},
      drawWidth = width - margin.left - margin.right,
      drawHeight = height - margin.top - margin.bottom;
  
    var svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);
    
    svg.append('g').attr("transform", `translate(${margin.left},${margin.top})`);

    // Add X axis --> it is a date format
    var xMin = d3.min(data, (d => parseInt(d.x)));
    var xMax = d3.max(data, (d => parseInt(d.x)));
    var x = d3.scaleLinear()
      .domain([xMin, xMax])
      .range([ 0, drawWidth ]);
    svg.append("g")
      .attr("transform", `translate(0,${drawHeight})`)
      .call(d3.axisBottom(x));

    // Add Y axis
    var yMin = d3.min(data, (d => parseInt(d.y)));
    var yMax = d3.max(data, (d => parseInt(d.y)));
    yMax += yMax / 10;
    var y = d3.scaleLinear()
      .domain([yMin, yMax])
      .range([ drawHeight, 0 ]);
    svg.append("g")
      .call(d3.axisLeft(y));

    // This allows to find the closest X index of the mouse:
    var bisect = d3.bisector(function(d) { return d.x; }).left;

    // Create the circle that travels along the curve of chart
    var focus = svg
      .append('g')
      .append('circle')
        .style("fill", "none")
        .attr("stroke", "black")
        .attr('r', 8.5)
        .style("opacity", 0)

    // Create the text that travels along the curve of chart
    var focusText = svg
      .append('g')
      .append('text')
        .style("opacity", 0)
        .attr("text-anchor", "left")
        .attr("alignment-baseline", "middle")

    // Add the line
    svg
      .append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("d", d3.line()
        .x(function(d) { return x(d.x) })
        .y(function(d) { return y(d.y) })
        )

    // Create a rect on top of the svg area: this rectangle recovers mouse position
    svg
      .append('rect')
      .style("fill", "none")
      .style("pointer-events", "all")
      .attr('width', drawWidth)
      .attr('height', drawHeight)
      .on('mouseover', mouseover)
      .on('mousemove', mousemove)
      .on('mouseout', mouseout);


    // What happens when the mouse move -> show the annotations at the right positions.
    function mouseover() {
      focus.style("opacity", 1)
      focusText.style("opacity",1)
    }

    function mousemove() {
      // recover coordinate we need
      var x0 = x.invert(d3.mouse(this)[0]);
      var i = bisect(data, x0, 1);
      var selectedData = data[i];
      focus
        .attr("cx", x(selectedData.x))
        .attr("cy", y(selectedData.y));
      focusText
        .html(`x:${selectedData.x}  -  y:${selectedData.y}`)
        .attr("x", x(selectedData.x)+15)
        .attr("y", y(selectedData.y));
    }
    function mouseout() {
      focus.style("opacity", 0)
      focusText.style("opacity", 0)
    }
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

export default LineChart;
