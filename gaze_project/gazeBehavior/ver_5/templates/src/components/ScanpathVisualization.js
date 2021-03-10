// d3 code reference
// https://bl.ocks.org/rjurney/e04ceddae2e8f85cf3afe4681dac1d74
// http://bl.ocks.org/emmasaunders/c25a147970def2b02d8c7c2719dc7502

import React, { useEffect, useRef } from 'react';

function ScanpathVisualization(props) {
  const { width, height, scanpathList, stimulusSwitch, stimulusURL } = props;
  const svgRef = useRef();
  const d3 = window.d3;
  const colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf", "#999999"];
  useEffect(() => {
    if( scanpathList.length == 0 || stimulusSwitch == null)
      return;
    d3.select(svgRef.current).selectAll("*").remove();
    
    // set the dimensions and margins of the graph
    var margin = {top: 5, right: 5, bottom: 5, left: 5};
    var drawWidth = width - margin.left - margin.right;
    var drawHeight = height - margin.top - margin.bottom;

    // var imgWidth = stiSize.width;
    // var imgHeight = stiSize.height;
    var imgWidth = 1920;
    var imgHeight = 1080;
    var stiWidth = drawWidth;
    var stiHeight = (imgHeight/imgWidth)*stiWidth;
    var ratio = stiWidth/imgWidth;

    // for(let i=0; i<scanpathList.length; i++){
    //   let _fixs = [];
    //   for(let j=0; j<scanpathList[i].length; j++){
    //     var _fix ={
    //       'id': 0,
    //       'x': (scanpathList[i][j].x*ratio)+margin.left,
    //       'y': (scanpathList[i][j].y*ratio)+margin.top
    //     };
    //     _fixs.push(_fix);
    //   }
    // }

    var svg = d3.select(svgRef.current)
    .attr("width", drawWidth + margin.left + margin.right)
    .attr("height", drawHeight + margin.top + margin.bottom)
      .append("svg")
      .attr("width", drawWidth + margin.left + margin.right)
      .attr("height", drawHeight + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    if(stimulusSwitch == 'on'){
      svg.append("image")
      .attr('x', margin.left)
      .attr('y', margin.top)
      .attr("width", stiWidth)
      .attr("height", stiHeight)
      .attr("xlink:href", `http://${window.location.hostname}:5000/static/access/temp.jpg?`+Math.random());
    }else{
      svg.append("rect")
      .attr('x', margin.left)
      .attr('y', margin.top)
      .attr("width", stiWidth)
      .attr("height", stiHeight)
      .attr("stroke", "black")
      .attr("stroke-width", "1px")
      .style("fill", "none");
    }

    var line = d3.line()
    .x(function(d){
      // return d.x;
      return (d.x*ratio)+margin.left;
    })
    .y(function(d){
      // return d.y;
      return (d.y*ratio)+margin.top;
    })
    .curve(d3.curveLinear);
    // .curve(d3.curveCardinal);

    var scanpathLayer = svg.selectAll(".scanpath")
    .data(scanpathList)
    .enter()
    .append('g')
    .attr('class', 'scanpath');
    
    scanpathLayer.append("path")
    .style("fill","none")
    .style("stroke",function(d){
      if(d.clu == 0 || d.clu == 4){
        return "red";
      }else{
        return "black";
      }
    })
    .style("stroke-width","1px")
    .attr('d', function(d){
      console.log(d);
      return line(d.scanpath);
    });

    // var fixationLayer = svg.selectAll(".fixPoint")
    // .data(scanpathList)
    // .enter()
    // .append('g')
    // .attr('class', 'fixPoint');

    // fixationLayer.append("circle")
    // .attr("cx", function(d, i){ console.log(d); return d.x;})
    // .attr("cy", function(d, i){ return d.y;})
    // .attr("r", 5)
    // .style("fill","black");
    


  }, [, props.scanpathList, props.stimulusSwitch]);

  return (
    <>
    { scanpathList.length > 0 && stimulusSwitch != null &&
      <svg ref={svgRef}>
      </svg>
    }
    </>
  );
}

export default ScanpathVisualization;

