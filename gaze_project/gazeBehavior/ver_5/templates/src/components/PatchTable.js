import React, { useEffect, useRef } from 'react';
import axios from 'axios';

function PatchTable(props) {
  const { width, height, patchURLs, patchScatterData, numClusters, features, filteredData, passSelectedFeature, selectedPatchUpdate, similarPatchList } = props;
  const svgRef = useRef();
  const d3 = window.d3;
  const colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf", "#999999"];
  const _padding = 5;
  let _rowMax = 50;
  let selectedFeature = -1;
  let selectedPatches = [[0, 0, 0]];
  let reorderingData = [];
  let patchData = [];
  const FLAG = `http://${window.location.hostname}:5000/static/access/patches.png?`+Math.random()
  const fixRecords = (2081+1)*50

  useEffect(() => {
    if (patchURLs.length === 0 || patchScatterData.length ===0 || numClusters === 0)
      return;
    d3.select(svgRef.current).selectAll("*").remove();
    let frameBox = [];
    let cluFrame = [];
    let fixFrame = [];
    let viewFrame = [];
    
    var margin = {top: 10, right: 30, bottom: 10, left: 30},
      drawWidth = width - margin.left - margin.right,
      drawHeight = height - margin.top - margin.bottom;
    var resizingFlag = true;
    // col, row
    let dataframe = [features.length, numClusters+1];
    let boxSize = {
      // "width": drawWidth/(dataframe[0]+1),
      // "height": (drawHeight/(dataframe[1]+1))/2
      "width": drawWidth/(dataframe[0]+1),
      "height": 30
    };
    let patchSize = (drawWidth-(2*_padding)-boxSize.width)/_rowMax;

    if(selectedPatches.length == 0){
      selectedPatches[0][2] = reorderingData[0][0].id;
    }
    // console.log("start axios: selected_patch_table_index.json");
    axios.get(`http://${window.location.hostname}:5000/static/access/selected_patch_table_index.json?`+Math.random())
    .then(response => {
      // console.log("step 1 start");
      console.log("initialize selected patches");
      selectedPatches = response.data;
      console.log(selectedPatches);
      // console.log("step 1 end");
    })
    .then(()=>{
      // console.log("step 2 start");
      // console.log('patchScatterData');
      // console.log(patchScatterData);
      reorderingData = [];
      for(let i=0; i<dataframe[1]; i++){
        var _cluPoints = [];
        for(let j=0; j<patchScatterData.length; j++){
          if(i == patchScatterData[j].clu){
            var _cluPoint = {
              "order": -1,
              "ox": patchScatterData[j].x,
              "oy": patchScatterData[j].y,
              "clu": patchScatterData[j].clu,
              "id": patchURLs[j][0],
              "x": 0,
              "y": 0,
              "url": `http://${window.location.hostname}:5000`+patchURLs[j][1]+"?"+Math.random(),
              "fValue": 0,
              "renderingIndex": -1
            }
            _cluPoints.push(_cluPoint);
          }
        }
        reorderingData.push(_cluPoints);
      }
      // console.log("step 2 reorderingData");
      // console.log(reorderingData);
      // console.log("step 2 end");
    })
    .then(()=>{
      // console.log("step 3 start");
      // console.log("step 3 reorderingData 1");
      // console.log(reorderingData);
      // Resizing the patch size
      let totalPatchRows = 0;
      for(let i=0; i<reorderingData.length; i++){
        let _dataNum = reorderingData[i].length;
        let _numRow = parseInt(Math.floor(_dataNum/_rowMax));
        if(_dataNum%_rowMax !== 0){
          _numRow += 1;
        }
        totalPatchRows += _numRow;
      }
      
      let totalHeight = boxSize.height + reorderingData.length*(_padding*2) + totalPatchRows*patchSize;
      while(totalHeight>drawHeight){
        resizingFlag = false;
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
          break;
        }
      }
      
      if(resizingFlag){
        totalHeight = boxSize.height + reorderingData.length*(_padding*2) + totalPatchRows*patchSize;
        while(totalHeight<drawHeight-50){
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
            break;
          }
        }
      }
      // console.log("step 3 reorderingData 2");
      // console.log(reorderingData);
      
      patchData = [];
      let stack_y = 0;
      let stackIndex = 0;
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
          reorderingData[i][j].renderingIndex = stackIndex;
          stackIndex+=1;
        }
        stack_y += _padding;
        stack_y += patchSize;
      }

      // console.log("step 3 reorderingData 3");
      // console.log(reorderingData);
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

      patch.append('symbol')
        .attr("id", function(d){ return "bar"+String(d.id)})
        .attr("viewBox", function(d){
          let _xPos = parseInt(d.id)*50
          let _rVal = String(_xPos)+" 0 50 50"
          return _rVal
        })
        .append("image")
        .attr("width", function(d){return String(fixRecords)+"px"})
        .attr("height", "50px")
        .attr("xlink:href", FLAG)
        .attr('x', 0)
        .attr('y', 0);

      patch.append('use')
        .attr("xlink:href", function(d){ return "#bar"+String(d.id)})
        .attr('width', patchSize)
        .attr('height', patchSize)
        .attr('x', 0)
        .attr('y', 0);
      
      d3.selectAll(".patch")
      .on('click', function(d){
        let duplicated = false;
        let duplicatedIdx = -1;
        for(let i=0; i<selectedPatches.length; i++){
          if(parseInt(selectedPatches[i][2]) == parseInt(d.id)){
            duplicated = true;
            duplicatedIdx = i;
            break;
          }
        }
        if(duplicated){
          selectedPatches.splice(duplicatedIdx, 1);
        }else{
          selectedPatches.push([parseInt(d.class), d.order, parseInt(d.id)]);
        }
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
          let selectedColorApplied = false;
          for(let i=0; i<selectedPatches.length; i++){
            if(parseInt(selectedPatches[i][2]) == parseInt(d.id)){
              selectedColorApplied = true;
              break;
            }
          }
          let similarColorApplied = false;
          for(let i=0; i<similarPatchList.length; i++){
            if(parseInt(similarPatchList[i].id) == parseInt(d.id)){
              similarColorApplied = true;
              break;
            }
          }
          if(selectedColorApplied == true && similarColorApplied == true){
            return "green";
          }else if(selectedColorApplied == true && similarColorApplied == false){
            return "#b30000";
          }else if(selectedColorApplied == false && similarColorApplied == true){
            return "blue";
          }else{
            return "black";
          }
        })
        .attr("stroke-width", function(d){
          let selectedColorApplied = false;
          for(let i=0; i<selectedPatches.length; i++){
            if(parseInt(selectedPatches[i][2]) == parseInt(d.id)){
              selectedColorApplied = true;
              break;
            }
          }
          let similarColorApplied = false;
          for(let i=0; i<similarPatchList.length; i++){
            if(parseInt(similarPatchList[i].id) == parseInt(d.id)){
              similarColorApplied = true;
              break;
            }
          }
          if(selectedColorApplied || similarColorApplied){
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
          let selectedColorApplied = false;
          for(let i=0; i<selectedPatches.length; i++){
            if(parseInt(selectedPatches[i][2]) == parseInt(d.id)){
              selectedColorApplied = true;
              break;
            }
          }
          let similarColorApplied = false;
          for(let i=0; i<similarPatchList.length; i++){
            if(parseInt(similarPatchList[i].id) == parseInt(d.id)){
              similarColorApplied = true;
              break;
            }
          }
          if(selectedColorApplied == true && similarColorApplied == true){
            return "green";
          }else if(selectedColorApplied == true && similarColorApplied == false){
            return "#b30000";
          }else if(selectedColorApplied == false && similarColorApplied == true){
            return "blue";
          }else{
            return "black";
          }
        })
        .attr("stroke-width", function(d){
          let selectedColorApplied = false;
          for(let i=0; i<selectedPatches.length; i++){
            if(parseInt(selectedPatches[i][2]) == parseInt(d.id)){
              selectedColorApplied = true;
              break;
            }
          }
          let similarColorApplied = false;
          for(let i=0; i<similarPatchList.length; i++){
            if(parseInt(similarPatchList[i].id) == parseInt(d.id)){
              similarColorApplied = true;
              break;
            }
          }
          if(selectedColorApplied || similarColorApplied){
            return "3px";
          }else{
            return "1px";
          }
        });

        d3.selectAll(".fixs")
        .on('click', function(d){
          if(selectedFeature==-1 || selectedFeature != d.index-1){
            let _featureIdx = d.index-1;
            let _selectedPatchesID = [];
            for(let i=0; i<reorderingData.length; i++){
              let _ids = [];
              for(let j=0; j<reorderingData[i].length; j++){
                _ids.push(reorderingData[i][j].id);
              }
              _selectedPatchesID.push(_ids);
            }
            let _selectedPatchesClu = [];
            for(let i=0; i<reorderingData.length; i++){
              let _clus = [];
              for(let j=0; j<reorderingData[i].length; j++){
                _clus.push(parseInt(reorderingData[i][j].clu));
              }
              _selectedPatchesClu.push(_clus);
            }
            const _data = new FormData();
            _data.set('selectedFeature', _featureIdx);
            _data.set('patchesId', _selectedPatchesID);
            _data.set('patchesClu', _selectedPatchesClu);
            let updatedData = [];
            axios.post(`http://${window.location.hostname}:5000/api/patchTable/selectFeature`, _data)
            .then( response => {
              if (response.data.status === 'success') {
                // console.log(response.data);
                passSelectedFeature();
                axios.get(`http://${window.location.hostname}:5000/static/access/patchTable_sorting_update.json?`+Math.random())
                .then( response => {
                  let _update = response.data;
                  for(let i=0; i<_update.length; i++){
                    let _clu = [];
                    for(let j=0; j<_update[i].length; j++){
                      let _renderedOrder = _update[i][j][3];
                      let _p = {
                        "order": _update[i][j][4],
                        "ox": reorderingData[i][_renderedOrder].ox,
                        "oy": reorderingData[i][_renderedOrder].oy,
                        "clu": i,
                        "id": _update[i][j][1],
                        "x": 0,
                        "y": 0,
                        "url": reorderingData[i][_renderedOrder].url,
                        "fValue": _update[i][j][2],
                        "renderingIndex": reorderingData[i][_renderedOrder].renderingIndex
                      }
                      _clu.push(_p)
                    }
                    updatedData.push(_clu);
                  }
                })
                .then(()=>{
                  let stack_y = 0;
                  let stackIndex = 0;
                  // update patchData array
                  for(let i=0; i<updatedData.length; i++){
                    for(let j=0; j<updatedData[i].length; j++){
                      if(j != 0 && j%_rowMax == 0){
                        stack_y += patchSize;
                      }
                      let _x = _padding + boxSize.width + (j*patchSize) - Math.floor((j/_rowMax))*(_rowMax*patchSize);
                      let _y = (i+1)*_padding + boxSize.height + stack_y;       
                      patchData[updatedData[i][j].renderingIndex].order = j;
                      patchData[updatedData[i][j].renderingIndex].class = updatedData[i][j].clu;
                      patchData[updatedData[i][j].renderingIndex].id = updatedData[i][j].id;
                      patchData[updatedData[i][j].renderingIndex].url = updatedData[i][j].url;
                      patchData[updatedData[i][j].renderingIndex].x = _x;
                      patchData[updatedData[i][j].renderingIndex].y = _y;
                      patchData[updatedData[i][j].renderingIndex].ox = updatedData[i][j].ox;
                      patchData[updatedData[i][j].renderingIndex].oy = updatedData[i][j].oy;
                      updatedData[i][j].x = _x;
                      updatedData[i][j].y = _y;
                      updatedData[i][j].renderingIndex = stackIndex;
                      stackIndex+=1;
                    }
                    stack_y += _padding;
                    stack_y += patchSize;
                  }
                })
                .then(()=>{
                  // update renderingData array
                  for(let i=0; i<updatedData.length; i++){
                    for(let j=0; j<updatedData[i].length; j++){
                      reorderingData[i][j].order = updatedData[i][j].order;
                      reorderingData[i][j].ox = updatedData[i][j].ox;
                      reorderingData[i][j].oy = updatedData[i][j].oy;
                      reorderingData[i][j].clu = updatedData[i][j].clu;
                      reorderingData[i][j].id = updatedData[i][j].id;
                      reorderingData[i][j].x = updatedData[i][j].x;
                      reorderingData[i][j].y = updatedData[i][j].y;
                      reorderingData[i][j].url = updatedData[i][j].url;
                      reorderingData[i][j].fValue = updatedData[i][j].fValue;
                      reorderingData[i][j].renderingIndex = updatedData[i][j].renderingIndex;
                    }
                  }
                })
                .then(()=>{
                  // update slected pacthes array [[clu, order, id], ..., [...]]
                  for(let i=0; i<selectedPatches.length; i++){
                    let _c = selectedPatches[i][0];
                    for(let j=0; j<reorderingData[_c].length; j++){
                      if(parseInt(selectedPatches[i][2]) == parseInt(reorderingData[_c][j].id)){
                        selectedPatches[i][1] = reorderingData[_c][j].order;
                        break;
                      }
                    }
                  }
                })
                .then(()=>{
                  // update d3 rendering
                  d3.selectAll(".patch").transition()
                  .attr("transform", function(d) {
                    let _x = d.x;
                    let _y = d.y;
                    return "translate(" + _x + "," + _y + ")";
                  });
                  // d3.selectAll(".patch image")
                  // .attr("xlink:href", function(d) {
                  //   return d.url;
                  // });
                  d3.selectAll(".patch use")
                    .attr("xlink:href", function(d){
                      return "#bar"+String(d.id)
                    });
                  d3.selectAll(".pFrame").transition()
                  .attr("transform", function(d) {
                    let _x = d.x;
                    let _y = d.y;
                    return "translate(" + _x + "," + _y + ")";
                  });
                  d3.selectAll(".pFrame rect").transition()
                  .attr("stroke", function(d){
                    let selectedColorApplied = false;
                    for(let i=0; i<selectedPatches.length; i++){
                      if(parseInt(selectedPatches[i][2]) == parseInt(d.id)){
                        selectedColorApplied = true;
                        break;
                      }
                    }
                    let similarColorApplied = false;
                    for(let i=0; i<similarPatchList.length; i++){
                      if(parseInt(similarPatchList[i].id) == parseInt(d.id)){
                        similarColorApplied = true;
                        break;
                      }
                    }
                    if(selectedColorApplied == true && similarColorApplied == true){
                      return "green";
                    }else if(selectedColorApplied == true && similarColorApplied == false){
                      return "#b30000";
                    }else if(selectedColorApplied == false && similarColorApplied == true){
                      return "blue";
                    }else{
                      return "black";
                    }
                  })
                  .attr("stroke-width", function(d){
                    let selectedColorApplied = false;
                    for(let i=0; i<selectedPatches.length; i++){
                      if(parseInt(selectedPatches[i][2]) == parseInt(d.id)){
                        selectedColorApplied = true;
                        break;
                      }
                    }
                    let similarColorApplied = false;
                    for(let i=0; i<similarPatchList.length; i++){
                      if(parseInt(similarPatchList[i].id) == parseInt(d.id)){
                        similarColorApplied = true;
                        break;
                      }
                    }
                    if(selectedColorApplied || similarColorApplied){
                      return "3px";
                    }else{
                      return "1px";
                    }
                  });
                  
                  const _spaUpdate = new FormData();
                  _spaUpdate.set('selectedPatches', selectedPatches);
                  axios.post(`http://${window.location.hostname}:5000/api/patchTable/selectedPatchesUpdate`, _spaUpdate)
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
                });

                console.log('reorderingData test');
                console.log(reorderingData);
                let _clus = [];
                let _orders = [];
                let _ids = [];
                for(let i=0; i<reorderingData.length; i++){
                  for(let j=0; j<reorderingData[i].length; j++){
                    _clus.push(reorderingData[i][j].clu);
                    _orders.push(reorderingData[i][j].order);
                    _ids.push(reorderingData[i][j].id);
                  }
                }
                // post clu, order, id data to python-flask server
                const _coiData = new FormData();
                // set clu, order, and id
                _coiData.set('reorderedClu', _clus);
                _coiData.set('reorderedOrder', _orders);
                _coiData.set('reorderedId', _ids);
                axios.post(`http://${window.location.hostname}:5000/api/patchTable/updatePatchTableStatus`, _coiData)
                .then(response => {
                  if (response.data.status === 'success') {
                    // selecte patches update signal: patchTable -> Data.js
                    console.log(response.data);
                  } else if (response.data.status === 'failed') {
                    alert(`Failed to load data - ${response.data.reason}`);
                  }
                }).catch(error => {
                  alert(`Error - ${error.message}`);
                });
              } else if (response.data.status === 'failed') {
                alert(`Failed to load data - ${response.data.reason}`);
              }
            })
            .then(()=>{
            })
            .catch(error => {
              alert(`Error - ${error.message}`);
            });
            selectedFeature = _featureIdx;
          }else{
            selectedFeature = -1;
          }

          if(similarPatchList.length != 0){
            console.log('updateMovingPatchList: inner');
            let movePatchClu = [];
            let movePatchOrder = [];
            let movePatchId = [];
            for(let i=0; i<similarPatchList.length; i++){
              let _id = similarPatchList[i].id;
              let _clu = 0;
              let _order = 0;
              let _catchFlag = false;
              for(let j=0; j<reorderingData.length; j++){
                for(let k=0; k<reorderingData[j].length; k++){
                  if(_id == reorderingData[j][k].id){
                    _clu = reorderingData[j][k].clu;
                    _order = reorderingData[j][k].order;
                    _catchFlag = true;
                    break;
                  }
                }
                if(_catchFlag){
                  break;
                }
              }
              movePatchClu.push(_clu);
              movePatchOrder.push(_order);
              movePatchId.push(_id);
            }
            const _movePatchData = new FormData();
            _movePatchData.set('patchClu', movePatchClu);
            _movePatchData.set('patchOrder', movePatchOrder);
            _movePatchData.set('patchId', movePatchId);
            axios.post(`http://${window.location.hostname}:5000/api/patchTable/updateMovingPatchList`, _movePatchData)
            .then(response => {
              if (response.data.status === 'success') {
                console.log("update patch cluster");
              } else if (response.data.status === 'failed') {
                alert(`Failed to load data - ${response.data.reason}`);
              }
            }).catch(error => {
              alert(`Error - ${error.message}`);
            });
          }
      });

      if(similarPatchList.length != 0){
        console.log('updateMovingPatchList: outer');
        let movePatchClu = [];
        let movePatchOrder = [];
        let movePatchId = [];
        for(let i=0; i<similarPatchList.length; i++){
          let _id = similarPatchList[i].id;
          let _clu = 0;
          let _order = 0;
          let _catchFlag = false;
          for(let j=0; j<reorderingData.length; j++){
            for(let k=0; k<reorderingData[j].length; k++){
              if(_id == reorderingData[j][k].id){
                _clu = reorderingData[j][k].clu;
                _order = reorderingData[j][k].order;
                _catchFlag = true;
                break;
              }
            }
            if(_catchFlag){
              break;
            }
          }
          movePatchClu.push(_clu);
          movePatchOrder.push(_order);
          movePatchId.push(_id);
        }
        const _movePatchData = new FormData();
        _movePatchData.set('patchClu', movePatchClu);
        _movePatchData.set('patchOrder', movePatchOrder);
        _movePatchData.set('patchId', movePatchId);
        axios.post(`http://${window.location.hostname}:5000/api/patchTable/updateMovingPatchList`, _movePatchData)
        .then(response => {
          if (response.data.status === 'success') {
            console.log("update patch cluster");
          } else if (response.data.status === 'failed') {
            alert(`Failed to load data - ${response.data.reason}`);
          }
        }).catch(error => {
          alert(`Error - ${error.message}`);
        });
      }
      // console.log("step 3 end");
    });
    // console.log("end axios: selected_patch_table_index.json");
  }, [props.patchURLs, props.patchScatterData, props.numClusters, props.features, props.filteredData, props.similarPatchList]);
  
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