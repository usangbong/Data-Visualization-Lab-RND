import React, { useEffect, useRef } from 'react';

function PatchVisualization(props) {
  const { width, height, patchURLs, patchList, patchDrawFlag, patchBoxOpacity, colorEncoding, selectedObserver } = props;
  const svgRef = useRef();
  const d3 = window.d3v4;
  const colores_g = ["#109618", "#ff9900", "#990099", "#dd4477", "#0099c6", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac", "#3366cc", "#dc3912"];
  const PATCH_SIZE = 20;
  const PATCH_DRAW_LENGTH = 40;
  let selectPatchID = "";
  let prevPos = [0, 0];
  useEffect(() => {
    if (patchURLs.length === 0)
      return;
    d3.select(svgRef.current).selectAll("*").remove();
    
    let margin = {top: 5, right: 5, bottom: 5, left: 5};
    let drawWidth = width - (margin.left + margin.right);
    let drawHeight = height - (margin.top + margin.bottom);

    // console.log(patchURLs);
    // console.log(patchList);
    let allObserverList = [];
    for(let i=0; i<patchList.length; i++){
      allObserverList.push(patchList[i][0].split("/")[3].split(".")[0]);
    }
    let set = new Set(allObserverList);
    let observerList = [...set];
    
    let aggregatedPatchImageLength = 0;
    let patchData = [];
    let patchCount = 0;
    for(let i=0; i<patchList.length; i++){
      let _id = patchList[i][0].split("/")[3].split(".")[0];
      let _idIdx = 0;
      for(let j=0; j<observerList.length; j++){
        if(_id == observerList[j]){
          _idIdx = j;
          break;
        }
      }
      let patch = {
        id: _idIdx,
        x: patchList[i][1],
        y: patchList[i][2],
        clu: patchList[i][3],
        index: patchCount,
        order: i,
        observer: _id
      };
      patchData.push(patch);
      patchCount = patchCount+1;
    }
    aggregatedPatchImageLength = PATCH_SIZE*patchCount;
    
    var xMin = d3.min(patchData, (d=>parseFloat(d.x)));
    var xMax = d3.max(patchData, (d=>parseFloat(d.x)));
    var x = d3.scaleLinear()
    .domain([xMin, xMax])
    .range([PATCH_DRAW_LENGTH, drawWidth-PATCH_DRAW_LENGTH]);

    var yMin = d3.min(patchData, (d=>parseFloat(d.y)));
    var yMax = d3.max(patchData, (d=>parseFloat(d.y)));
    var y = d3.scaleLinear()
    .domain([yMin, yMax])
    .range([drawHeight-PATCH_DRAW_LENGTH, PATCH_DRAW_LENGTH]);

    var svg = d3.select(svgRef.current)
    .attr("width", width)
    .attr("height", height)
    .append("svg")
      .attr("width", drawWidth)
      .attr("height", drawHeight)
      .style("font", "12px sans-serif")
      .style("text-anchor", "middle")
      .append('g').attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");
    
    var patchFrame = svg.selectAll(".pFrame")
    .data(patchData)
    .enter()
    .append("g")
    .attr("class", "pFrame")
    .attr("transform", function(d) {
      let _x = x(d.x) - PATCH_DRAW_LENGTH/2;
      let _y = y(d.y) - PATCH_DRAW_LENGTH/2;
      return "translate(" + _x + "," + _y + ")";
    });

    patchFrame.append('rect')
    .attr("width", PATCH_DRAW_LENGTH)
    .attr("height", PATCH_DRAW_LENGTH)
    .style("fill", function(d){ 
      if(patchDrawFlag == "box"){
        return colorEncoding[d.clu];
      }else if(patchDrawFlag == "observer"){
        if(d.id < colores_g.length){
          return colores_g[d.id];
        }else{
          let mIdx = d.id - colores_g.length;
          return colorEncoding[mIdx];
        }
      }else{
        return "white";
      }
    })
    .attr("stroke", function(d){ return colorEncoding[d.clu] })
    .attr("stroke-width", "3px")
    .attr("opacity", function(d){
      if(selectedObserver.length == 0){
        return patchBoxOpacity;
      }else{
        if(selectedObserver[1] == d.observer){
          return 1;
        }else{
          if(patchBoxOpacity == 1){
            return 0.3;
          }else{
            return patchBoxOpacity;
          }
        }
      }
    });

    if(patchDrawFlag == "image"){
      var patch = svg.selectAll(".patch")
      .data(patchData)
      // .data(scanpathData)
      .enter()
      .append("g")
      .attr("class", "patch")
      .attr("transform", function(d) {
        let _x = x(d.x) - PATCH_DRAW_LENGTH/2;
        let _y = y(d.y) - PATCH_DRAW_LENGTH/2;
        return "translate(" + _x + "," + _y + ")";
      })
      .on('mousedown', function(d){
        selectPatchID = "bar"+String(d.index);
        // console.log(selectPatchID);
        d3.select(svgRef.current).selectAll('.patch').on("mousemove", mousemove);
      })
      .on('mouseup', function(d){
        selectPatchID = "";
        // console.log(selectPatchID);
        d3.select(svgRef.current).selectAll('.patch').on("mousemove", null);
      });

      function mousemove(){
        if(selectPatchID !== ""){
          var m = d3.mouse(this);
          var _x = m[0];
          var _y = m[1];
          if(prevPos[0] == 0 && prevPos[1]==0){
            prevPos=[_x, _y];
          }
          var _trs = "translate(" + _x + "," + _y + ")";
          // console.log("move: "+m[0]+", "+m[1]);
          for(let i=0; i<patchData.length; i++){
            if("bar"+String(patchData[i].index) == selectPatchID){
              patchData[i].x = patchData[i].x+_x-(PATCH_SIZE/2);
              patchData[i].y = patchData[i].y+_y-(PATCH_SIZE/2);
              break;
            }
          }
          // for(let i=0; i<scanpathData.length; i++){
          //   if("bar"+String(scanpathData[i].index) == selectPatchID){
          //     scanpathData[i].x = scanpathData[i].x+_x-(PATCH_SIZE/2);
          //     scanpathData[i].y = scanpathData[i].y+_y-(PATCH_SIZE/2);
          //     break;
          //   }
          // }

          // d3.selectAll(".pFrame rect").transition()
          // .attr("transform", function(d){
          //   if("bar"+String(d.index) == selectPatchID){
          //     return _trs;
          //   }
          // });
          // d3.selectAll(".pFrame rect").transition()
          // .attr("transform", function(d) {
          //   if("bar"+String(d.index) == selectPatchID){
          //     // return "translate(" + d.x + "," + d.y + ")";
          //     return _trs;
          //   }
          // });
          d3.selectAll(".pFrame")
          .attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
          });

          d3.selectAll(".patch")
          .attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
          });
          // d3.selectAll(".patch "+selectPatchID).attr("transform", _trs);
        }
        prevPos=[_x, _y];
      }

      patch.append('symbol')
      .attr("id", function(d){ return "bar"+String(d.index)})
      .attr("viewBox", function(d){
        let _xPos = d.index*PATCH_SIZE
        let _rVal = String(_xPos)+" 0 20 20"
        return _rVal
      })
      .append("image")
      .attr("width", String(aggregatedPatchImageLength)+"px")
      .attr("height", "20px")
      .attr("xlink:href", patchURLs)
      .attr('x', 0)
      .attr('y', 0);

      patch.append('use')
      .attr("xlink:href", function(d){ return "#bar"+String(d.index)})
      .attr('width', PATCH_DRAW_LENGTH)
      .attr('height', PATCH_DRAW_LENGTH)
      .attr('x', 0)
      .attr('y', 0);
    }
    

  }, [props.patchURLs, props.patchList, props.patchDrawFlag, props.patchBoxOpacity ,props.colorEncoding, props.selectedObserver]);
  
  return (
    <>
      {patchURLs.length !== 0 && 
        <svg ref={svgRef}>
        </svg>
      }
    </>
  );
}

export default PatchVisualization;