// https://www.d3-graph-gallery.com/graph/parallel_custom.html
import React, { useEffect, useRef } from 'react';

function ParallelCoordinateChart(props) {
  const { width, height, patchDataFileURL } = props;
  const svgRef = useRef();
  const d3 = window.d3;
  const COLORS = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf", "#999999"];
  const featureList = ["intensity", "color", "orientation", "curvature", "center_bias", "entropy_rate", "log_spectrum", "HOG"];
    
  useEffect(() => {
    if (patchDataFileURL.length === 0)
      return;
    d3.select(svgRef.current).selectAll("*").remove();
    console.log(patchDataFileURL);
    let margin = {top: 30, right: 50, bottom: 30, left: 50};
    let drawWidth = width - (margin.left + margin.right);
    let drawHeight = height - (margin.top + margin.bottom);

    var svg = d3.select(svgRef.current)
    .attr("width", width)
    .attr("height", height)
    .append("svg")
      .attr("width", width)
      .attr("height", height)
      .style("font", "12px sans-serif")
      .style("text-anchor", "middle")
      .append('g').attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

    d3.csv(patchDataFileURL, function(data) {
      console.log("data");
      console.log(data);
      
      var color = d3.scaleOrdinal()
      .domain(["0", "1"])
      .range(["#e41a1c", "#377eb8"])

      let dimensions = ["intensity", "color", "orientation", "curvature", "center_bias", "entropy_rate", "log_spectrum", "HOG"];
      var y = {};
      for (let i in dimensions) {
        var name = dimensions[i];
        var yMin = d3.min(data, (d=>parseFloat(d[name])));
        var yMax = d3.max(data, (d=>parseFloat(d[name])));
        y[name] = d3.scaleLinear()
        .domain( [yMin, yMax] )
        .range([drawHeight, 0]);
      }

      let x = d3.scalePoint()
      .range([0, drawWidth])
      .domain(dimensions);
      
      function path(d) {
        return d3.line()(dimensions.map(function(p) { return [x(p), y[p](d[p])]; }));
      }
      
      svg.selectAll("pcPath")
      .data(data)
      .enter()
      .append("path")
        .attr("class", function(d){ return "line "+d.id })
        .attr("d", path)
        .style("fill", "none")
        .style("stroke", function(d){ return(color(String(d.label))) })
        .style("opacity", 0.5);

      
      // Draw the axis:
      svg.selectAll("pcAxis")
      // For each dimension of the dataset I add a 'g' element:
      .data(dimensions).enter()
      .append("g")
      .attr("class", "axis")
      // I translate this element to its right position on the x axis
      .attr("transform", function(d) { return "translate(" + x(d) + ")"; })
      // And I build the axis with the call function
      .each(function(d) { d3.select(this).call(d3.axisLeft().ticks(5).scale(y[d])); })
      // Add axis title
      .append("text")
        .style("text-anchor", "middle")
        .attr("y", -9)
        .text(function(d) { return d; })
        .style("fill", "black");
    });




  }, [props.patchDataFileURL]);
  
  return (
    <>
      {patchDataFileURL.length !== 0 && 
        <svg ref={svgRef}>
        </svg>
      }
    </>
  );
}

export default ParallelCoordinateChart;