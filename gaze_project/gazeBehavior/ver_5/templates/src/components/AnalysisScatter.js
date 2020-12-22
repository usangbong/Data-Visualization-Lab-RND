import React, { useEffect, useRef } from 'react';

function AnalysisScatter(props) {
  const { width, height, dataURL, filteredData } = props;
  const svgRef = useRef();
  const d3 = window.d3;
  const colors = ["#a6cee3", "#fb9a99", "#fdbf6f", "#cab2d6", "#b15928", "#b2df8a", "#ffff99", "#1f78b4", "#e31a1c", "#ff7f00", "#33a02c", "#6a3d9a"];
  
  useEffect(() => {
    if(typeof dataURL !== 'string' || dataURL.length === 0)
      return;

    d3.select(svgRef.current).selectAll("*").remove();
    
      // set the dimensions and margins of the graph
    var margin = {top: 30, right: 30, bottom: 30, left: 30},
    drawWidth = width - margin.left - margin.right,
    drawHeight = height - margin.top - margin.bottom;

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
      // console.log(data);
      // Add X axis
      var xMin = d3.min(data, (d => parseFloat(d.x)));
      var xMax = d3.max(data, (d => parseFloat(d.x)));
      var x = d3.scaleLinear()
        .domain([xMin, xMax])
        .range([ 0, drawWidth ]);
      svg.append("g")
        .attr("class", "xaxis")
        .attr("transform", "translate(0," + drawHeight + ")")
        .call(d3.axisBottom(x));

      // Add Y axis
      var yMin = d3.min(data, (d => parseFloat(d.y)));
      var yMax = d3.max(data, (d => parseFloat(d.y)));
      var y = d3.scaleLinear()
        .domain([yMin, yMax])
        .range([ drawHeight, 0]);
      svg.append("g")
        .attr("class", "yaxis")
        .call(d3.axisLeft(y));

      // Add dots
      svg.append('g')
      .selectAll("dot")
      .data(data)
      .enter()
      .append("circle")
        .attr("class", "point")
        .attr("cx", function (d) { return x(d.x); } )
        .attr("cy", function (d) { return y(d.y); } )
        .attr("r", 1.5)
        .style("fill", function (d) {return colors[parseInt(d.clu)]});

        d3.selectAll('.point')
        .on('click', function(d){
          console.log(d);
        });

    });
    

    
  }, [, props.dataURL]);

  return (
    <>
      {typeof dataURL === 'string' && dataURL.length !== 0 &&
        <svg ref={svgRef}>
        </svg>
      }
    </>
  );
}

export default AnalysisScatter;
