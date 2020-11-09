import React, { useEffect, useRef } from 'react';

function CorrelationMatrix(props) {
  const { width, height, data } = props;
  const svgRef = useRef();
  const d3 = window.d3;
  const jz = window.jz;
  const data2grid = window.data2grid;
  const chroma = window.chroma;

  useEffect(() => {
    // if (typeof data !== 'object' || data.length === 0)
    //   return;
    

    var data = [];
    var cols = "abcdefghijklmnopqrstuvwxyz".split("");
    for (var i = 0; i <= 30; i++){
        var obj = {index: i};
        cols.forEach(col => {
            // obj[col] = jz.num.randBetween(1, 100);
            obj[col] = jz.num.randBetween(1, 100);
        });
        data.push(obj);
    }
    var corr = jz.arr.correlationMatrix(data, cols);
    var extent = d3.extent(corr.map(function(d){ return d.correlation; }).filter(function(d){ return d !== 1; }));

    var grid = data2grid.grid(corr);
    var rows = d3.max(grid, function(d){ return d.row; });

    var margin = {top: 20, bottom: 1, left: 20, right: 1};

    var dim = d3.min([window.innerWidth * .9, window.innerHeight * .9]);

    var width = dim - margin.left - margin.right, height = dim - margin.top - margin.bottom;

    // d3.select("#corr").append("div").attr("id", "legend");
    // d3.select("#corr").append("div").attr("id", "grid");    
    d3.select("#corr").append("div").attr("class", "tip").style("display", "none");
    
    // var svg = d3.select("#grid")
    //     .append("svg")
    //         .attr("width", width + margin.left + margin.right)
    //         .attr("height", height + margin.top + margin.bottom)
    //     .append("g")
    //         .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

    var svg = d3.select("#grid")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

    var padding = .1;

    var x = d3.scaleBand()
        .range([0, width])
        .paddingInner(padding)
        .domain(d3.range(1, rows + 1));

    var y = d3.scaleBand()
        .range([0, height])
        .paddingInner(padding)
        .domain(d3.range(1, rows + 1));

    var c = chroma.scale(["tomato", "white", "steelblue"])
        .domain([extent[0], 0, extent[1]]);

    var x_axis = d3.axisTop(y).tickFormat(function(d, i){ return cols[i]; });
    var y_axis = d3.axisLeft(x).tickFormat(function(d, i){ return cols[i]; });

    svg.append("g")
        .attr("class", "x axis")
        .call(x_axis);

    svg.append("g")
        .attr("class", "y axis")
        .call(y_axis);

    svg.selectAll("rect")
        .data(grid, function(d){ return d.column_a + d.column_b; })
        .enter().append("rect")
        .attr("x", function(d){ return x(d.column); })
        .attr("y", function(d){ return y(d.row); })
        .attr("width", x.bandwidth())
        .attr("height", y.bandwidth())
        .style("fill", function(d){ return c(d.correlation); })
        .style("opacity", 1e-6)
        .transition()
        .style("opacity", 1);

    svg.selectAll("rect")

    d3.selectAll("rect")
        .on("mouseover", function(d){
            d3.select(this).classed("selected", true);

            d3.select(".tip")
                .style("display", "block")
                .html(d.column_x + ", " + d.column_y + ": " + d.correlation.toFixed(2));

            var row_pos = y(d.row);
            var col_pos = x(d.column);
            
            var tip_pos = d3.select(".tip").node().getBoundingClientRect();
            var tip_width = tip_pos.width;
            var tip_height = tip_pos.height;
            var grid_pos = d3.select("#grid").node().getBoundingClientRect();
            var grid_left = grid_pos.left;
            var grid_top = grid_pos.top;

            var left = grid_left + col_pos + margin.left + (x.bandwidth() / 2) - (tip_width / 2);
            var top = grid_top + row_pos + margin.top - tip_height - 5;

            d3.select(".tip")
                .style("left", left + "px")
                .style("top", top + "px");

            d3.select(".x.axis .tick:nth-of-type(" + d.column + ") text").classed("selected", true);
            d3.select(".y.axis .tick:nth-of-type(" + d.row + ") text").classed("selected", true);
            d3.select(".x.axis .tick:nth-of-type(" + d.column + ") line").classed("selected", true);
            d3.select(".y.axis .tick:nth-of-type(" + d.row + ") line").classed("selected", true);

        })
        .on("mouseout", function(){
            d3.selectAll("rect").classed("selected", false);
            d3.select(".tip").style("display", "none");
            d3.selectAll(".axis .tick text").classed("selected", false);
            d3.selectAll(".axis .tick line").classed("selected", false);
        });

    // legend scale
    var legend_top = 15;
    var legend_height = 15;
    
    // var legend_svg = d3.select(svgRef.current)
    //     .append("svg")
    //     .attr("width", width + margin.left + margin.right)
    //     .attr("height", legend_height + legend_top)
    //     .append("g")
    //     .attr("transform", "translate(" + margin.left + ", " + legend_top + ")");

    
    var legend_svg = d3.select("#legend").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", legend_height + legend_top)
        .append("g")
        .attr("transform", "translate(" + margin.left + ", " + legend_top + ")");

    var defs = legend_svg.append("defs");

    var gradient = defs.append("linearGradient")
        .attr("id", "linear-gradient");

    var stops = [{offset: 0, color: "tomato", value: extent[0]}, {offset: .5, color: "white", value: 0}, {offset: 1, color: "steelblue", value: extent[1]}];

    gradient.selectAll("stop")
        .data(stops)
        .enter().append("stop")
        .attr("offset", function(d){ return (100 * d.offset) + "%"; })
        .attr("stop-color", function(d){ return d.color; });

    legend_svg.append("rect")
        .attr("width", width)
        .attr("height", legend_height)
        .style("fill", "url(#linear-gradient)");

    legend_svg.selectAll("text")
        .data(stops)
        .enter().append("text")
        .attr("x", function(d){ return width * d.offset; })
        .attr("dy", -3)
        .style("text-anchor", function(d, i){ return i == 0 ? "start" : i == 1 ? "middle" : "end"; })
        .text(function(d, i){ return d.value.toFixed(2) + (i == 2 ? ">" : ""); })

    // // set the dimensions and margins of the graph
    // var margin = {top: 30, right: 30, bottom: 30, left: 100},
    // width = 1800 - margin.left - margin.right,
    // height = 500 - margin.top - margin.bottom;

    // // append the svg object to the body of the page
    // var svg = d3.select(svgRef.current)
    //     .attr("width", width + margin.left + margin.right)
    //     .attr("height", height + margin.top + margin.bottom)
    //     .append("svg")
    //         .attr("width", width + margin.left + margin.right)
    //         .attr("height", height + margin.top + margin.bottom)
    //     .append("g")
    //         .attr("transform",
    //             "translate(" + margin.left + "," + margin.top + ")");

    // // Labels of row and columns
    // var myGroups = ["cetner-bias", "contrast-intensity", "contrast-color", "contrast-orientation", "HOG", "horizontal line", "LOG spectrum", "saliency-intensity", "saliency-color", "saliency-orientation", "computed-saliency"]
    // var myVars = ["cetner-bias", "contrast-intensity", "contrast-color", "contrast-orientation", "HOG", "horizontal line", "LOG spectrum", "saliency-intensity", "saliency-color", "saliency-orientation", "computed-saliency"]

    // // Build X scales and axis:
    // var x = d3.scaleBand()
    //     .range([ 0, width ])
    //     .domain(myGroups)
    //     .padding(0.01);
    // svg.append("g")
    //     .attr("transform", "translate(0," + height + ")")
    //     .call(d3.axisBottom(x))

    // // Build X scales and axis:
    // var y = d3.scaleBand()
    // .range([ height, 0 ])
    // .domain(myVars)
    // .padding(0.01);
    // svg.append("g")
    // .call(d3.axisLeft(y));

    // // Build color scale
    // var myColor = d3.scaleLinear()
    // .range(["#fb8072", "#1f78b4"])
    // .domain([-1,1])

    // //Read the data
    // // d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/heatmap_data.csv", function(data) {
    // d3.csv("http://localhost:5000/static/data/MIT300/usb_02/A_cor.csv", function(data) {
    //     // create a tooltip
    //     var tooltip = d3.select(svgRef.current)
    //     .append("div")
    //     .style("opacity", 0)
    //     .attr("class", "tooltip")
    //     .style("background-color", "white")
    //     .style("border", "solid")
    //     .style("border-width", "2px")
    //     .style("border-radius", "5px")
    //     .style("padding", "5px")

    //     // Three function that change the tooltip when user hover / move / leave a cell
    //     var mouseover = function(d) {
    //     tooltip.style("opacity", 1)
    //     }
    //     var mousemove = function(d) {
    //     tooltip
    //         .html("The exact value of<br>this cell is: " + d.value)
    //         .style("left", (d3.mouse(this)[0]+70) + "px")
    //         .style("top", (d3.mouse(this)[1]) + "px")
    //     }
    //     var mouseleave = function(d) {
    //     tooltip.style("opacity", 0)
    //     }

    //     // add the squares
    //     svg.selectAll()
    //     .data(data, function(d) {return d.group+':'+d.variable;})
    //     .enter()
    //     .append("rect")
    //         .attr("x", function(d) { return x(d.group) })
    //         .attr("y", function(d) { return y(d.variable) })
    //         .attr("width", x.bandwidth() )
    //         .attr("height", y.bandwidth() )
    //         .style("fill", function(d) { return myColor(d.value)} )
    //     .on("mouseover", mouseover)
    //     .on("mousemove", mousemove)
    //     .on("mouseleave", mouseleave)
    //     })
    
    }, []);

    return (
        <>
        {/* {typeof data === 'object' && data.length > 0 && */}
        <div id ="legend"></div>
        <div id ="grid"></div>
            <svg ref={svgRef}>
            </svg>
        {/* } */}
        </>
  );
}

export default CorrelationMatrix;
