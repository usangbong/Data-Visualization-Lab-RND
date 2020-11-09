import React, { useEffect, useRef } from 'react';
import axios from 'axios';

function Heatmap(props) {
   const { width, height, dataURL} = props;
   const svgRef = useRef();
   const d3 = window.d3;
   var colOrigin = ["Action", "Affective", "Art", "BlackWhite", "Cartoon", "Fractal", "Indoor", "Inverted", "Jumbled", "LineDrawing", "LowResolution", "Noisy", "Object", "OutdoorManMade", "OutdoorNatural", "Pattern", "Random", "Satelite", "Sketch", "Social"];
   var selectedCols = [];
   var selectedRows = [];

   useEffect(() => {
      if (typeof dataURL !== 'string' && dataURL.length === 0)
         return;
      
      // console.log(svgRef.current)
      
      // set the dimensions and margins of the graph
      var margin = {top: 30, right: 30, bottom: 30, left: 100},
      width = 1800 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

      // append the svg object to the body of the page
      // var svg = d3.select(svgRef.current)
      var svg = d3.select(svgRef.current)
         .attr("width", width + margin.left + margin.right)
         .attr("height", height + margin.top + margin.bottom)
         .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
         .append("g")
            .attr("transform",
                  "translate(" + margin.left + "," + margin.top + ")");

      // Labels of row and columns
      var myGroups = ["Action", "Affective", "Art", "BlackWhite", "Cartoon", "Fractal", "Indoor", "Inverted", "Jumbled", "LineDrawing", "LowResolution", "Noisy", "Object", "OutdoorManMade", "OutdoorNatural", "Pattern", "Random", "Satelite", "Sketch", "Social"]
      var myVars = ["center_bias", "contrast_intensity", "contrast_color", "contrast_orientation", "HOG", "horizontal_line", "LOG_spectrum", "saliency_intensity", "saliency_color", "saliency_orientation", "saliency_computed"]

      // Build X scales and axis:
      var x = d3.scaleBand()
         .range([ 0, width ])
         .domain(myGroups)
         .padding(0.01);
      svg.append("g")
         .attr("class", "xaxis")
         .attr("transform", "translate(0," + height + ")")
         .attr("stroke", function(d){
            var _selected = false;
            for(var i=0; i<selectedCols.length; i++){
               if(d === selectedCols[i]){
                  _selected = true;
                  break;
               }
            }
            if(_selected){
               return "red";
            }else{
               return "black";
            }
         })
         .call(d3.axisBottom(x))

      d3.selectAll(".xaxis .tick")
         .on('click', function(d){
            var dCheck = 0;
            for(var i=0; i<selectedCols.length; i++){
               if(selectedCols[i] === d){
                  dCheck++;
                  break;
               }
            }
            if(dCheck === 0){
               selectedCols.push(d);
               for(var i=0; i<selectedCols.length; i++){
                  for(var j=0; j<myGroups.length; j++){
                     if(selectedCols[i] === myGroups[j]){
                        myGroups.splice(j, 1);
                        break;
                     }
                  }
               }
            }else{
               myGroups.splice(0, 0, d);
               for(var i=0; i<selectedCols.length; i++){
                  if(selectedCols[i] === d){
                     selectedCols.splice(i, 1);
                  }
               }
            }

            console.log(selectedCols);
            console.log(myGroups);
            d3.selectAll(".xaxis .tick").transition()
               .attr("stroke", function(d){
                  var _selected = false;
                  for(var i=0; i<selectedCols.length; i++){
                     if(d === selectedCols[i]){
                        _selected = true;
                        break;
                     }
                  }
                  if(_selected){
                     return "red";
                  }else{
                     return "black";
                  }
            });

            svg.selectAll("rect").transition()
            .style("fill", function(d){
               var _ccheck = false;
               for(var i=0; i<selectedCols.length; i++){
                  if(d.group === selectedCols[i]){
                     _ccheck = true;
                     break;
                  }
               }
               var _rcheck = false;
               for(var i=0; i<selectedRows.length; i++){
                  if(d.variable === selectedRows[i]){
                     _rcheck = true;
                     break;
                  }
               }

               if(_rcheck || _ccheck){
                  return "#e31a1c";
               }else{
                  if(d.value == -999)
                     return "#fb9a99";
                  else if(d.value < 1)
                     return "#fdbf6f";
                  else
                     return myColor(d.value);
               }
            });
            sendRemoveList(selectedCols, selectedRows);
         });
      
      // Build X scales and axis:
      var y = d3.scaleBand()
         .range([ height, 0 ])
         .domain(myVars)
         .padding(0.01);
      svg.append("g")
         .attr("class", "yaxis")
         .attr("stroke", function(d){
            var _selected = false;
            for(var i=0; i<selectedRows.length; i++){
               if(d === selectedRows[i]){
                  _selected = true;
                  break;
               }
            }
            if(_selected){
               return "red";
            }else{
               return "black";
            }
         })
         .call(d3.axisLeft(y));

      d3.selectAll(".yaxis .tick")
         .on('click', function(d){
            var dCheck = 0;
            for(var i=0; i<selectedRows.length; i++){
               if(selectedRows[i] === d){
                  dCheck++;
                  break;
               }
            }
            if(dCheck === 0){
               selectedRows.push(d);
               for(var i=0; i<selectedRows.length; i++){
                  for(var j=0; j<myVars.length; j++){
                     if(selectedRows[i] === myVars[j]){
                        myVars.splice(j, 1);
                        break;
                     }
                  }
               }
            }else{
               myVars.splice(0, 0, d);
               for(var i=0; i<selectedRows.length; i++){
                  if(selectedRows[i] === d){
                     selectedRows.splice(i, 1);
                  }
               }
            }

            console.log(selectedRows);
            console.log(myVars);
            d3.selectAll(".yaxis .tick").transition()
            .attr("stroke", function(d){
               var _selected = false;
               for(var i=0; i<selectedRows.length; i++){
                  if(d === selectedRows[i]){
                     _selected = true;
                     break;
                  }
               }
               if(_selected){
                  return "red";
               }else{
                  return "black";
               }
            });
            
            svg.selectAll("rect").transition()
            .style("fill", function(d){
               var _rcheck = false;
               for(var i=0; i<selectedRows.length; i++){
                  if(d.variable === selectedRows[i]){
                     _rcheck = true;
                     break;
                  }
               }
               var _ccheck = false;
               for(var i=0; i<selectedCols.length; i++){
                  if(d.group === selectedCols[i]){
                     _ccheck = true;
                     break;
                  }
               }

               if(_rcheck || _ccheck){
                  return "#e31a1c";
               }else{
                  if(d.value == -999)
                     return "#fb9a99";
                  else if(d.value < 1)
                     return "#fdbf6f";
                  else
                     return myColor(d.value);
               }
            });

            sendRemoveList(selectedCols, selectedRows);
         });


      // Build color scale
      var myColor = d3.scaleLinear()
         .range(["#d9d9d9", "#a6cee3"])
         .domain([1,2])

      //Read the data
      // d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/heatmap_data.csv", function(data) {
      d3.csv(dataURL+"?"+Math.random(), function(data) {
         // create a tooltip
         // var tooltip = d3.select(svgRef.current)
         var tooltip = d3.select("#my_dataviz")
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "2px")
            .style("border-radius", "5px")
            .style("padding", "5px")

         // Three function that change the tooltip when user hover / move / leave a cell
         var mouseover = function(d) {
            tooltip.style("opacity", 1)
         }
         var mousemove = function(d) {
            tooltip
               .html("The exact value of<br>this cell is: " + d.value)
               .style("left", (d3.mouse(this)[0]+70) + "px")
               .style("top", (d3.mouse(this)[1]) + "px")
         }
         var mouseleave = function(d) {
            tooltip.style("opacity", 1)
         }

         // add the squares
         svg.selectAll()
         .data(data, function(d) {return d.group+':'+d.variable;})
         .enter()
         .append("rect")
            .attr("x", function(d) { return x(d.group) })
            .attr("y", function(d) { return y(d.variable) })
            .attr("width", x.bandwidth() )
            .attr("height", y.bandwidth() )
            .style("fill", function(d) { 
               if(d.value == -999)
                  return "#fb9a99"
               else if(d.value < 1)
                  return "#fdbf6f"
               else
                  return myColor(d.value);
            } )
         .on("mouseover", mouseover)
         .on("mousemove", mousemove)
         .on("mouseleave", mouseleave)
         })

      function sendRemoveList(_stiClass, _stiFeat){
         const _data = new FormData();
         _data.set('removeClass', _stiClass);
         _data.set('removeFeature', _stiFeat);

         axios.post(`http://${window.location.hostname}:5000/api/data/removefilter`, _data)
         .then(response => {
            if (response.data.status === 'success') {
               alert('data columns changed');
            } else if (response.data.status === 'failed') {
               alert(`Failed change data columns - ${response.data.reason}`);
            }
         }).catch(error => {
            alert(`Error - ${error.message}`);
         });
      }
      
   }, [props.dataURL, ]);

  return (
    <>
      {typeof dataURL === 'string' && dataURL.length > 0 &&
         <div id="my_dataviz">
            <svg ref={svgRef}>
            </svg>
         </div>
      }
    </>
  );
}

export default Heatmap;
