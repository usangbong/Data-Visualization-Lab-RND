import React, { useEffect, useRef } from 'react';

function ColorPoint(props) {
  const { divClassName, colorArray, selectedColor, selectedColorIdx, heightVal, selectedColorUpdate } = props;
  const svgRef = useRef();
  const d3 = window.d3v4;

  useEffect(() => {
    if(colorArray.length === 0)
      return;
    d3.select(svgRef.current).selectAll("*").remove();
    var divSize = {
      width: d3.select(divClassName).node().getBoundingClientRect().width,
      // height: d3.select(divClassName).node().getBoundingClientRect().height
      height: heightVal
    };
    // console.log(divSize)

    var margin = {top: 0, right: 0, bottom: 0, left: 0};
    var drawWidth = divSize.width - (margin.left + margin.right);
    var drawHeight = divSize.height - (margin.top + margin.bottom);
    
    var colorPointBox = [colorArray[selectedColor]];
    
    var svg = d3.select(svgRef.current)
    .attr("width", drawWidth + margin.left + margin.right)
    .attr("height", drawHeight + margin.top + margin.bottom)
      .append("svg")
      .attr("width", drawWidth + margin.left + margin.right)
      .attr("height", drawHeight + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var colorPointSVG = svg.selectAll(".colorpoint")
    .data(colorPointBox)
    .enter()
    .append('g')
    .attr('class', 'colorbox')
    .attr("width", drawWidth)
    .attr("height", drawHeight)
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    colorPointSVG.append('rect')
    .attr("width", drawWidth)
    .attr("height", drawHeight)
    .attr("stroke", "black")
    .attr("stroke-location", "inside")
    .attr("stroke-width", function(d){
      if(selectedColorIdx == selectedColor){
        // console.log("selectedColor: "+selectedColor+", selectedColorIdx: "+ selectedColorIdx);
        return "6px";
      }else{
        return "none";
      }
    })
    .style("fill", function(d){
      return d;
    })
    .on("mousedown", function(){
      // console.log("md selectedColor: "+selectedColor+", selectedColorIdx: "+ selectedColorIdx);
      selectedColorUpdate(selectedColor);
    });

    
  }, [, props.colorArray, props.selectedColor, props.selectedColorUpdate ]);

  return (
    <>
      {colorArray !== null &&
        <svg ref={svgRef}>
        </svg>
      }
    </>
  );
}

export default ColorPoint;
