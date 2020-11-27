import React, { useEffect, useRef } from 'react';
// import axios from 'axios';

function PatchTable(props) {
  // const { width, height, data } = props;
  const svgRef = useRef();
  const d3 = window.d3;
  // col, row
  const dataframe = [11, 5];

  // input col, row length in dataframe
  //dataframe = [C, R];
  let frameBox = [];
  let cluFrame = [];
  let fixFrame = [];
  let viewFrame = [];
  // let boxSize = width/dataframe[0];
  let tmpWidth = 300;
  let tmpHeight = 300;
  let boxSize = {
    "width": tmpWidth/dataframe[0],
    "height": tmpHeight/dataframe[1]
  };

  let patches = [];
  let patchSize = (tmpWidth-(2*5)-boxSize.width)/10;
  let patchData = [];

  // generate temprary patches
  for(let i=0; i<dataframe[1]; i++){
    for(let j=0; j<10; j++){
      let _patch = {
        "class": i,
        "id": j,
        "url": ""
      };
      patches.push(_patch);
    }
  }

  for(let i=0; i<dataframe[0]; i++){
    for(let j=0; j<dataframe[1]; j++){
      let _tag = "";
      if(i === 0 && j === 0){
        continue;
      }else{
        if(i === 0){
          _tag = "clusters";
        }else if(i !== 0 && j === 0){
          _tag = "fixations";
        }else{
          continue;
        }
      }
      let _x = i*boxSize.width;
      let _y = j*boxSize.height;
      let _box = {
        "tag": _tag,
        "x": _x,
        "y": _y,
        "width": boxSize.width,
        "height": boxSize.height
      };
      frameBox.push(_box);
      if(i===0){
        _tag = "patches";
        let _x = (i+1)*boxSize.width;
        let _y = j*boxSize.height;
        let _box = {
          "tag": _tag,
          "x": _x,
          "y": _y,
          "width": tmpWidth-boxSize.width,
          "height": boxSize.height
        };
        frameBox.push(_box);
      }
    }
  }

  for(let i=0; i<frameBox.length; i++){
    let _tag = frameBox[i].tag;
    if(_tag === "clusters"){
      cluFrame.push(frameBox[i]);
    }else if(_tag === "fixations"){
      fixFrame.push(frameBox[i]);
    }else if(_tag === "patches"){
      viewFrame.push(frameBox[i]);
    }else{
      console.log("error");
    }
  }

  for(let i=0; i<dataframe[1]; i++){
    for(let j=0; j<patches.length; j++){
      if(i+1 !== patches[j].class){
        continue;
      }
      let _padding = 5;
      let _x = _padding + boxSize.width + (patches[j].id*patchSize)/2;
      let _y = _padding + ((i+1)*boxSize.height);
      let _patch = {
        "class": patches[j].class,
        "id": patches[j].id,
        "url": patches[j].url,
        "x": _x,
        "y": _y,
        "width": patchSize,
        "height": patchSize
      };
      patchData.push(_patch);
    }
  }
  
  // console.log("patchData");
  // console.log(patchData);


  useEffect(() => {
    // if (typeof data !== 'object' || data.length === 0)
    //   return;

    var margin = {top: 10, right: 50, bottom: 20, left: 30},
      drawWidth = 1000 - margin.left - margin.right,
      drawHeight = 1000 - margin.top - margin.bottom;
      
    var svg = d3.select(svgRef.current)
      .attr('width', drawWidth)
      .attr('height', drawHeight)
      .append("svg")
        .attr('width', drawWidth)
        .attr('height', drawHeight)
        .style("font", "12px sans-serif")
        .style("text-anchor", "middle")
        .append('g').attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");
    
    var clus = svg.selectAll(".clu")
      .data(cluFrame)
      .enter()
      .append("g")
      .attr("class", "clu")
      .attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
      });

    clus.append("rect")
      .attr("width", boxSize.width)
      .attr("height", boxSize.height)
      .style("fill", "lightgray")
      .attr("stroke", "black")
      .attr("stroke-width", "1px")

    clus.append("text")
      .attr("x", function(d){ return d.width/2})
      .attr("y", function(d){ return 5+d.height/2})
      .text(function(d, i){ return "c_"+i})
      .style("fill", "black");

    var fixs = svg.selectAll(".fixs")
      .data(fixFrame)
      .enter()
      .append("g")
      .attr("class", "fixs")
      .attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
      });

    fixs.append("rect")
      .attr("width", boxSize.width)
      .attr("height", boxSize.height)
      .style("fill", "lightgray")
      .attr("stroke", "black")
      .attr("stroke-width", "1px")

      fixs.append("text")
      .attr("x", function(d){ return d.width/2})
      .attr("y", function(d){ return 5+d.height/2})
      .text(function(d, i){ return "f_"+i})
      .style("fill", "black");

    var pats = svg.selectAll(".view")
      .data(viewFrame)
      .enter()
      .append("g")
      .attr("class", "view")
      .attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
      });
      
    pats.append("rect")
      .attr("width", tmpWidth - boxSize.width)
      .attr("height", boxSize.height)
      .style("fill", "none")
      .attr("stroke", "black")
      .attr("stroke-width", "1px")

    var patch = svg.selectAll(".patch")
      .data(patchData)
      .enter()
      .append("g")
      .attr("class", "patch")
      .attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
      });

    patch.append("image")
      .attr("width", patchSize)
      .attr("height", patchSize)
      .attr("xlink:href", "http://localhost:5000/static/access/MIT300/Action/018/005.png")
      .style("fill", function(d){
        if(d.class === 0){
          return "#fbb4ae";
        }else if(d.class === 1){
          return "#b3cde3";
        }else if(d.class === 2){
          return "#ccebc5";
        }else if(d.class === 3){
          return "#decbe4";
        }else if(d.class === 4){
          return "#fed9a6";
        }else{
          return "gray";
        }
      }).style("opacity", 1.0)
      .attr("stroke", "black")
      .attr("stroke-width", "1px")
      
    
  }, []);

  return (
    <>
      <svg ref={svgRef}>
      </svg>
      {/* {typeof data === 'object' && data.length > 0 &&
        <svg ref={svgRef}>
        </svg>
      } */}
    </>
  );
}

export default PatchTable;
