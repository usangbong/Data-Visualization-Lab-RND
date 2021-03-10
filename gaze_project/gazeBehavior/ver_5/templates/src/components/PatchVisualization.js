import React, { isValidElement, useEffect, useRef } from 'react';
import axios from 'axios';

function PatchVisualization(props) {
  const { width, height, visStyle, nodeStyle, nodeSpinnerSize, patchURLs, patchScatterData, numClusters, features, selectedPatchUpdate, similarPatchList } = props;
  const svgRef = useRef();
  const d3 = window.d3;
  const colors = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf", "#999999"];
  const _padding = 5;
  let _rowMax = 50;
  let selectedFeature = -1;
  let selectedPatches = [[0, 0, 0]];
  let reorderingData = [];
  let patchData = [];
  // let coordiData = [];
  const FLAG = `http://${window.location.hostname}:5000/static/access/patches.png?`+Math.random()
  const fixRecords = (2081+1)*50;
  let mouseDownLocation = [0, 0];
  let selectBox = [{x:0, y:0, w:0, h:0}];

  useEffect(() => {
    if (patchURLs.length === 0 || patchScatterData.length ===0 || numClusters === 0)
      return;
    d3.select(svgRef.current).selectAll("*").remove();
    let frameBox = [];
    let cluFrame = [];
    let viewFrame = [];
    let nodeLength = nodeSpinnerSize;
    
    var margin = {top: 10, right: 30, bottom: 50, left: 30},
      drawWidth = width - margin.left - margin.right,
      drawHeight = height - margin.top - margin.bottom;
    var resizingFlag = true;
    // col, row
    let dataframe = [features.length, numClusters+1];
    console.log('dataframe');
    console.log(dataframe);
    let boxSize = {
      "width": drawWidth/(dataframe[0]+10),
      "height": 30
    };
    let patchSize = (drawWidth-(2*_padding)-boxSize.width)/_rowMax;

    if(selectedPatches.length == 0){
      selectedPatches[0][2] = reorderingData[0][0].id;
    }
    // console.log("start axios: selected_patch_table_index.json");
    axios.get(`http://${window.location.hostname}:5000/static/access/selected_patch_table_index.json?`+Math.random())
    .then(response => {
      // console.log("initialize selected patches");
      selectedPatches = response.data;
      // console.log(selectedPatches);
    })
    .then(()=>{
      // console.log("patchScatterData");
      // console.log(patchScatterData);
      reorderingData = [];
      for(let i=0; i<dataframe[1]; i++){
        var _cluPoints = [];
        for(let j=0; j<patchScatterData.length; j++){
          if(i == patchScatterData[j].clu){
            var _cluPoint = {
              "order": -1,
              "ox": parseFloat(patchScatterData[j].x),
              "oy": parseFloat(patchScatterData[j].y),
              "clu": parseInt(patchScatterData[j].clu),
              "id": parseInt(patchURLs[j][0]),
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
    })
    .then(()=>{
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
      

      // stpe: data setting
      patchData = [];
      let stack_y = 0;
      let stackIndex = 0;
      for(let i=0; i<reorderingData.length; i++){
        for(let j=0; j<reorderingData[i].length; j++){
          if(j != 0 && j%_rowMax == 0){
            stack_y += patchSize;
          }
          let _x = _padding + boxSize.width + (j*patchSize) - Math.floor((j/_rowMax))*(_rowMax*patchSize);
          // let _y = (i+1)*_padding + boxSize.height + stack_y;
          let _y = (i+1)*_padding + stack_y;
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

      if(visStyle == 'clustering'){
        console.log("visStyle: clustering");
        for(let i=0; i<dataframe[0]+1; i++){
          for(let j=0; j<dataframe[1]+1; j++){
            let _tag = "";
            if(i === 0 && j === 0){
              continue;
            }else{
              if(i === 0){
                _tag = "clusters";
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
          }else if(_tag === "patches"){
            viewFrame.push(frameBox[i]);
          }else{
            console.log("error");
          }
        }
        
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

      }else if(visStyle == 'scatterplot'){
        console.log("visStyle: scatterplot");
        // Add X axis
        var xMin = d3.min(patchData, (d => parseFloat(d.ox)));
        var xMax = d3.max(patchData, (d => parseFloat(d.ox)));
        var x = d3.scaleLinear()
        .domain([xMin, xMax])
        .range([ 0, drawWidth ]);
        // Add Y axis
        var yMin = d3.min(patchData, (d => parseFloat(d.oy)));
        var yMax = d3.max(patchData, (d => parseFloat(d.oy)));
        var y = d3.scaleLinear()
        .domain([yMin, yMax])
        .range([ drawHeight, 0]);

        // Add dots
        var node = svg.append('g')
        .selectAll("dot") 
        .data(patchData)
        .enter()
        .append("rect")
          .attr("class", "node")
          .attr("x", function (d) { return x(d.ox)-nodeLength/2; } )
          .attr("y", function (d) { return y(d.oy)-nodeLength/2; } )
          .attr("width", nodeLength)
          .attr("height", nodeLength)
          .style("fill", function (d) {return colors[parseInt(d.class)]});
        
        var brushPatch = d3.select(svgRef.current)
        .on('mousedown', mousedown)
        .on('mouseup', mouseup)
        .append("g")
        .attr("width", drawWidth)
        .attr("height", drawHeight)
          .selectAll(".brushPatch")
          .data(selectBox)
          .enter()
            .append('g')
            .attr("class", "brushPatch");

        brushPatch.append("rect")
        .attr("x", function(d){return d.x})
        .attr("y", function(d){return d.y})
        .attr("width", function(d){return d.w})
        .attr("height", function(d){return d.h})
        .style("fill", "gray")
        .attr("stroke", "black")
        .attr("stroke-width", "1px")
        .style("opacity", 0.2);

        d3.selectAll('.node')
        .on('click', function(d){
          d3.select(svgRef.current).selectAll(".pallete").remove();
          d3.selectAll(".brushPatch rect")
          .attr("x", 0)
          .attr("y", 0)
          .attr("width", 0)
          .attr("height", 0);

          console.log("patch node id: "+d.id);
          var m = d3.mouse(this);
          var _x = m[0];
          var _y = m[1];
          console.log("scatter - click: "+m[0]+", "+m[1]);

          var pieData = {a: 20, b: 20, c: 20, d:20, e:20};
          var radius = 20;
          var colorArr = [];
          for(let i=0; i<dataframe[1]; i++){
            colorArr.push(colors[i]);
          }
          var color = d3.scaleOrdinal()
          .domain(pieData)
          .range(colorArr);
          var pie = d3.pie()
          .value(function(d){return d.value});
          var data_ready = pie(d3.entries(pieData));

          var pallete = svg.append('g')
          .attr("class", "pallete")
          .attr("transform", "translate(" + _x + "," + _y + ")")
          .selectAll('whatever')
          .data(data_ready)
          .enter()
          .append('path')
          .attr('d', d3.arc()
            .innerRadius(radius-12)
            .outerRadius(radius)
          )
          .attr('fill', function(d){ return(color(d.data.key)) })
          .attr("stroke", "black")
          .style("stroke-width", "2px");

          d3.selectAll('path')
          .on('click', function(d){
            console.log(d);
          });
        });
        
        
        function mousedown(){
          d3.select(svgRef.current).selectAll(".pallete").remove();
          
          var m = d3.mouse(this);
          mouseDownLocation[0] = m[0];
          mouseDownLocation[1] = m[1];
          console.log("scatter - mousedown: "+m[0]+", "+m[1]);
          d3.selectAll(".brushPatch rect")
          .attr("x", mouseDownLocation[0])
          .attr("y", mouseDownLocation[1])
          .attr("width", 0)
          .attr("height", 0);
          d3.select(svgRef.current).on("mousemove", mousemove);
        }

        function mousemove(){
          var m = d3.mouse(this);
          console.log("scatter - mousemove: "+m[0]+", "+m[1]);
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
          
          d3.selectAll(".brushPatch rect")
          .attr("x", mouseDownLocation[0])
          .attr("y", mouseDownLocation[1])
          .attr("width", function(d){
            return _w;
          })
          .attr("height", function(d){
            return _h;
          });

          d3.select(svgRef.current).selectAll(".pallete").remove();
          var _x = m[0]-24;
          var _y = m[1]-8;

          var pieData = {a: 20, b: 20, c: 20, d:20, e:20};
          var radius = 20;
          var colorArr = [];
          for(let i=0; i<dataframe[1]; i++){
            colorArr.push(colors[i]);
          }
          var color = d3.scaleOrdinal()
          .domain(pieData)
          .range(colorArr);
          var pie = d3.pie()
          .value(function(d){return d.value});
          var data_ready = pie(d3.entries(pieData));

          var pallete = svg.append('g')
          .attr("class", "pallete")
          .attr("transform", "translate(" + _x + "," + _y + ")")
          .selectAll('whatever')
          .data(data_ready)
          .enter()
          .append('path')
          .attr('d', d3.arc()
            .innerRadius(radius-12)
            .outerRadius(radius)
          )
          .attr('fill', function(d){ return(color(d.data.key)) })
          .attr("stroke", "black")
          .style("stroke-width", "2px");
        }
        function mouseup(){
          d3.select(svgRef.current).on("mousemove", null);
          
        }
      }else{
        console.log("visStyle: empty");
      }
      if(nodeStyle == 'patch'){
        var patch = svg.selectAll(".patch")
        .data(patchData)
        .enter()
        .append("g")
        .attr("class", "patch")
        .attr("transform", function(d) {
          return "translate(" + (x(d.ox)-(nodeLength-2)/2) + "," + (y(d.oy)-(nodeLength-2)/2) + ")";
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
        .attr('width', (nodeLength-2))
        .attr('height', (nodeLength-2))
        .attr('x', 0)
        .attr('y', 0);
      }

    });
  }, [props.visStyle, props.nodeStyle, props.nodeSpinnerSize, props.patchURLs, props.patchScatterData, props.numClusters, props.features, props.filteredData, props.similarPatchList]);
  
  return (
    <>
      {patchURLs.length !== 0 && patchScatterData.length !==0 && numClusters !== 0 &&
        <svg ref={svgRef}>
        </svg>
      }
    </>
  );
}

export default PatchVisualization;