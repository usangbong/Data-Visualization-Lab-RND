// reference code: 
// http://plnkr.co/edit/RJk5vmROVAJGPHIPutVR?p=preview&preview
import React, { useEffect, useRef } from 'react';
import axios from 'axios';

function CorrelationMatrix(props) {
  const { width, height, dataURL, features, onAxisChanged } = props;
  const svgRef = useRef();
  const d3 = window.d3;
  let selectedAxis = [];

  useEffect(() => {
    if (typeof dataURL !== 'string' || dataURL.length === 0)
      return;
    d3.select(svgRef.current).selectAll("*").remove();

    d3.csv(dataURL, function(error, rows) {
      // console.log(rows)
      var data = [];

      rows.forEach(function(d) {
        // console.log(d);
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
      // console.log(data);
      
      var margin = {top: 25, right: 70, bottom: 25, left: 20};
      var drawWidth = width - margin.left - margin.right;
      var drawHeight = height - margin.top - margin.bottom;
      var domain = d3.set(data.map(function(d) {
          // console.log(d);
          return d.x;
        })).values();
      var num = Math.sqrt(data.length);
      var color = d3.scaleLinear()
        .domain([-1, 0, 1])
        .range(["#B22222", "#fff", "#000080"]);

      var x = d3.scalePoint()
        .range([0, drawWidth])
        .domain(domain);

      var y = d3.scalePoint()
        .range([0, drawHeight])
        .domain(domain)
    
      var xSpace = x.range()[1] - x.range()[0],
      ySpace = y.range()[1] - y.range()[0];
      // ySpace = y.range()[1] - y.range()[0];
      // console.log("x.range: "+x.range());
      // console.log("xSpace: "+xSpace);
      // console.log("ySpace: "+ySpace);
      // console.log("xSpace/10: "+xSpace/10);
      // console.log("-xSpace/(12*2): "+(-xSpace/((num-1)*2)));
      // console.log(features);

      var svg = d3.select(svgRef.current)
        .attr("width", drawWidth + margin.left + margin.right)
        .attr("height", drawHeight + margin.top + margin.bottom)
        .append("svg")
          .attr("width", drawWidth + margin.left + margin.right)
          .attr("height", drawHeight + margin.top + margin.bottom)
          .style("font", "9px sans-serif")
          .style("font-weight", "bold")
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
        .attr("width", xSpace/(num-1))
        .attr("height", ySpace/(num-1))
        .attr("x", -xSpace/((num-1)*2))
        .attr("y", -ySpace/((num-1)*2))
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
        return (drawWidth / (num * 2)) * (Math.abs(d.value) + 0.1);
      })
      .style("fill", function(d){
        if (d.value === 1) {
          return "#000";
        } else {
            return color(d.value);
        }
      });

      d3.selectAll(".cor text")
        .on('click', function(d){
          if(selectedAxis.length === 0){
            selectedAxis = [];
            if(d.x !== d.y){
              selectedAxis = [d.x, d.y];
            }
          }else if(selectedAxis.length === 2){
            if(selectedAxis[0] === d.x && selectedAxis[1] === d.y){
              selectedAxis = [];
            }else{
              if(d.x === d.y){
                selectedAxis = [];
              }else{
                selectedAxis = [];
                selectedAxis = [d.x, d.y];
              }
            }
          }

          svg.selectAll(".cor rect").transition()
            .attr("stroke", function(d){
              if(selectedAxis.length === 2){
                if(selectedAxis[0] === d.x && selectedAxis[1] === d.y){
                  return "black";
                }else{
                  return "lightgray";
                }
              }else{
                return "lightgray";
              }
            })
            .style("fill", function(d){
              if(selectedAxis.length === 2){
                if(selectedAxis[0] === d.x && selectedAxis[1] === d.y){
                  return "#969696";
                }else{
                  return "none";
                }
              }else{
                return "none";
              }
            });

            if(selectedAxis.length === 2){
              sendSelectedAxis(selectedAxis[0], selectedAxis[1]);
              onAxisChanged();
            }
        });

      function sendSelectedAxis(_f1, _f2){
        const _data = new FormData();
        _data.set('feature_1', _f1);
        _data.set('feature_2', _f2);
        axios.post(`http://${window.location.hostname}:5000/api/correlationMatrix/selectedAxis`, _data)
        .then(response => {
          if (response.data.status === 'success') {
              console.log('selected features saved');
          } else if (response.data.status === 'failed') {
              alert(`Failed save selected features - ${response.data.reason}`);
          }
        }).catch(error => {
          alert(`Error - ${error.message}`);
        });
      }
      
      var aS = d3.scaleLinear()
        .range([-margin.top + 5, drawHeight + margin.bottom - 5])
        .domain([1, -1]);
              
      var yA = d3.axisRight()
        .scale(aS)
        .tickPadding(7);

      var aG = svg.append("g")
        .attr("class", "y axis")
        .call(yA)
        .attr("transform", "translate(" + (drawWidth + margin.right / 2) + " ,0)")

      var iR = d3.range(-1, 1.01, 0.01);
      var h = drawHeight / iR.length + 3;
      iR.forEach(function(d){
        aG.append('rect')
        .style('fill',color(d))
        .style('stroke-width', 0)
        .style('stroke', 'none')
        .attr('height', h)
        .attr('width', 10)
        .attr('x', 0)
        .attr('y', aS(d))
      });
    });

    
  }, [props.dataURL, props.features]);

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
