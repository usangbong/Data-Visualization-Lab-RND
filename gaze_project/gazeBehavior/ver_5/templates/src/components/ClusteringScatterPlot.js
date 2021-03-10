import React, { useEffect, useRef } from 'react';
import axios from 'axios';

function ClusteringScatterPlot(props) {
  const { width, height, dataURL} = props;
  const svgRef = useRef();
  const d3 = window.d3;
  const colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf", "#999999"];
  let mouseDownLocation = [0, 0];

  let selectBox = [{x:0, y:0, w:0, h:0}];

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
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    let scatterData = [];
    // load data
    axios.get(dataURL)
    .then(response => {
      // console.log(response.data);
      for (let value of response.data.split('\n')){
        if (value.length > 0){
          if(value.split(",")[0] === "id"){
            continue;
          }
          var _row = {
            "id": parseInt(value.split(",")[0]), 
            "duration": parseFloat(value.split(",")[1]),
            "length": parseFloat(value.split(",")[2]),
            "x": parseFloat(value.split(",")[3]),
            "y": parseFloat(value.split(",")[4]),
            "clu": parseInt(value.split(",")[5])
          };
          scatterData.push(_row);
        }
      }
      // console.log("scatter data test");
      // console.log(scatterData);
    })
    .then(()=>{
      // Add X axis
      var xMin = d3.min(scatterData, (d => parseFloat(d.x)));
      var xMax = d3.max(scatterData, (d => parseFloat(d.x)));
      var x = d3.scaleLinear()
        .domain([xMin, xMax])
        .range([ 0, drawWidth ]);
      // svg.append("g")
      //   .attr("class", "xaxis")
      //   .attr("transform", "translate(0," + drawHeight + ")")
      //   .call(d3.axisBottom(x));
      // Add Y axis
      var yMin = d3.min(scatterData, (d => parseFloat(d.y)));
      var yMax = d3.max(scatterData, (d => parseFloat(d.y)));
      var y = d3.scaleLinear()
        .domain([yMin, yMax])
        .range([ drawHeight, 0]);
      // svg.append("g")
      // .attr("class", "yaxis")
      // .call(d3.axisLeft(y));
      
      // Add dots
      var dots = svg.append('g')
      .selectAll("dot") 
      .data(scatterData)
      .enter()
      .append("circle")
        .attr("class", "point")
        .attr("cx", function (d) { return x(d.x); } )
        .attr("cy", function (d) { return y(d.y); } )
        .attr("r", 1.5)
        .style("fill", function (d) {return colors[parseInt(d.clu)]});

      var brushBox = d3.select(svgRef.current)
      .on('mousedown', mousedown)
      .on('mouseup', mouseup)
      .append("g")
      .attr("width", drawWidth)
      .attr("height", drawHeight)
        .selectAll(".brushBox")
        .data(selectBox)
        .enter()
          .append('g')
          .attr("class", "brushBox");

      brushBox.append("rect")
      .attr("x", function(d){return d.x})
      .attr("y", function(d){return d.y})
      .attr("width", function(d){return d.w})
      .attr("height", function(d){return d.h})
      .style("fill", "gray")
      .attr("stroke", "black")
      .attr("stroke-width", "1px")
      .style("opacity", 0.2);

      function mousedown(){
        var m = d3.mouse(this);
        mouseDownLocation[0] = m[0];
        mouseDownLocation[1] = m[1];
        // console.log("down: "+m[0]+", "+m[1]);
        // console.log(mouseDownLocation);
        d3.select(svgRef.current).on("mousemove", mousemove);
      }
  
      function mousemove(){
        var m = d3.mouse(this);
        var _w = m[0] - mouseDownLocation[0];
        var _h = m[1] - mouseDownLocation[1];
        // console.log("move: "+m[0]+", "+m[1]+" down: "+ mouseDownLocation[0] +", "+mouseDownLocation[1]);
        if(_w<0){
          mouseDownLocation[0] = mouseDownLocation[0] + _w;
          _w = _w*-1;
        }
        if(_h<0){
          mouseDownLocation[1] = mouseDownLocation[1] + _h;
          _h = _h*-1;
        }

        var updateBox = [{x: mouseDownLocation[0], y: mouseDownLocation[1], w: _w, h: _h}];
        selectBox = updateBox;
        // console.log(selectBox);

        d3.selectAll(".brushBox rect")
        .attr("x", mouseDownLocation[0])
        .attr("y", mouseDownLocation[1])
        .attr("width", function(d){
          return _w;
        })
        .attr("height", function(d){
          return _h;
        });
      }
  
      function mouseup(){
        d3.select(svgRef.current).on("mousemove", null)
      }
      
      d3.selectAll('.point')
      .on('click', function(d){
        var _x = d3.mouse(this)[0];
        var _y = d3.mouse(this)[1];
        console.log(_x+", "+_y);
        
        var pieData = {a: 20, b: 20, c: 20, d:20, e:20};
        var radius = 10;
        var color = d3.scaleOrdinal()
        .domain(pieData)
        .range(["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00"]);
        var pie = d3.pie()
        .value(function(d){return d.value});
        var data_ready = pie(d3.entries(pieData));

        var pallete = svg.append('g')
        .attr("transform", "translate(" + _x + "," + _y + ")")
        .selectAll('whatever')
        .data(data_ready)
        .enter()
        .append('path')
        .attr('d', d3.arc()
          .innerRadius(8)
          .outerRadius(20)
        )
        .attr('fill', function(d){ return(color(d.data.key)) })
        .attr("stroke", "black")
        .style("stroke-width", "2px")
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

export default ClusteringScatterPlot;

