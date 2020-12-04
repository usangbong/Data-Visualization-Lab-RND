import React, { useEffect, useRef } from 'react';
import axios from 'axios';

function PatchTable(props) {
  const { width, height, patchURLs, patchScatterData, numClusters, features, filteredData, passSelectedFeature, selectedPatchUpdate } = props;
  const svgRef = useRef();
  const d3 = window.d3;
  const colors = ["#a6cee3", "#fb9a99", "#fdbf6f", "#cab2d6", "#b15928", "#b2df8a", "#ffff99", "#1f78b4", "#e31a1c", "#ff7f00", "#33a02c", "#6a3d9a"];
  const _padding = 5;
  let _rowMax = 50;
  let selectedFeature = -1;
  let selectedPatches = [[0, 0]];

  useEffect(() => {
    if (patchURLs.length === 0 || patchScatterData.length ===0 || numClusters === 0)
      return;
    d3.select(svgRef.current).selectAll("*").remove();

    let frameBox = [];
    let cluFrame = [];
    let fixFrame = [];
    let viewFrame = [];

    var margin = {top: 10, right: 30, bottom: 20, left: 30},
      drawWidth = width - margin.left - margin.right,
      drawHeight = height - margin.top - margin.bottom;

    // col, row
    let dataframe = [features.length, numClusters+1];
    let boxSize = {
      // "width": drawWidth/(dataframe[0]+1),
      // "height": (drawHeight/(dataframe[1]+1))/2
      "width": drawWidth/(dataframe[0]+1),
      "height": 30
    };

    let patchSize = (drawWidth-(2*_padding)-boxSize.width)/_rowMax;
    let reorderingData = [];
    for(let i=0; i<dataframe[1]; i++){
      var _cluPoints = [];
      for(let j=0; j<patchScatterData.length; j++){
        if(i == patchScatterData[j]["clu"]){
          var _cluPoint = {
            "order": -1,
            "ox": patchScatterData[j]["x"],
            "oy": patchScatterData[j]["y"],
            "clu": patchScatterData[j]["clu"],
            "id": patchURLs[j][0],
            "x": 0,
            "y": 0,
            "url": "http://localhost:5000"+patchURLs[j][1]+"?"+Math.random()
          }
          _cluPoints.push(_cluPoint);
        }
      }
      reorderingData.push(_cluPoints);
    }
    // console.log("reorderingData");
    // console.log(reorderingData);
    // Resizing the patch size
    // console.log("Resizing the patch size");
    let totalPatchRows = 0;
    for(let i=0; i<reorderingData.length; i++){
      let _dataNum = reorderingData[i].length;
      let _numRow = parseInt(Math.floor(_dataNum/_rowMax));
      if(_dataNum%_rowMax !== 0){
        _numRow += 1;
      }
      totalPatchRows += _numRow;
    }
    // console.log("totalPatchRows: "+totalPatchRows);
    // console.log("down-sizing");
    let totalHeight = boxSize.height + reorderingData.length*(_padding*2) + totalPatchRows*patchSize;
    while(totalHeight>drawHeight){
      _rowMax += 5;
      totalPatchRows = 0;
      for(let i=0; i<reorderingData.length; i++){
        let _dataNum = reorderingData[i].length;
        let _numRow = parseInt(Math.floor(_dataNum/_rowMax));
        if(_dataNum%_rowMax !== 0){
          _numRow += 1;
        }
        totalPatchRows += _numRow;
      }
      patchSize = (drawWidth-(2*_padding)-boxSize.width)/_rowMax;
      totalHeight = boxSize.height + reorderingData.length*(_padding*2) + totalPatchRows*patchSize;
      // console.log("drawHeight: "+drawHeight+", totalHeight: "+totalHeight+", patchSize: "+patchSize+", rowMax: "+_rowMax);
      if(totalHeight > drawHeight){
        _rowMax += 5;
        totalPatchRows = 0;
        for(let i=0; i<reorderingData.length; i++){
          let _dataNum = reorderingData[i].length;
          let _numRow = parseInt(Math.floor(_dataNum/_rowMax));
          if(_dataNum%_rowMax !== 0){
            _numRow += 1;
          }
          totalPatchRows += _numRow;
        }
        patchSize = (drawWidth-(2*_padding)-boxSize.width)/_rowMax;
        totalHeight = boxSize.height + reorderingData.length*(_padding*2) + totalPatchRows*patchSize;
        // console.log("drawHeight: "+drawHeight+", totalHeight: "+totalHeight+", patchSize: "+patchSize+", rowMax: "+_rowMax);
        break;
      }
    }
    
    // console.log("up-sizing");
    totalHeight = boxSize.height + reorderingData.length*(_padding*2) + totalPatchRows*patchSize;
    while(totalHeight<700){
      if(_rowMax < 10){
        break;
      }
      _rowMax -= 5;
      totalPatchRows = 0;
      for(let i=0; i<reorderingData.length; i++){
        let _dataNum = reorderingData[i].length;
        let _numRow = parseInt(Math.floor(_dataNum/_rowMax));
        if(_dataNum%_rowMax !== 0){
          _numRow += 1;
        }
        totalPatchRows += _numRow;
      }
      patchSize = (drawWidth-(2*_padding)-boxSize.width)/_rowMax;
      totalHeight = boxSize.height + reorderingData.length*(_padding*2) + totalPatchRows*patchSize;
      // console.log("drawHeight: "+drawHeight+", totalHeight: "+totalHeight+", patchSize: "+patchSize+", rowMax: "+_rowMax);
      if(totalHeight > drawHeight){
        _rowMax += 5;
        totalPatchRows = 0;
        for(let i=0; i<reorderingData.length; i++){
          let _dataNum = reorderingData[i].length;
          let _numRow = parseInt(Math.floor(_dataNum/_rowMax));
          if(_dataNum%_rowMax !== 0){
            _numRow += 1;
          }
          totalPatchRows += _numRow;
        }
        patchSize = (drawWidth-(2*_padding)-boxSize.width)/_rowMax;
        totalHeight = boxSize.height + reorderingData.length*(_padding*2) + totalPatchRows*patchSize;
        // console.log("drawHeight: "+drawHeight+", totalHeight: "+totalHeight+", patchSize: "+patchSize+", rowMax: "+_rowMax);
        break;
      }
    }

    let patchData = [];
    let stack_y = 0;
    for(let i=0; i<reorderingData.length; i++){
      for(let j=0; j<reorderingData[i].length; j++){
        if(j != 0 && j%_rowMax == 0){
          stack_y += patchSize;
        }
        let _x = _padding + boxSize.width + (j*patchSize) - Math.floor((j/_rowMax))*(_rowMax*patchSize);
        let _y = (i+1)*_padding + boxSize.height + stack_y;       
        let _patch = {
          "order": j,
          "class": reorderingData[i][j].clu,
          "id": reorderingData[i][j].id,
          "url": reorderingData[i][j].url,
          "x": _x,
          "y": _y,
          "ox": reorderingData[i][j].ox,
          "oy": reorderingData[i][j].oy,
          "width": patchSize,
          "height": patchSize
        };
        patchData.push(_patch);
        reorderingData[i][j].x = _x;
        reorderingData[i][j].y = _y;
        reorderingData[i][j].order = j;
      }
      stack_y += _padding;
      stack_y += patchSize;
    }
    
    for(let i=0; i<dataframe[0]+1; i++){
      for(let j=0; j<dataframe[1]+1; j++){
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
        let _y = 0;
        let _h = boxSize.height;
        if(j>0){
          _y = reorderingData[j-1][0].y - _padding;
          let _len = reorderingData[j-1].length
          _h = reorderingData[j-1][_len-1].y - reorderingData[j-1][0].y + patchSize +_padding*2;
        }
        
        let _box = {
          "index": i,
          "tag": _tag,
          "x": _x,
          "y": _y,
          "width": boxSize.width,
          "height": _h
        };
        frameBox.push(_box);
        if(i===0){
          _tag = "patches";
          let _x = (i+1)*boxSize.width;
          let _box = {
            "index": i,
            "tag": _tag,
            "x": _x,
            "y": _y,
            "width": drawWidth-boxSize.width,
            "height": _h
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
      
    var svg = d3.select(svgRef.current)
      .attr("width", drawWidth + margin.left + margin.right)
      .attr("height", drawHeight + margin.top + margin.bottom)
      .append("svg")
        .attr("width", drawWidth + margin.left + margin.right)
        .attr("height", drawHeight + margin.top + margin.bottom)
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
      .attr("height", function(d){return d.height;})
      .style("fill", function(d, i){return colors[i]})
      .attr("stroke", "black")
      .attr("stroke-width", "1px")

    clus.append("text")
      .attr("x", function(d){ return d.width/2})
      .attr("y", function(d){ return _padding+d.height/2})
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
      .attr("y", function(d){ return _padding+d.height/2})
      .text(function(d, i){ return features[i][2]})
      .style("fill", "black");

    d3.selectAll(".fixs")
      .on('click', function(d){
        // console.log(d);
        if(selectedFeature==-1 || selectedFeature != d.index-1){
          let _featureIdx = d.index-1;
          const _data = new FormData();
          _data.set('selectedFeature', _featureIdx);
          axios.post(`http://${window.location.hostname}:5000/api/patchTable/selectFeature`, _data)
          .then(response => {
            if (response.data.status === 'success') {
              // console.log(response.data);
              passSelectedFeature();
            } else if (response.data.status === 'failed') {
              alert(`Failed to load data - ${response.data.reason}`);
            }
          }).catch(error => {
            alert(`Error - ${error.message}`);
          });
          selectedFeature = _featureIdx;
        }else{
          selectedFeature = -1;
        }
    });

    var pats = svg.selectAll(".view")
      .data(viewFrame)
      .enter()
      .append("g")
      .attr("class", "view")
      .attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
      });
      
    pats.append("rect")
      .attr("width", drawWidth - boxSize.width)
      .attr("height", function(d){
        return d.height;
      })
      .style("fill", "none")
      .attr("stroke", "black")
      .attr("stroke-width", "1px");

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
      .attr("xlink:href", function(d) {return d.url});
      // .style("opacity", 1.0);

    d3.selectAll(".patch")
    .on('click', function(d){
      let duplicated = false;
      let duplicatedIdx = -1;
      for(let i=0; i<selectedPatches.length; i++){
        let _clu = selectedPatches[i][0];
        let _ord = selectedPatches[i][1];
        if(parseInt(d.class) == _clu && d.order == _ord){
          duplicated = true;
          duplicatedIdx = i;
          break;
        }
      }
      if(duplicated){
        selectedPatches.splice(duplicatedIdx, 1);
      }else{
        selectedPatches.push([parseInt(d.class), d.order]);
      }
      // console.log("selectedPatches");
      // console.log(selectedPatches);
      const _data = new FormData();
      _data.set('selectedPatches', selectedPatches);
      axios.post(`http://${window.location.hostname}:5000/api/patchTable/selectedPatchesUpdate`, _data)
        .then(response => {
          if (response.data.status === 'success') {
            // selecte patches update signal: patchTable -> Data.js
            selectedPatchUpdate();
          } else if (response.data.status === 'failed') {
            alert(`Failed to load data - ${response.data.reason}`);
          }
        }).catch(error => {
          alert(`Error - ${error.message}`);
      });

      d3.selectAll(".pFrame rect").transition()
      .attr("stroke", function(d){
        let colorApplied = false;
        for(let i=0; i<selectedPatches.length; i++){
          // console.log("selectedPatches["+i+"]");
          // console.log(selectedPatches[i]);
          let _clu = selectedPatches[i][0];
          let _ord = selectedPatches[i][1];
          if(parseInt(d.class) == _clu && d.order == _ord){
            colorApplied = true;
            break;
          }
        }
        if(colorApplied){
          return "#b30000";
        }else{
          return "black";
        }
      })
      .attr("stroke-width", function(d){
        let colorApplied = false;
        for(let i=0; i<selectedPatches.length; i++){
          let _clu = selectedPatches[i][0];
          let _ord = selectedPatches[i][1];
          if(parseInt(d.class) == _clu && d.order == _ord){
            colorApplied = true;
            break;
          }
        }
        if(colorApplied){
          return "3px";
        }else{
          return "1px";
        }
      });
    });

    var patchFrame = svg.selectAll(".pFrame")
      .data(patchData)
      .enter()
      .append("g")
      .attr("class", "pFrame")
      .attr("transform", function(d) {
        let _x = d.x;
        let _y = d.y;
        return "translate(" + _x + "," + _y + ")";
      });
    
    patchFrame.append("rect")
      .attr("width", patchSize)
      .attr("height", patchSize)
      .attr("fill", "none")
      .attr("stroke", function(d){
        let colorApplied = false;
        for(let i=0; i<selectedPatches.length; i++){
          let _clu = selectedPatches[i][0];
          let _ord = selectedPatches[i][1];
          // console.log("clu: "+_clu+", order: "+_ord);
          // console.log("d.clu: "+d.clu+", d.order: "+d.order);
          if(parseInt(d.class) == _clu && d.order == _ord){
            colorApplied = true;
            break;
          }
        }
        if(colorApplied){
          return "#b30000";
        }else{
          return "black";
        }
      })
      .attr("stroke-width", function(d){
        let colorApplied = false;
        for(let i=0; i<selectedPatches.length; i++){
          let _clu = selectedPatches[i][0];
          let _ord = selectedPatches[i][1];
          // console.log("clu: "+_clu+", order: "+_ord);
          // console.log("d.clu: "+d.clu+", d.order: "+d.order);
          if(parseInt(d.class) == _clu && d.order == _ord){
            colorApplied = true;
            break;
          }
        }
        if(colorApplied){
          return "3px";
        }else{
          return "1px";
        }
      });
    
    
  }, [, props.patchURLs, props.patchScatterData, props.numClusters, props.features]);

  return (
    <>
      {patchURLs.length !== 0 && patchScatterData.length !==0 && numClusters !== 0 &&
        <svg ref={svgRef}>
        </svg>
      }
    </>
  );
}

export default PatchTable;
