function drawBarChart(dataName, w, h, margin, xaxis, yaxis, labelPos, labelRot, max, colors, min = 0) {
    var color = colors[0];

    var width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

    var svg = d3.select('.barchart')
        .append('svg')
            .attr('width', width+margin.left+margin.right)
            .attr('height', height+margin.top+margin.bottom)
        .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    d3.csv('../../../../../static/data/bar/' + dataName, function(data) {
        //XAxis
        var x = d3.scaleBand()
            .domain(data.map(function(d) { return d[xaxis]; }))
            .range([0, width])
            .padding(0.2);
        svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x));

        //YAxis
        var y = d3.scaleLinear()
            .domain([min, max])
            .range([height, 0]);
        svg.append('g')
            .call(d3.axisLeft(y));

        svg.append('text')
            .attr('text-anchor', 'end')
            .attr('x', w/2)
            .attr('y', height+labelPos[0])
            .attr('transform', 'rotate(' + labelRot[0] + ')')
            .text(xaxis);

        svg.append('text')
            .attr('text-anchor', 'end')
            .attr('x', -h/2)
            .attr('y', labelPos[1])
            .attr('transform', 'rotate(' + labelRot[1] + ')')
            .text(yaxis);

        svg.selectAll('mybar')
            .data(data)
            .enter().append('rect')
            .attr('x', function(d) { return x(d[xaxis]); })
            .attr('y', function(d) { return y(d[yaxis]); })
            .attr('width', x.bandwidth())
            .attr('height', function(d) { return height - y(d[yaxis]); })
            .attr('fill', color);
    })
}

function drawTriangleBarChart(dataName, w, h, margin, xaxis, yaxis, labelPos, labelRot, triangle_size, max, colors) {
    var color = colors[0];

    var width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

    var svg = d3.select('.barchart')
        .append('svg')
            .attr('width', width+margin.left+margin.right)
            .attr('height', height+margin.top+margin.bottom)
        .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    d3.csv('../../../../../static/data/bar/' + dataName, function(data) {
        //XAxis
        var x = d3.scaleBand()
            .domain(data.map(function(d) { return d[xaxis]; }))
            .range([0, width])
            .padding(0.2);
        svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x));

        //YAxis
        var y = d3.scaleLinear()
            .domain([0, max])
            .range([height, 0]);
        svg.append('g')
            .call(d3.axisLeft(y));

        svg.append('text')
            .attr('text-anchor', 'end')
            .attr('x', w/2)
            .attr('y', height+labelPos[0])
            .attr('transform', 'rotate(' + labelRot[0] + ')')
            .text(xaxis);

        svg.append('text')
            .attr('text-anchor', 'end')
            .attr('x', -h/2)
            .attr('y', labelPos[1])
            .attr('transform', 'rotate(' + labelRot[1] + ')')
            .text(yaxis);

        var triangleWidth = width/data.length - triangle_size;
        for(var i=0;i<data.length;i++) {
            var xcenter = x(data[i][xaxis]) + triangleWidth/2;
            var ypos = y(data[i][yaxis]);

            var top = [xcenter, ypos];
            var left = [xcenter-triangleWidth/2, height];
            var right = [xcenter+triangleWidth/2, height];

            var points = '' + top[0] + ',' + top[1] + ' ' + left[0] + ',' + left[1] + ' ' + right[0] + ',' + right[1];

            svg.append('polygon')
                .attr('points', points)
                .attr('stroke', color)
                .attr('fill', color);
        }
    })
}

function drawBarChartGroup(dataName, w, h, margin, xaxis, yaxis, ycolumns, labelPos, labelRot, legendposX, max, colors, rotate_xtick=false) {
    var width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

    var svg = d3.select('.barchart')
        .append('svg')
            .attr('width', width+margin.left+margin.right)
            .attr('height', height+margin.top+margin.bottom)
        .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    d3.csv('../../../../../static/data/bar/' + dataName, function(data) {
        var subgroups = data.columns.slice(1);
        var groups = d3.map(data, function(d) { return(d[xaxis])}).keys();

        //XAxis
        var x = d3.scaleBand()
            .domain(groups)
            .range([0,width])
            .padding([0.2]);

        if(rotate_xtick) {
        svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x))
            .selectAll('text')
            .style('text-anchor', 'end')
            .attr('dx', '5px')
            .attr('dy', '5px')
            .attr('transform', 'rotate(-45)');
        }

        else {
        svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x).tickSize(0));
        }

        //YAxis
        var y = d3.scaleLinear()
            .domain([0, max])
            .range([height, 0]);
        svg.append('g')
            .call(d3.axisLeft(y));

        var xSubgroup = d3.scaleBand()
            .domain(subgroups)
            .range([0, x.bandwidth()])
            .padding([0.05]);

        var color = d3.scaleOrdinal()
            .domain(subgroups)
            .range(colors);

        svg.append('text')
            .attr('text-anchor', 'end')
            .attr('x', w/2)
            .attr('y', height+labelPos[0])
            .attr('transform', 'rotate(' + labelRot[0] + ')')
            .text(xaxis);

        svg.append('text')
            .attr('text-anchor', 'end')
            .attr('x', -h/2)
            .attr('y', labelPos[1])
            .attr('transform', 'rotate(' + labelRot[1] + ')')
            .text(yaxis);

        svg.append('g')
            .selectAll('g')
            .data(data).enter().append('g')
                .attr('transform', function(d) { return 'translate(' + x(d[xaxis]) + ',0)';})
            .selectAll('rect')
            .data(function(d) { return subgroups.map(function(key) { return {key:key, value:d[key]}; }); })
            .enter().append('rect')
                .attr('x', function(d) { return xSubgroup(d.key); })
                .attr('y', function(d) { return y(d.value); })
                .attr('width', xSubgroup.bandwidth())
                .attr('height', function(d) { return height - y(d.value); })
                .attr('fill', function(d) { return color(d.key); });

        var legendRectSize = 18;
        var legendSpacing = 4;
        var legend = svg.selectAll('.legend')
            .data(color.domain())
            .enter().append('g')
            .attr('class', 'legend')
            .attr('transform', function(d, i) {
                var height = legendRectSize + legendSpacing;
                var offset = height * color.domain().length/2;
                var vert = (i+5)*height - offset;
                return 'translate(' + legendposX + ',' + vert + ')';
        });

        legend.append('rect')
            .attr('width', legendRectSize)
            .attr('height', legendRectSize)
            .style('fill', color)
            .style('stroke', color);

        legend.append('text')
            .attr('x', legendRectSize + legendSpacing)
            .attr('y', legendRectSize - legendSpacing)
            .text(function(d) { return d;});
    })
}

function drawTriangleBarChartGroup(dataName, w, h, margin, xaxis, yaxis, ycolumns, labelPos, labelRot, legendposX, triangle_size, triangle_padding, max, colors) {
    var width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

    var svg = d3.select('.barchart')
        .append('svg')
            .attr('width', width+margin.left+margin.right)
            .attr('height', height+margin.top+margin.bottom)
        .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    d3.csv('../../../../../static/data/bar/' + dataName, function(data) {
        var subgroups = data.columns.slice(1);
        var groups = d3.map(data, function(d) { return(d[xaxis])}).keys();

        //XAxis
        var x = d3.scaleBand()
            .domain(groups)
            .range([0,width])
            .padding(0.2);
        svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x));

        //YAxis
        var y = d3.scaleLinear()
            .domain([0, max])
            .range([height, 0]);
        svg.append('g')
            .call(d3.axisLeft(y));

        var t = [];
        for(var i=0;i<data.length;i++) {
            t.push(x(data[i][xaxis]));
        }

        var barWidth = t[1] - t[0] - triangle_size;
        for(var i=0;i<data.length;i++) {
            for(var s=0;s<subgroups.length;s++) {
                var center = t[i] + barWidth / subgroups.length * s + triangle_padding;
                var tWidth = barWidth / subgroups.length;

                var ypos = y(data[i][subgroups[s]]);

                var top = [center, ypos];
                var left = [center-tWidth/2 ,height];
                var right = [center+tWidth/2 ,height];

                var points = '' + top[0] + ',' + top[1] + ' ' + left[0] + ',' + left[1] + ' ' + right[0] + ',' + right[1];

                var color = colors[s];
                svg.append('polygon')
                    .attr('points', points)
                    .attr('stroke', color)
                    .attr('fill', color);
            }
        }

        var color = d3.scaleOrdinal()
            .range(colors);
        color.domain(d3.keys(data[0]).filter(function(key) { return key != xaxis; }));

        var legendRectSize = 18;
        var legendSpacing = 4;
        var legend = svg.selectAll('.legend')
            .data(color.domain())
            .enter().append('g')
            .attr('class', 'legend')
            .attr('transform', function(d, i) {
                var height = legendRectSize + legendSpacing;
                var offset = height * color.domain().length/2;
                var vert = (i+5)*height - offset;
                return 'translate(' + legendposX + ',' + vert + ')';
        });

        svg.append('text')
            .attr('text-anchor', 'end')
            .attr('x', w/2)
            .attr('y', height+labelPos[0])
            .attr('transform', 'rotate(' + labelRot[0] + ')')
            .text(xaxis);

        svg.append('text')
            .attr('text-anchor', 'end')
            .attr('x', -h/2)
            .attr('y', labelPos[1])
            .attr('transform', 'rotate(' + labelRot[1] + ')')
            .text(yaxis);

        legend.append('rect')
            .attr('width', legendRectSize)
            .attr('height', legendRectSize)
            .style('fill', color)
            .style('stroke', color);

        legend.append('text')
            .attr('x', legendRectSize + legendSpacing)
            .attr('y', legendRectSize - legendSpacing)
            .text(function(d) { return d;});
    })
}

function testdrawBarChart(dataName, w, h, margin, xaxis, yaxis, labelPos, labelRot, max, colors, min = 0) {
    var color = colors[0];

    var width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

    var svg = d3.select('.barchart')
        .append('svg')
            .attr('width', width+margin.left+margin.right)
            .attr('height', height+margin.top+margin.bottom)
        .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    d3.csv('../../static/data/test/' + dataName, function(data) {
        //XAxis
        var x = d3.scaleBand()
            .domain(data.map(function(d) { return d[xaxis]; }))
            .range([0, width])
            .padding(0.2);
        svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x));

        //YAxis
        var y = d3.scaleLinear()
            .domain([min, max])
            .range([height, 0]);
        svg.append('g')
            .call(d3.axisLeft(y));

        svg.append('text')
            .attr('text-anchor', 'end')
            .attr('x', w/2)
            .attr('y', height+labelPos[0])
            .attr('transform', 'rotate(' + labelRot[0] + ')')
            .text(xaxis);

        svg.append('text')
            .attr('text-anchor', 'end')
            .attr('x', -h/2)
            .attr('y', labelPos[1])
            .attr('transform', 'rotate(' + labelRot[1] + ')')
            .text(yaxis);

        svg.selectAll('mybar')
            .data(data)
            .enter().append('rect')
            .attr('x', function(d) { return x(d[xaxis]); })
            .attr('y', function(d) { return y(d[yaxis]); })
            .attr('width', x.bandwidth())
            .attr('height', function(d) { return height - y(d[yaxis]); })
            .attr('fill', color);
    })
}

function testdrawBarChartGroup(dataName, w, h, margin, xaxis, yaxis, ycolumns, labelPos, labelRot, legendposX, max, colors, rotate_xtick=false) {
    var width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

    var svg = d3.select('.barchart')
        .append('svg')
            .attr('width', width+margin.left+margin.right)
            .attr('height', height+margin.top+margin.bottom)
        .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    d3.csv('../../static/data/test/' + dataName, function(data) {
        var subgroups = data.columns.slice(1);
        var groups = d3.map(data, function(d) { return(d[xaxis])}).keys();

        //XAxis
        var x = d3.scaleBand()
            .domain(groups)
            .range([0,width])
            .padding([0.2]);

        if(rotate_xtick) {
        svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x))
            .selectAll('text')
            .style('text-anchor', 'end')
            .attr('dx', '5px')
            .attr('dy', '5px')
            .attr('transform', 'rotate(-45)');
        }

        else {
        svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x).tickSize(0));
        }

        //YAxis
        var y = d3.scaleLinear()
            .domain([0, max])
            .range([height, 0]);
        svg.append('g')
            .call(d3.axisLeft(y));

        var xSubgroup = d3.scaleBand()
            .domain(subgroups)
            .range([0, x.bandwidth()])
            .padding([0.05]);

        var color = d3.scaleOrdinal()
            .domain(subgroups)
            .range(colors);

        svg.append('text')
            .attr('text-anchor', 'end')
            .attr('x', w/2)
            .attr('y', height+labelPos[0])
            .attr('transform', 'rotate(' + labelRot[0] + ')')
            .text(xaxis);

        svg.append('text')
            .attr('text-anchor', 'end')
            .attr('x', -h/2)
            .attr('y', labelPos[1])
            .attr('transform', 'rotate(' + labelRot[1] + ')')
            .text(yaxis);

        svg.append('g')
            .selectAll('g')
            .data(data).enter().append('g')
                .attr('transform', function(d) { return 'translate(' + x(d[xaxis]) + ',0)';})
            .selectAll('rect')
            .data(function(d) { return subgroups.map(function(key) { return {key:key, value:d[key]}; }); })
            .enter().append('rect')
                .attr('x', function(d) { return xSubgroup(d.key); })
                .attr('y', function(d) { return y(d.value); })
                .attr('width', xSubgroup.bandwidth())
                .attr('height', function(d) { return height - y(d.value); })
                .attr('fill', function(d) { return color(d.key); });

        var legendRectSize = 18;
        var legendSpacing = 4;
        var legend = svg.selectAll('.legend')
            .data(color.domain())
            .enter().append('g')
            .attr('class', 'legend')
            .attr('transform', function(d, i) {
                var height = legendRectSize + legendSpacing;
                var offset = height * color.domain().length/2;
                var vert = (i+5)*height - offset;
                return 'translate(' + legendposX + ',' + vert + ')';
        });

        legend.append('rect')
            .attr('width', legendRectSize)
            .attr('height', legendRectSize)
            .style('fill', color)
            .style('stroke', color);

        legend.append('text')
            .attr('x', legendRectSize + legendSpacing)
            .attr('y', legendRectSize - legendSpacing)
            .text(function(d) { return d;});
    })
}