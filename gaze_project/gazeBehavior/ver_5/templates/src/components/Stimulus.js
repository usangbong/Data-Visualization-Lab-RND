// d3 code reference
// https://bl.ocks.org/rjurney/e04ceddae2e8f85cf3afe4681dac1d74
import React, { useEffect, useRef } from 'react';

function Stimulus(props) {
  const { width, height, stimulusData, stimulusPath, selectedPatchOrder, patchCluster } = props;
  const svgRef = useRef();
  const d3 = window.d3;
  const colors = ["#a6cee3", "#fb9a99", "#fdbf6f", "#cab2d6", "#b15928", "#b2df8a", "#ffff99", "#1f78b4", "#e31a1c", "#ff7f00", "#33a02c", "#6a3d9a"];
  const PATCH_SIZE = 50;
  useEffect(() => {
    if(stimulusPath.length === 0 || stimulusPath.length === 0)
      return;
    console.log("stimulusData");
    console.log(stimulusData);
    console.log("stimulusPath");
    console.log(stimulusPath);
    console.log("patchCluster");
    console.log(patchCluster);
    d3.select(svgRef.current).selectAll("*").remove();
    
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 5, bottom: 10, left: 5};
    var drawWidth = width - margin.left - margin.right;
    var drawHeight = height - margin.top - margin.bottom;

    var imgWidth = 1920;
    var imgHeight = 1080;
    var stiWidth = drawWidth- margin.left - margin.right;
    var stiHeight = (imgHeight/imgWidth)*stiWidth;
    var ratio = stiWidth/imgWidth;
    let patchSize = PATCH_SIZE*ratio;

    let fixations = [];
    for(let i=0; i<stimulusData.length; i++){
      var _fix = {
        "clu": -1,
        "x": (stimulusData[i].x*ratio)+margin.left,
        "y": (stimulusData[i].y*ratio)+margin.top,
        "px": (stimulusData[i].x*ratio)+margin.left-patchSize/2,
        "py": (stimulusData[i].y*ratio)+margin.top-patchSize/2,
      };
      if(i==selectedPatchOrder){
        _fix.clu = patchCluster;
      }
      fixations.push(_fix);
    }
    
    let saccadeData = [];
    for(let i=0; i<fixations.length-1; i++){
      let _str = fixations[i];
      let _end = fixations[i+1];
      let _s = {
        "s": _str,
        "e": _end
      }
      saccadeData.push(_s);
    }
    

    var svg = d3.select(svgRef.current)
      .attr("width", drawWidth + margin.left + margin.right)
      .attr("height", drawHeight + margin.top + margin.bottom)
        .append("svg")
        .attr("width", drawWidth + margin.left + margin.right)
        .attr("height", drawHeight + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var stimulus = svg.selectAll(".sti")
      .data(fixations)
      .enter()
      .append("g")
      .attr("class", "sti")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
    stimulus.append("image")
      .attr("width", stiWidth)
      .attr("height", stiHeight)
      .attr("xlink:href", stimulusPath);

    var sFrame = svg.selectAll(".sFrame")
      .data(fixations)
      .enter()
      .append("g")
      .attr("class", "sFrame")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    sFrame.append("rect")
      .attr("width", stiWidth)
      .attr("height", stiHeight)
      .attr("stroke", "black")
      .attr("stroke-width", "1px")
      .style("fill", "none");
    
    var saccade = svg.selectAll(".saccade")
      .data(saccadeData)
      .enter()
      .append("g")
      .attr("class", "saccade")
    
    saccade.append("line")
      .attr("stroke", "black")
      .attr("stroke-width", "1px")
      .attr("x1", function (d) { return d.s.x; } )
      .attr("y1", function (d) { return d.s.y; } )
      .attr("x2", function (d) { return d.e.x; } )
      .attr("y2", function (d) { return d.e.y; } )
      .attr("r", 5)

    var fixation = svg.selectAll(".fixation")
      .data(fixations)
      .enter()
      .append("g")
      .attr("class", "fixation")

    fixation.append("circle")
      .attr("cx", function(d){ return d.x; } )
      .attr("cy", function(d) { return d.y; } )
      .attr("r", 5)
      .style("fill", function(d){
        if(d.clu == patchCluster){
          return colors[d.clu];
        }else{
          return "black";
        }
      })
      .style("opacity", 0.5);

    var sPatch = svg.selectAll(".sPatch")
      .data(fixations)
      .enter()
      .append("g")
      .attr("class", "sPatch")
      .attr("transform", function(d) {
        return "translate(" + d.px + "," + d.py + ")";
      });
    
    sPatch.append("rect")
      .attr("width", patchSize)
      .attr("height", patchSize)
      .attr("stroke", function(d){
        if(d.clu == patchCluster){
          return colors[d.clu];
        }else{
          return "none";
        }
      })
      .attr("stroke-width", "2px")
      .style("fill", "none");
    
  }, [, props.stimulusData, props.stimulusPath, props.patchCluster]);

  return (
    <>
      {stimulusPath.length > 0 && stimulusPath.length > 0 &&
        <svg ref={svgRef}>
        </svg>
      }
    </>
  );
}

export default Stimulus;

