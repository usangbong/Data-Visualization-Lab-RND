import React, { useEffect, useRef } from 'react';

function StimulusView(props) {
  const { imgURL, gridWidthCellNumber, gridHeightCellNumber, gridColor, gridVisableFlag, colorArray, selectedArea, selectedColorIdx, selectedAreaUpdate, selectedAreaChage } = props;
  const svgRef = useRef();
  const d3 = window.d3v4;
  
  useEffect(() => {
    if(imgURL.length === 0)
      return;
    
    d3.select(svgRef.current).selectAll("*").remove();
    var local_selectedArea = selectedArea;
    if(selectedArea.length == 0){
      for(let i=0; i<colorArray.length; i++){
        local_selectedArea.push([]);
      }
      selectedAreaUpdate(local_selectedArea);
    }else if(selectedArea.length != colorArray.length){
      for(let i=0; i<colorArray.length-selectedArea.length; i++){
        local_selectedArea.push([]);
      }
      selectedAreaUpdate(local_selectedArea);
    }

    let mouseDragFlag = false;
    let imageOnFlag = false;
    var windowSize ={
      width: d3.select(".imageViewer").node().getBoundingClientRect().width,
      height: d3.select(".imageViewer").node().getBoundingClientRect().height
    };

    var margin = {top: 0, right: 0, bottom: 0, left: 0};
    var drawWidth = windowSize.width - (margin.left + margin.right);
    var drawHeight = windowSize.height - (margin.top + margin.bottom);
    
    var imgWidth = imgURL.width;
    var imgHeight = imgURL.height;
    var stiWidth = windowSize.width;
    var stiHeight = (imgHeight/imgWidth)*stiWidth;
    var resizingRatio = stiWidth/imgWidth;
    if(stiWidth > drawWidth || stiHeight > drawHeight){
      stiHeight = drawHeight;
      stiWidth = (imgWidth/imgHeight)*stiHeight;
      resizingRatio = stiHeight/imgHeight;
    }
    drawWidth = stiWidth;
    drawHeight = stiHeight;
    var sti_url_rnd = imgURL.url+"?"+Math.random();

    var gridBox = [];
    var cellWidthNumber = gridWidthCellNumber;
    var cellHeightNumber = gridHeightCellNumber;
    var cellWidth = stiWidth/cellWidthNumber;
    var cellHeight = stiHeight/cellHeightNumber;
    var gridBoxArr = [];
    for(let i=0; i<cellHeightNumber; i++){
      var _row = [];
      for(let j=0; j<cellWidthNumber; j++){
        var _cell = {
          x: j*cellWidth,
          y: i*cellHeight,
          f: false
        };
        _row.push(_cell);
        gridBoxArr.push({
          x: j*cellWidth,
          y: i*cellHeight,
          ix: j,
          iy: i,
          c: "none",
          label: -1
        });
      }
      gridBox.push(_row);
    }
    
    if(local_selectedArea.length!=0){
      for(let i=0; i<local_selectedArea.length; i++){
        for(let j=0; j<local_selectedArea[i].length; j++){
          let _ic = local_selectedArea[i][j].ic;
          gridBoxArr[_ic].c = colorArray[local_selectedArea[i][j].c];
          gridBoxArr[_ic].label = colorArray[local_selectedArea[i][j].label];
        }
      }
    }
    
    
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
    .on('mouseout', function(d){
      if(mouseDragFlag){
        imageOnFlag = false;
      }else{
        imageOnFlag = true;
      }
    });


    var gridCell = svg.selectAll(".gcell")
    .data(gridBoxArr)
    .enter()
    .append('g')
    .attr('class', 'gcell')
    .attr("transform", function(d){
      let _x = d.x;
      let _y = d.y;
      return "translate(" + _x + "," + _y + ")";
    });

    gridCell.append('rect')
    .attr("width", cellWidth)
    .attr("height", cellHeight)
    .attr('class', 'cellRect')
    .attr("stroke", function(){
      if(gridVisableFlag){
        return gridColor;
      }else{
        return "none";
      }
    })
    .attr("stroke-width", "1px")
    .style("fill", function(d){return d.c})
    .style('opacity', 0.5)
    .on('mouseover', function(d){
      imageOnFlag = true;
    });

    function duplicateCheck(ix, iy, ic, selectedColorIndex){
      for(let i=0; i<local_selectedArea[selectedColorIndex].length; i++){
        let _ix = local_selectedArea[selectedColorIndex][i].ix;
        let _iy = local_selectedArea[selectedColorIndex][i].iy;
        let _ic = local_selectedArea[selectedColorIndex][i].ic;
        if(ix == _ix && iy == _iy && ic==_ic){
          return true;
        }
      }
      return false;
    }

    function localSelectedAreaUpdate(ix, iy, ic, selectedColorIndex){
      let _sa = {
        ix: ix,
        iy: iy,
        ic: ic,
        c: selectedColorIndex,
        label: selectedColorIdx
      }
      local_selectedArea[selectedColorIndex].push(_sa);
      selectedAreaUpdate(local_selectedArea);
    }

    svg
    .on("mousedown", mouseDown)
    .on("mousemove", brushPosUpdate)
    .on('mouseup', mouseUp);
    
    function mouseDown(){
      let _x = d3.event.pageX - d3.select(svgRef.current).node().getBoundingClientRect().left-5;
      let _y = d3.event.pageY - d3.select(svgRef.current).node().getBoundingClientRect().top;
      mouseDragFlag = true;

      let _ix = Math.floor(_x/cellWidth);
      let _iy = Math.floor(_y/cellHeight);
      let maxX = Math.floor(stiWidth/cellWidth);
      let maxY = Math.floor(stiHeight/cellHeight);
      // console.log("x: "+_ix+", y: "+_iy);
      if(mouseDragFlag == true && _ix >=0 && _iy >= 0 && _ix<maxX && _iy<maxY){
        imageOnFlag = true;
        var _ci = _ix + _iy*cellWidthNumber;
        // console.log(_ci);
        let dupFlag = duplicateCheck(_ix, _iy, _ci, selectedColorIdx);
        if(!dupFlag){
          if(gridBoxArr[_ci].c == "none"){
            gridBoxArr[_ci].c = colorArray[selectedColorIdx];
            gridBoxArr[_ci].label = selectedColorIdx;
          }else{
            selectedAreaChage([_ix, _iy]);
            gridBoxArr[_ci].c = colorArray[selectedColorIdx];
            gridBoxArr[_ci].label = selectedColorIdx;
          }
          localSelectedAreaUpdate(_ix, _iy, _ci, selectedColorIdx);
          gridCell.selectAll("rect")
          .style('fill', function(d){
            return d.c;
          });
        }
      }
    }
    function brushPosUpdate(){
      if(mouseDragFlag == true && imageOnFlag == true){
        mouseDragFlag = true;
      }else if(mouseDragFlag == true && imageOnFlag == false){
        mouseDragFlag = false;
        selectedAreaUpdate(local_selectedArea);
      }

      let _x = d3.event.pageX - d3.select(svgRef.current).node().getBoundingClientRect().left;
      let _y = d3.event.pageY - d3.select(svgRef.current).node().getBoundingClientRect().top;
      

      let _ix = Math.floor(_x/cellWidth);
      let _iy = Math.floor(_y/cellHeight);
      let maxX = Math.floor(stiWidth/cellWidth);
      let maxY = Math.floor(stiHeight/cellHeight);
      
      if(mouseDragFlag == true && _ix >=0 && _iy >= 0 && _ix<maxX && _iy<maxY){
        var _ci = _ix + _iy*cellWidthNumber;
        let dupFlag = duplicateCheck(_ix, _iy, _ci, selectedColorIdx);
        if(!dupFlag){
          if(gridBoxArr[_ci].c == "none"){
            gridBoxArr[_ci].c = colorArray[selectedColorIdx];
            gridBoxArr[_ci].label = selectedColorIdx;
          }else{
            selectedAreaChage([_ix, _iy]);
            gridBoxArr[_ci].c = colorArray[selectedColorIdx];
            gridBoxArr[_ci].label = selectedColorIdx;
          }
          localSelectedAreaUpdate(_ix, _iy, _ci, selectedColorIdx);
          gridCell.selectAll("rect")
          .style('fill', function(d){
            return d.c;
          });
        }
      }
    }
    function mouseUp(){
      mouseDragFlag = false;
      selectedAreaUpdate(local_selectedArea);
    }


  }, [, props.imgURL, props.colorArray, props.selectedColorIdx, props.gridWidthCellNumber, props.gridHeightCellNumber, props.gridColor, props.gridVisableFlag, props.selectedAreaUpdate ]);
  return (
    <>
      {imgURL !== null &&
        <svg ref={svgRef}>
        </svg>
      }
    </>
  );
}

export default StimulusView;