import React, { useEffect, useRef } from 'react';

const ColorBox=(props)=>{
  const { colorArray, selectedColor, selectedColorUpdate} = props;
  const svgRef = useRef();
  const d3 = window.d3v4;

  const updateSelectedColorIndex =(index)=>{
    selectedColorUpdate(index);
  }

  useEffect(() => {
    if(colorArray.length === 0)
      return;
    // console.log("selectedColor: "+selectedColor);
    d3.select(svgRef.current).selectAll("*").remove();
    var selectedBoxIndex = selectedColor;
    var divSize = {
      width: d3.select(".colorPallete").node().getBoundingClientRect().width,
      height: d3.select(".colorPallete").node().getBoundingClientRect().height
    };
    // console.log(divSize)

    var margin = {top: 0, right: 0, bottom: 0, left: 0};
    // var drawWidth = width - (margin.left + margin.right);
    var drawWidth = divSize.width - (margin.left + margin.right);
    var drawHeight = divSize.height - (margin.top + margin.bottom);
    var boxWidth = drawWidth/colorArray.length;
    var colorBoxArray = [];
    for(let i=0; i<colorArray.length; i++){
      var _box = {
        x: i*boxWidth,
        c: colorArray[i]
      };
      colorBoxArray.push(_box);
    }
    
    var svg = d3.select(svgRef.current)
    .attr("width", drawWidth + margin.left + margin.right)
    .attr("height", drawHeight + margin.top + margin.bottom)
      .append("svg")
      .attr("width", drawWidth + margin.left + margin.right)
      .attr("height", drawHeight + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var colorBox = svg.selectAll(".colorbox")
    .data(colorBoxArray)
    .enter()
    .append('g')
    .attr('class', 'colorbox')
    .attr("width", boxWidth)
    .attr("height", drawHeight)
    .attr("transform", function(d){
      let _x = d.x;
      return "translate(" + _x + "," + margin.top + ")";
    })
    .on("click", function(d, i){
      if(selectedBoxIndex >= 0){
        selectedBoxIndex = i;
      }else if(selectedBoxIndex == i){
        selectedBoxIndex = -1;
      }
      updateSelectedColorIndex(i);
      console.log("click: "+i);

      colorBox.selectAll("rect").transition()
      .attr("stroke", function(d, i){
        if(d.c==colorArray[selectedBoxIndex]){
          return "black";
        }else{
          return "none";
        }
      })
      .attr("stroke-width", function(d, i){
        if(d.c==colorArray[selectedBoxIndex]){
          return "4px";
        }else{
          return "none";
        }
      });
    });

    colorBox.append('rect')
    .attr("width", boxWidth)
    .attr("height", drawHeight)
    .attr("stroke", function(d, i){
      if(i==selectedBoxIndex){
        return "black";
      }else{
        return "none";
      }
    })
    .attr("stroke-width", function(d, i){
      if(i==selectedBoxIndex){
        return "4px";
      }else{
        return "none";
      }
    })
    .style("fill", function(d){
      return d.c;
    });
    
  }, [, props.colorArray]);

  return (
    <>
      {colorArray !== null &&
        <svg ref={svgRef}>
        </svg>
      }
    </>
  );
}

export default ColorBox;
