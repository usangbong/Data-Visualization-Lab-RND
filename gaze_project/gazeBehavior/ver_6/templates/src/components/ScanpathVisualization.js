// d3 code reference
// https://bl.ocks.org/rjurney/e04ceddae2e8f85cf3afe4681dac1d74
// http://bl.ocks.org/emmasaunders/c25a147970def2b02d8c7c2719dc7502

import React, { useEffect, useRef } from 'react';

function ScanpathVisualization(props) {
  const { width, height, stimulusURL, scanpathList, imageOpacity } = props;
  const svgRef = useRef();
  const d3 = window.d3;
  const colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf", "#999999"];
  useEffect(() => {
    if(stimulusURL.length == 0)
      return;
    d3.select(svgRef.current).selectAll("*").remove();
    
    // set the dimensions and margins of the graph
    var margin = {top: 5, right: 5, bottom: 5, left: 5};
    var drawWidth = width - (margin.left + margin.right);
    var drawHeight = height - (margin.top + margin.bottom);

    // var imgWidth = stiSize.width;
    // var imgHeight = stiSize.height;
    var imgWidth = stimulusURL[0].width;
    var imgHeight = stimulusURL[0].height;
    var stiWidth = drawWidth;
    var stiHeight = (imgHeight/imgWidth)*stiWidth;
    var ratio = stiWidth/imgWidth;
    if(stiWidth > drawWidth || stiHeight > drawHeight){
      stiHeight = drawHeight;
      stiWidth = (imgWidth/imgHeight)*stiHeight;
      ratio = stiHeight/imgHeight;
    }
    
    var sti_url_rnd = stimulusURL[0].url+"?"+Math.random();
    let scanpathData = [];
    for(let i=0; i<scanpathList.length; i++){
      let _fixs = [];
      for(let j=0; j<scanpathList[i].scanpath.length; j++){
        var _fix ={
          'id': scanpathList[i].scanpath[j].id,
          'clu': parseInt(scanpathList[i].scanpath[j].clu),
          'x': parseFloat(scanpathList[i].scanpath[j].x)*ratio,
          'y': parseFloat(scanpathList[i].scanpath[j].y)*ratio
        };
        _fixs.push(_fix);
      }
      let _fixsData = {
        rId: scanpathList[i].rId,
        rClu: scanpathList[i].rClu,
        scanpath: _fixs
      };
      scanpathData.push(_fixsData);
    }
    // console.log(scanpathData);

    var svg = d3.select(svgRef.current)
    .attr("width", drawWidth + margin.left + margin.right)
    .attr("height", drawHeight + margin.top + margin.bottom)
      .append("svg")
      .attr("width", drawWidth + margin.left + margin.right)
      .attr("height", drawHeight + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("image")
    .attr('x', 0)
    .attr('y', 0)
    .attr("width", stiWidth)
    .attr("height", stiHeight)
    .attr("xlink:href", sti_url_rnd)
    .attr("opacity", imageOpacity);
    
    // if(stimulusSwitch == 'on'){
    //   svg.append("image")
    //   .attr('x', margin.left)
    //   .attr('y', margin.top)
    //   .attr("width", stiWidth)
    //   .attr("height", stiHeight)
    //   .attr("xlink:href", stimulusURL);
    // }else{
    //   svg.append("rect")
    //   .attr('x', margin.left)
    //   .attr('y', margin.top)
    //   .attr("width", stiWidth)
    //   .attr("height", stiHeight)
    //   .attr("stroke", "black")
    //   .attr("stroke-width", "1px")
    //   .style("fill", "none");
    // }

    var line = d3.line()
    .x(function(d){
      return d.x;
    })
    .y(function(d){
      return d.y;
    })
    .curve(d3.curveLinear);
    // .curve(d3.curveCardinal);

    var scanpathLayer = svg.selectAll(".scanpath")
    .data(scanpathData)
    .enter()
    .append('g')
    .attr('class', 'scanpath');
    
    scanpathLayer.append("path")
    .style("fill","none")
    .style("stroke",function(d){
      if(d.rClu == 0){
        return "white";
      }else if(d.rClu == 1){
        return "red";
      }else if(d.rClu == 2 || d.rClu == 6){
        return "green";
      }else if(d.rClu == 3 || d.rClu == 4 || d.rClu == 5){
        return "blue";
      }else{
        return "black";
      }
    })
    .style("stroke-width","1px")
    .attr('d', function(d){
      return line(d.scanpath);
    });
    // scanpathLayer.append("path")
    // .style("fill","none")
    // .style("stroke", "black")
    // .style("stroke-width","1px")
    // .attr('d', function(d){
    //   return line(d);
    // });

    // console.log("scanpathData");
    // console.log(scanpathData);
    var fixationLayer = svg.selectAll(".fixPoint");
    // console.log('scanpathData');
    // console.log(scanpathData);
    for(let i=0; i<scanpathData.length; i++){
      // console.log('scanpathData[i]');
      // console.log(scanpathData[i]);
      fixationLayer
      .data(scanpathData[i].scanpath)
      .enter()
      .append('g')
      .attr('class', 'fixPoint')
      .append("circle")
      .attr("cx", function(d){return d.x;})
      .attr("cy", function(d){return d.y;})
      .attr("r", 5)
      .style("fill", function(d){
        if(d.clu == 0){
          return "white";
        }else if(d.clu == 1){
          return "red";
        }else if(d.clu == 2 || d.clu == 6){
          return "green";
        }else if(d.clu == 3 || d.clu == 4 || d.clu == 5){
          return "blue";
        }else{
          return "black";
        }
      });
    }
    
  }, [, props.stimulusURL, props.scanpathList, props.imageOpacity]);

  return (
    <>
    { stimulusURL.length != 0 &&
      <svg ref={svgRef}>
      </svg>
    }
    </>
  );
}

export default ScanpathVisualization;

