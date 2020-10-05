import React, { useEffect, useRef } from 'react';

function LineChart(props) {
  const { width, height, data } = props;
  const svgRef = useRef();
  const d3 = window.d3;

  useEffect(() => {
    if (typeof data !== 'object' || data.length === 0)
      return;
    var margin = {top: 10, right: 50, bottom: 20, left: 60},
      drawWidth = width - margin.left - margin.right,
      drawHeight = height - margin.top - margin.bottom;
  
    var svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);
    
    svg.append('g').attr("transform",
      "translate(" + margin.left + "," + margin.top + ")");

    // Add X axis --> it is a date format
    var xMin = d3.min(data, (d => parseInt(d.x)));
    var xMax = d3.max(data, (d => parseInt(d.x)));
    var x = d3.scaleLinear()
      .domain([xMin, xMax])
      .range([ 0, drawWidth ]);
    svg.append("g")
      .attr("transform", "translate(0," + drawHeight + ")")
      .call(d3.axisBottom(x));

    // Add Y axis: position value
    // var yMin = d3.min(data, (d => parseInt(d.y)));
    // var yMax = d3.max(data, (d => parseInt(d.y)));
    // yMax += yMax / 10;
    // var y = d3.scaleLinear()
    //   .domain([yMin, yMax])
    //   .range([ drawHeight, 0 ]);
    // svg.append("g")
    //   .call(d3.axisLeft(y));
    var yMin = d3.min(data, (d => parseInt(d.y)));
    var yMax = d3.max(data, (d => parseInt(d.y)));
    yMax += yMax / 10;
    var y = d3.scaleLinear()
      .domain([yMin, yMax])
      .range([ drawHeight, 0 ]);
    svg.append("g")
      .call(d3.axisLeft(y));

    var vMin = d3.min(data, (d => d.v));
    var vMax = d3.max(data, (d => d.v));
    vMax += vMax * 1;
    var v = d3.scaleLinear()
      .domain([vMin, vMax])
      .range([ drawHeight, 0 ]);
    svg.append("g")
      .call(d3.axisRight(v));

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

    var focusLine = svg
      .append('path')
        .append("g")
        .attr("fill", "none")
        .attr("stroke", "black")
        .attr('stroke-width', 1.5)
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

    svg
      .append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "red")
      .attr("stroke-width", 1.5)
      .attr("d", d3.line()
        .x(function(d) { return x(d.x) })
        .y(function(d) { return v(d.v) })
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

    function getHoriData(_y, _xMax){
      const _data = [];

      for (let i=0; i<_xMax; i++){
        var _p = {
          x: i,
          y: _y
        }
        _data.push(_p);
      }
      return _data;
    }

    
    // What happens when the mouse move -> show the annotations at the right positions.
    function mouseover() {
      focus.style("opacity", 1)
      focusText.style("opacity",1)
      focusLine.style("opacity",1)
    }

    function mousemove() {
      // recover coordinate we need
      var x0 = x.invert(d3.mouse(this)[0]);
      var i = bisect(data, x0, 1);
      var my = d3.mouse(this)[1];
      
      var selectedData = data[i];
      focus
        .attr("cx", x(selectedData.x))
        .attr("cy", v(selectedData.v));
      focusText
        // .html(`x:${selectedData.x}  -  y:${selectedData.y}`)
        .html(`v:${my}`)
        .attr("x", x(selectedData.x)+15)
        .attr("y", my);
      
      var _lineData = getHoriData(my, xMax);
      console.log(_lineData);
      svg.append("path")
        .datum(_lineData)
        .attr("d", d3.line()
          .x(function(d) {return x(d.x); })
          .y(function(d) {return 100; })
        );

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
