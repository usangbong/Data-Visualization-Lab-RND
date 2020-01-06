function drawline(data,f) {
    // 2. Use the margin convention practice
    var margin = {top:10, right: 20, bottom:20, left: 40}
      , width = 170 // Use the window's width
      , height = 40,
      padding = 0; // Use the window's height
    // The number of datapoints
    var n = 24;
    // 5. X scale will use the index of our data
    var xScale = d3.scaleLinear()
        .domain([0, n-1]) // input
        .range([0, width]); // output
    // 6. Y scale will use the randomly generate number
    var yScale = d3.scaleLinear()
        .domain([d3.min(data,function(d){return Math.min(d[f])}), d3.max(data,function(d){return 0.15+Math.max(d[f])})]) // input
        .range([height, 0]); // output
    // 7. d3's line generator
    var line = d3.line()
        .x(function(d, i) { return xScale(d.time); }) // set the x values for the line generator
        .y(function(d) { return yScale(d[f]); }) // set the y values for the line generator
        .curve(d3.curveMonotoneX) // apply smoothing to the line
    // 1. Add the SVG to the page and employ #2
    var svg = d3.select("#lineplot").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // 3. Call the x axis in a group tag
    svg.append("g")
    .style("font-size","7px")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom

    // 4. Call the y axis in a group tag
    svg.append("g")
    .style("font-size","5px")
    .style("fill","white")
        .attr("class", "y axis")
        .call(d3.axisLeft(yScale).ticks(3)); // Create an axis component with d3.axisLeft

    svg.append("text")
        .attr("transform", "translate(" +( margin.left+10) + "," +( margin.top-10) + ")")
        .attr("x", padding)
        .attr("y", padding)
        .attr("dy", ".71em")
        .attr("text-anchor", "middle")
		   .style("fill", "white")
        .text(f);

    // 9. Append the path, bind the data, and call the line generator
    svg.append("path")
        .datum(data) // 10. Binds data to the line
        .attr("class", "line") // Assign a class for styling
        .attr("d", line); // 11. Calls the line generator

    // 12. Appends a circle for each datapoint
    svg.selectAll(".dot")
        .data(data)
      .enter().append("circle") // Uses the enter().append() method
        .attr("class", "dot") // Assign a class for styling
        .attr("cx", function(d) { return xScale(d.time) })
        .attr("cy", function(d) { return yScale(d[f])})
        .attr("r", 2)//dot size
    }
drawline(micData,"noise");
drawline(micData,"temp");
drawline(micData,"humi");
drawline(micData,"pm25");
