// d3 code reference
// https://bl.ocks.org/rjurney/e04ceddae2e8f85cf3afe4681dac1d74
import React, { useEffect, useRef } from 'react';

function Patch(props) {
  const { width, height, patchURL, patchCluster, patchFeatureImageURLs, patchSelectedFeature, feature_define, dataset, participant, filterName, selectedPatchId } = props;
  const svgRef = useRef();
  const d3 = window.d3;
  const colors = ["#a6cee3", "#fb9a99", "#fdbf6f", "#cab2d6", "#b15928", "#b2df8a", "#ffff99", "#1f78b4", "#e31a1c", "#ff7f00", "#33a02c", "#6a3d9a"];
  
  useEffect(() => {
    if(patchURL.length === 0 || patchCluster < 0)
      return;
    // console.log("patchURL");
    // console.log(patchURL);
    // console.log("patchCluster");
    // console.log(patchCluster);
    d3.select(svgRef.current).selectAll("*").remove();
    
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 5, bottom: 10, left: 5};
    var drawWidth = width - margin.left - margin.right;
    var drawHeight = height - margin.top - margin.bottom;
    var patchSize = drawWidth - margin.left - margin.right;

    let selectedPatch = [];
    let _patchURL = `http://${window.location.hostname}:5000`+patchURL[1]+"?"+Math.random();
    if(patchSelectedFeature != -1){
      let _featType = "";
      for(let i=0; i<feature_define.length; i++){
        if(patchSelectedFeature == feature_define[i][0]){
          _featType=feature_define[i][2]
        }
      }
      _patchURL = `http://${window.location.hostname}:5000`+"/static/data/"+dataset+"/"+participant+"/patch/"+filterName+"/features/"+selectedPatchId+"/"+_featType+".png?"+Math.random();
    }else{
      _patchURL = `http://${window.location.hostname}:5000`+patchURL[1]+"?"+Math.random();
    }
    let _patch = {
      "clu": patchCluster,
      "patch": _patchURL
    };
    selectedPatch.push(_patch);

    var svg = d3.select(svgRef.current)
      .attr("width", drawWidth + margin.left + margin.right)
      .attr("height", drawHeight + margin.top + margin.bottom)
        .append("svg")
        .attr("width", drawWidth + margin.left + margin.right)
        .attr("height", drawHeight + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var oPatch = svg.selectAll(".oPatch")
      .data(selectedPatch)
      .enter()
      .append("g")
      .attr("class", "oPatch")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
      oPatch.append("image")
      .attr("width", patchSize)
      .attr("height", patchSize)
      .attr("xlink:href", function(d){
        return d.patch;
      });

    var pFrame = svg.selectAll(".pFrame")
      .data(selectedPatch)
      .enter()
      .append("g")
      .attr("class", "pFrame")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    pFrame.append("rect")
      .attr("width", patchSize)
      .attr("height", patchSize)
      .attr("stroke", function(d){
        return colors[d.clu];
      })
      .attr("stroke-width", "4px")
      .style("fill", "none");
    
  }, [, props.patchURL, props.patchCluster, props.patchFeatureImageURLs, props.patchSelectedFeature, props.feature_define]);

  return (
    <>
      
      {patchURL.length > 0 && patchCluster >= 0 &&
        <svg ref={svgRef}>
        </svg>
      }
    </>
  );
}

export default Patch;
