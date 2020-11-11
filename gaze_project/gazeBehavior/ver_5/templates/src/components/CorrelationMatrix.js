// reference code: 
// http://plnkr.co/edit/RJk5vmROVAJGPHIPutVR?p=preview&preview
import React, { useEffect, useRef } from 'react';

function CorrelationMatrix(props) {
  const { width, height, dataURL } = props;
  const svgRef = useRef();
  const d3 = window.d3;

  useEffect(() => {
    if (typeof dataURL !== 'string' || dataURL.length === 0)
      return;

    d3.csv(dataURL, function(error, rows) {
      // console.log(rows)
      var data = [];

      rows.forEach(function(d) {
        console.log(d);
        var x = d[""];
        delete d[""];
        
        for(var prop in d) {
          var y = prop;
          var value = d[prop];
          data.push({
            x: x,
            y: y,
            value: +value
          });
        }
      });
          
      var margin = {top: 50, right: 100, bottom: 50, left: 50};
      var width = 800 - margin.left - margin.right;
      var height = 800 - margin.top - margin.bottom;
      var domain = d3.set(data.map(function(d) {
          // console.log(d);
          return d.x;
        })).values();
      var num = Math.sqrt(data.length);
      console.log(data.length);
      console.log(num);
      var color = d3.scaleLinear()
        .domain([-1, 0, 1])
        .range(["#B22222", "#fff", "#000080"]);

      var x = d3.scalePoint()
        .range([0, width])
        .domain(domain);

      var y = d3.scalePoint()
        .range([0, height])
        .domain(domain)
    
      var xSpace = x.range()[1] - x.range()[0],
      ySpace = y.range()[1] - y.range()[0];
      ySpace = y.range()[1] - y.range()[0];

      var svg = d3.select(svgRef.current)
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .style("font", "12px sans-serif")
          .style("text-anchor", "middle")
        .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      var cor = svg.selectAll(".cor")
        .data(data)
        .enter()
        .append("g")
        .attr("class", "cor")
        .attr("transform", function(d) {
          return "translate(" + x(d.x) + "," + y(d.y) + ")";
        });
        
      cor.append("rect")
        .attr("width", xSpace/10)
        .attr("height", ySpace/10)
        .attr("x", -xSpace / 20)
        .attr("y", -ySpace / 20)
        .style("fill", "none")
        .attr("stroke", "lightgray")
        .attr("stroke-width", "1px")

      cor.filter(function(d){
        var ypos = domain.indexOf(d.y);
        var xpos = domain.indexOf(d.x);
        for (var i = (ypos + 1); i < num; i++){
          if (i === xpos) return false;
        }
          return true;
        })
        .append("text")
        .attr("y", 5)
        .text(function(d) {
          if (d.x === d.y) {
            return d.x;
          } else {
            return d.value.toFixed(2);
          }
        })
        .style("fill", function(d){
          if (d.value === 1) {
            return "#000";
          } else {
            return color(d.value);
          }
        });

        cor.filter(function(d){
          var ypos = domain.indexOf(d.y);
          var xpos = domain.indexOf(d.x);
          for (var i = (ypos + 1); i < num; i++){
              if (i === xpos) return true;
          }
          return false;
        })
        .append("circle")
        .attr("r", function(d){
          return (width / (num * 2)) * (Math.abs(d.value) + 0.1);
        })
        .style("fill", function(d){
          if (d.value === 1) {
            return "#000";
          } else {
              return color(d.value);
          }
        });
            
        var aS = d3.scaleLinear()
          .range([-margin.top + 5, height + margin.bottom - 5])
          .domain([1, -1]);
                
        var yA = d3.axisRight()
          .scale(aS)
          .tickPadding(7);

        var aG = svg.append("g")
          .attr("class", "y axis")
          .call(yA)
          .attr("transform", "translate(" + (width + margin.right / 2) + " ,0)")

        var iR = d3.range(-1, 1.01, 0.01);
        var h = height / iR.length + 3;
        iR.forEach(function(d){
          aG.append('rect')
          .style('fill',color(d))
          .style('stroke-width', 0)
          .style('stoke', 'none')
          .attr('height', h)
          .attr('width', 10)
          .attr('x', 0)
          .attr('y', aS(d))
        });
    });

    
  }, []);

  return (
    <>
      {typeof dataURL === 'string' && dataURL.length > 0 &&
        <svg ref={svgRef}>
        </svg>
      }
    </>
  );
}

export default CorrelationMatrix;
