import React, { useEffect, useRef } from 'react';

function HumanFixationMap(props) {
  const { width, height, humanFixationMapURL, patchDataList } = props;
  const svgRef = useRef();
  const d3 = window.d3;
  const PATCH_SIZE = 20;
  
  useEffect(() => {
    if(humanFixationMapURL.length == 0)
      return;
    d3.select(svgRef.current).selectAll("*").remove();
    
    // set the dimensions and margins of the graph
    var margin = {top: 0, right: 0, bottom: 0, left: 0};
    var drawWidth = width - (margin.left + margin.right);
    var drawHeight = height - (margin.top + margin.bottom);

    // var imgWidth = stiSize.width;
    // var imgHeight = stiSize.height;
    var imgWidth = humanFixationMapURL[0].width;
    var imgHeight = humanFixationMapURL[0].height;
    var stiWidth = drawWidth;
    var stiHeight = (imgHeight/imgWidth)*stiWidth;
    var ratio = stiWidth/imgWidth;
    if(stiWidth > drawWidth || stiHeight > drawHeight){
      stiHeight = drawHeight;
      stiWidth = (imgWidth/imgHeight)*stiHeight;
      ratio = stiHeight/imgHeight;
    }
    // console.log("RAW DATA LIST");
    // console.log(patchDataList);

    let patchData = [];
    for(let i=0; i<patchDataList.length; i++){
      let box = {
        x: parseFloat((patchDataList[i][1]-PATCH_SIZE/2)*ratio),
        y: parseFloat((patchDataList[i][2]-PATCH_SIZE/2)*ratio),
        label: patchDataList[i][3]
      };
      patchData.push(box);
    }

    var url_rnd = humanFixationMapURL[0].url+"?"+Math.random();
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
    .attr("xlink:href", url_rnd);

    var patchFrame = svg.selectAll(".opFrame")
    .data(patchData)
    // .data(scanpathData)
    .enter()
    .append("g")
    .attr("class", "opFrame")
    .attr("transform", function(d) {
      return "translate(" + d.x + "," + d.y + ")";
    });

    patchFrame.append('rect')
    .attr("width", PATCH_SIZE*ratio)
    .attr("height", PATCH_SIZE*ratio)
    .style("fill", "none")
    .attr("stroke", function(d){
      if(d.label == 0){
        return "blue";
      }else if(d.label == 1){
        return "red";
      }else{
        return "black";
      }
    })
    .attr("stroke-width", "2px");

    
    
  }, [, props.humanFixationMapURL, props.patchDataList]);

  return (
    <>
    { humanFixationMapURL.length != 0 &&
      <svg ref={svgRef}>
      </svg>
    }
    </>
  );
}

export default HumanFixationMap;

