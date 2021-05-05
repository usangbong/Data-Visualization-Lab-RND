import React, { useEffect, useRef } from 'react';

function StiRadarChart(props) {
  const { width, height, iqrData } = props;
  const svgRef = useRef();
  const d3 = window.d3v4;
  const colores_g = ["#662506", "#e41a1c", "#377eb8"];
  
  useEffect(() => {
    if (iqrData.length === 0)
      return;
    d3.select(svgRef.current).selectAll("*").remove();
    
    let margin = {top: 10, right: 10, bottom: 30, left: 10};
    let drawWidth = width - (margin.left + margin.right);
    let drawHeight = height - (margin.top + margin.bottom);

    var svg = d3.select(svgRef.current)
    .attr("width", width)
    .attr("height", height)
    .append("svg")
      .attr("width", width)
      .attr("height", height)
      .style("font", "12px sans-serif")
      .style("text-anchor", "middle")
    .append('g').attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

    let features = [];
    for(let i=0; i<iqrData.length; i++){
      features.push(iqrData[i][0]);
    }
    // ["intensity", "color", "orientation", "curvature", "center_bias", "entropy_rate", "log_spectrum", "HOG"];
    let line = d3.line()
    .x(d => d.x)
    .y(d => d.y);

    let area = d3.area()
    .x0(d => d.x0)
    .x1(d => d.x1)
    .y0(d => d.y0)
    .y1(d => d.y1);

    // console.log("iqrData");
    // console.log(iqrData);
    let pDataset = [];
    let _data_q1 = {};
    let _data_m = {};
    let _data_q3 = {};
    for(let i=0; i<iqrData.length; i++){
      _data_q1[iqrData[i][0]] = +iqrData[i][1];
      _data_m[iqrData[i][0]] = +iqrData[i][2];
      _data_q3[iqrData[i][0]] = +iqrData[i][3];
    }
    pDataset.push(_data_q1);
    pDataset.push(_data_m);
    pDataset.push(_data_q3);
    // console.log("pDataset");
    // console.log(pDataset);
    
    // let valueMin = 0;
    // let valueMax = 0;
    let radialScale = d3.scaleLinear()
    .domain([0, 1])
    .range([0, drawHeight-120]);

    // let tickVal = (valueMax-valueMin)/5;
    // let ticks = [];
    // for(let i=0; i<5; i++){
    //   let _v = (tickVal*(i+1)).toFixed(2);
    //   ticks.push(_v);
    // }
    let ticks = [0.2, 0.4, 0.6, 0.8, 1];

    ticks.forEach(t => 
      svg.append("circle")
      .attr("cx", (drawWidth/2)+margin.left)
      .attr("cy", (drawHeight/2)+margin.top)
      .attr("fill", "none")
      .attr("stroke", "gray")
      .attr("r", radialScale(t))
    );

    ticks.forEach(t =>
      svg.append("text")
      .attr("x", (drawWidth/2)+margin.left)
      .attr("y", (drawHeight/2)+margin.top - radialScale(t))
      .attr("font-family", "Roboto, sans-serif")
      .style("font-size", "6px")
      .text(t.toString())
    );

    function angleToCoordinate(angle, value){
      let x = Math.cos(angle)*radialScale(value);
      let y = Math.sin(angle)*radialScale(value);
      return {"x": (drawWidth/2)+margin.left+x, "y": (drawHeight/2)+margin.top-y};
    }

    for(let i = 0; i < features.length; i++) {
      let ft_name = features[i];
      let angle = (Math.PI / 2) + (2 * Math.PI * i / features.length);
      let line_coordinate = angleToCoordinate(angle, 1);
      let label_coordinate = angleToCoordinate(angle, 1.2);
  
      //draw axis line
      svg.append("line")
      .attr("x1", (drawWidth/2)+margin.left)
      .attr("y1", (drawHeight/2)+margin.top)
      .attr("x2", line_coordinate.x)
      .attr("y2", line_coordinate.y)
      .attr("stroke","gray");
  
      //draw axis label
      svg.append("text")
      .attr("x", label_coordinate.x)
      .attr("y", label_coordinate.y)
      .attr("font-family", "Roboto, sans-serif")
      .style("font-size", "6px")
      .text(ft_name);
    }

    for (var i = 0; i<pDataset.length; i++){
      if(i%3 == 2){
        continue;
      }
      let color = colores_g[parseInt(i/3)];

      if(i%3 == 0){
        let q1 = pDataset[i];
        let q3 = pDataset[i+2];
        let coordinates_q1 = getPathCoordinates(q1);
        let coordinates_q3 = getPathCoordinates(q3);
        let coordinates = [];
        for(let j=0; j<coordinates_q1.length; j++){
          let _x0 = coordinates_q1[j].x;
          let _x1 = coordinates_q3[j].x;
          let _y0 = coordinates_q1[j].y;
          let _y1 = coordinates_q3[j].y;
          
          let _a = {
            x0: _x0,
            x1: _x1,
            y0: _y0,
            y1: _y1
          }
          coordinates.push(_a);
        }
        
        svg.append("path")
        .datum(coordinates)
        .attr("class", "area")
        .attr("d", area)
        .style("fill", color)
        .style("opacity", 0.4);
      }

      if(i%3 == 1){
        let m = pDataset[i];
        let coordinates_m = getPathCoordinates(m);
        let q1 = pDataset[i-1];
        let q3 = pDataset[i+1];
        let coordinates_q1 = getPathCoordinates(q1);
        let coordinates_q3 = getPathCoordinates(q3);
        
        //draw the path element
        svg.append("path")
        .datum(coordinates_q1)
        .attr("d", line)
        .attr("stroke-width", 1)
        .attr("stroke", color)
        .attr("stroke-opacity", 1)
        .attr("fill", "none")
        .attr("opacity", 1);

        svg.append("path")
        .datum(coordinates_m)
        .attr("d", line)
        .attr("stroke-width", 2)
        .attr("stroke", color)
        .attr("stroke-opacity", 1)
        .attr("fill", "none")
        .attr("opacity", 1);

        svg.append("path")
        .datum(coordinates_q3)
        .attr("d", line)
        .attr("stroke-width", 1)
        .attr("stroke", color)
        .attr("stroke-opacity", 1)
        .attr("fill", "none")
        .attr("opacity", 1);

      }
    }


    function getPathCoordinates(data_point){
      let coordinates = [];
      for (var i = 0; i < features.length; i++){
          let ft_name = features[i];
          let angle = (Math.PI / 2) + (2 * Math.PI * i / features.length);
          coordinates.push(angleToCoordinate(angle, data_point[ft_name]));
      }
      return coordinates;
    }
  }, [props.iqrData]);
  
  return (
    <>
      {iqrData.length !== 0 && 
        <svg ref={svgRef}>
        </svg>
      }
    </>
  );
}

export default StiRadarChart;