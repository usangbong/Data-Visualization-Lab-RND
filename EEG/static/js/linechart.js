function drawLineChart(dataName, w, h, margin, xaxis, yaxis, labelPos, labelRot, colors, maxSize, condition) {
    var fillArea = condition['fillArea'];
    var isSize = condition['isSize'];

    var width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

    var svg = d3.select('.linechart')
        .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.bottom + margin.top)
        .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    d3.csv('../../../../../static/data/line/' + dataName, function(data) {
        var x = d3.scaleLinear()
            .domain([d3.min(data, function(d) { return +d[xaxis]; }), d3.max(data, function(d) { return +d[xaxis]; })])
            .range([0, width]);
        svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x));

        if(isSize) {
            var y = d3.scaleLinear()
                .domain([0, d3.max(data, function(d) { return +d[yaxis]; }) + maxSize])
                .range([height, 0]);
        }
        else{
            var y = d3.scaleLinear()
                .domain([0, d3.max(data, function(d) { return +d[yaxis]; })])
                .range([height, 0]);
        }
        svg.append('g')
            .call(d3.axisLeft(y));

        var color = colors[0];
        svg.append('path')
            .datum(data)
            .attr('fill', 'none')
            .attr('stroke', color)
            .attr('stroke-width', 1.5)
            .attr('d', d3.line()
                .x(function(d) { return x(d[xaxis]); })
                .y(function(d) { return y(d[yaxis]); })
            )

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

        if(fillArea) {
            svg.append('path')
                .datum(data)
                .style('fill', color)
                .attr('d', d3.area()
                    .x(function(d) { return x(d[xaxis]); })
                    .y0(height)
                    .y1(function(d) { return y(d[yaxis]); })
                )
        }
    })
}

function drawLineChartDate(dataName, w, h, margin, xaxis, yaxis, labelPos, labelRot, colors, fillArea = false, isSize = false, maxSize=0) {
    var width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

    var svg = d3.select('.linechart')
        .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.bottom + margin.top)
        .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    var parseTime = d3.timeParse("%Y-%m-%d");

    d3.csv('../../../../../static/data/line/' + dataName, function(data) {
        var x = d3.scaleTime()
            .domain(d3.extent(data, function(d) { return parseTime(d[xaxis]); }))
            .range([0, width]);
        svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x))
            .selectAll('text')
                .attr('dx', '-25px')
                .attr('dy', '8px')
                .attr('transform', 'rotate(-45)');

        if(isSize) {
            var y = d3.scaleLinear()
                .domain([0, d3.max(data, function(d) { return +d[yaxis]; }) + maxSize])
                .range([height, 0]);
        }
        else {
            var y = d3.scaleLinear()
                .domain([0, d3.max(data, function(d) { return +d[yaxis]; })])
                .range([height, 0]);
        }
        svg.append('g')
            .call(d3.axisLeft(y));

        var color = colors[0];
        svg.append('path')
            .datum(data)
            .attr('fill', 'none')
            .attr('stroke', color)
            .attr('stroke-width', 1.5)
            .attr('d', d3.line()
                .x(function(d) { return x(parseTime(d[xaxis])); })
                .y(function(d) { return y(d[yaxis]); })
            )

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

        if(fillArea) {
            svg.append('path')
                .datum(data)
                .style('fill', color)
                .attr('d', d3.area()
                    .x(function(d) { return x(parseTime(d[xaxis])); })
                    .y0(height)
                    .y1(function(d) { return y(d[yaxis]); })
                )
        }
    })
}

function drawLineChartGroup(dataName, w, h, margin, xaxis, yaxis, ycolumns, labelPos, labelRot, colors, legendposX, xtickPos, maxSize, condition) {
    var fillArea = condition['fillArea'];
    var rotate_xtick = condition['rotate_xtick'];
    var isNumber = condition['isNumber'];
    var isSize = condition['isSize'];

    var width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

    var svg = d3.select('.linechart')
        .append('svg')
            .attr('width', width+margin.left+margin.right)
            .attr('height', height+margin.top+margin.bottom)
        .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    if(isNumber) {
        var x = d3.scaleLinear()
            .range([0, width]);
    }
    else {
        var x = d3.scalePoint()
            .range([0, width]);
    }

    var y = d3.scaleLinear()
        .range([height, 0]);

    var color = d3.scaleOrdinal()
        .range(colors);

    var line = d3.line()
        .x(function(d) { return x(d.name); })
        .y(function(d) { return y(d.value); });

    var area = d3.area()
        .x(function(d) { return x(d.name); })
        .y0(height)
        .y1(function(d) { return y(d.value); });

    d3.csv('../../../../../static/data/line/' + dataName, function(data) {
        color.domain(d3.keys(data[0]).filter(function(key) { return key != xaxis; }));

        var sumstat = color.domain().map(function(name) {
            return {
                name:name,
                values:data.map(function(d) {
                    return {name:d[xaxis], value: +d[name]};
                })
            }
        })

        if(isNumber) x.domain([0, data.length]);
        else x.domain(data.map(function(d) { return d[xaxis]; }));
        if(rotate_xtick) {
            svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x))
            .selectAll('text')
            .attr('dx', xtickpos[0])
            .attr('dy', xtickpos[1])
                .attr('transform', 'rotate(-45)')
        }
        else {
            svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x));
        }

        if(isSize) {
            y.domain([
                d3.min(sumstat, function(s) { return d3.min(s.values, function(v) { return v.value; }); }),
                d3.max(sumstat, function(s) { return d3.max(s.values, function(v) { return v.value; }); }) + maxSize
            ]);
        }
        else {
            y.domain([
                d3.min(sumstat, function(s) { return d3.min(s.values, function(v) { return v.value; }); }),
                d3.max(sumstat, function(s) { return d3.max(s.values, function(v) { return v.value; }); })
            ]);
        }

        svg.append('g')
            .call(d3.axisLeft(y));

        svg.selectAll('.line')
            .data(sumstat)
            .enter().append('path')
            .attr('fill', 'none')
            .attr('stroke', function(d) { return color(d.name); })
            .attr('stroke-width', 1.5)
            .attr('d', function(d) { return line(d.values); })

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

        if(fillArea) {
            svg.selectAll('.area')
                .data(sumstat)
                .enter().append('path')
                .attr('fill', function(d) { return color(d.name); })
                .attr('d', function(d) { return area(d.values); });
        }
    })
}

function drawLineChartGroupDate(dataName, w, h, margin, xaxis, yaxis, ycolumns, labelPos, labelRot, colors, legendposX, xtickPos, maxSize, condition) {
    var fillArea = condition['fillArea'];
    var rotate_xtick = condition['rotate_xtick'];
    var isSize = condition['isSize'];

    var width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

    var svg = d3.select('.linechart')
        .append('svg')
            .attr('width', width+margin.left+margin.right)
            .attr('height', height+margin.top+margin.bottom)
        .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    var parseTime = d3.timeParse("%Y-%m-%d");

    var x = d3.scaleTime()
        .range([0, width]);

    var y = d3.scaleLinear()
        .range([height, 0]);

    var color = d3.scaleOrdinal()
        .range(colors);

    var line = d3.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.value); });

    var area = d3.area()
        .x(function(d) { return x(d.date); })
        .y0(height)
        .y1(function(d) { return y(d.value); });

    d3.csv('../../../../../static/data/line/' + dataName, function(data) {
        color.domain(d3.keys(data[0]).filter(function(key) { return key != xaxis; }));

        var sumstat = color.domain().map(function(name) {
            return {
                name:name,
                values:data.map(function(d) {
                    return {date:parseTime(d[xaxis]), value: +d[name]};
                })
            }
        })

        x.domain(d3.extent(data, function(d) { return parseTime(d[xaxis]); }));
        if(rotate_xtick) {
            svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x))
            .selectAll('text')
            .attr('dx', xtickpos[0])
            .attr('dy', xtickpos[1])
                .attr('transform', 'rotate(-45)')
        }
        else {
            svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x));
        }

        if(isSize) {
            y.domain([
                d3.min(sumstat, function(s) { return d3.min(s.values, function(v) { return v.value; }); }),
                d3.max(sumstat, function(s) { return d3.max(s.values, function(v) { return v.value; }); }) + maxSize
            ]);
        }
        else {
            y.domain([
                d3.min(sumstat, function(s) { return d3.min(s.values, function(v) { return v.value; }); }),
                d3.max(sumstat, function(s) { return d3.max(s.values, function(v) { return v.value; }); })
            ]);
        }

        svg.append('g')
            .call(d3.axisLeft(y));

        svg.selectAll('.line')
            .data(sumstat)
            .enter().append('path')
            .attr('fill', 'none')
            .attr('stroke', function(d) { return color(d.name); })
            .attr('stroke-width', 1.5)
            .attr('d', function(d) { return line(d.values); })

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

        if(fillArea) {
            svg.selectAll('.area')
                .data(sumstat)
                .enter().append('path')
                .attr('fill', function(d) { return color(d.date); })
                .attr('d', function(d) { return area(d.values); });
        }
    })
}

function testdrawLineChart(dataName, w, h, margin, xaxis, yaxis, labelPos, labelRot, colors, maxSize, condition) {
    var fillArea = condition['fillArea'];
    var isSize = condition['isSize'];

    var width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

    var svg = d3.select('.linechart')
        .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.bottom + margin.top)
        .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    d3.csv('../../static/data/test/' + dataName, function(data) {
        var x = d3.scaleLinear()
            .domain([d3.min(data, function(d) { return +d[xaxis]; }), d3.max(data, function(d) { return +d[xaxis]; })])
            .range([0, width]);
        svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x));

        if(isSize) {
            var y = d3.scaleLinear()
                .domain([0, d3.max(data, function(d) { return +d[yaxis]; }) + maxSize])
                .range([height, 0]);
        }
        else{
            var y = d3.scaleLinear()
                .domain([0, d3.max(data, function(d) { return +d[yaxis]; })])
                .range([height, 0]);
        }
        svg.append('g')
            .call(d3.axisLeft(y));

        var color = colors[0];
        svg.append('path')
            .datum(data)
            .attr('fill', 'none')
            .attr('stroke', color)
            .attr('stroke-width', 1.5)
            .attr('d', d3.line()
                .x(function(d) { return x(d[xaxis]); })
                .y(function(d) { return y(d[yaxis]); })
            )

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

        if(fillArea) {
            svg.append('path')
                .datum(data)
                .style('fill', color)
                .attr('d', d3.area()
                    .x(function(d) { return x(d[xaxis]); })
                    .y0(height)
                    .y1(function(d) { return y(d[yaxis]); })
                )
        }
    })
}

function testdrawLineChartGroup(dataName, w, h, margin, xaxis, yaxis, ycolumns, labelPos, labelRot, colors, legendposX, xtickPos, maxSize, condition) {
    var fillArea = condition['fillArea'];
    var rotate_xtick = condition['rotate_xtick'];
    var isNumber = condition['isNumber'];
    var isSize = condition['isSize'];

    var width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

    var svg = d3.select('.linechart')
        .append('svg')
            .attr('width', width+margin.left+margin.right)
            .attr('height', height+margin.top+margin.bottom)
        .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    if(isNumber) {
        var x = d3.scaleLinear()
            .range([0, width]);
    }
    else {
        var x = d3.scalePoint()
            .range([0, width]);
    }

    var y = d3.scaleLinear()
        .range([height, 0]);

    var color = d3.scaleOrdinal()
        .range(colors);

    var line = d3.line()
        .x(function(d) { return x(d.name); })
        .y(function(d) { return y(d.value); });

    var area = d3.area()
        .x(function(d) { return x(d.name); })
        .y0(height)
        .y1(function(d) { return y(d.value); });

    d3.csv('../../static/data/test/' + dataName, function(data) {
        color.domain(d3.keys(data[0]).filter(function(key) { return key != xaxis; }));

        var sumstat = color.domain().map(function(name) {
            return {
                name:name,
                values:data.map(function(d) {
                    return {name:d[xaxis], value: +d[name]};
                })
            }
        })

        if(isNumber) x.domain([0, data.length]);
        else x.domain(data.map(function(d) { return d[xaxis]; }));
        if(rotate_xtick) {
            svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x))
            .selectAll('text')
            .attr('dx', xtickpos[0])
            .attr('dy', xtickpos[1])
                .attr('transform', 'rotate(-45)')
        }
        else {
            svg.append('g')
            .attr('transform', 'translate(0,' + height + ')')
            .call(d3.axisBottom(x));
        }

        if(isSize) {
            y.domain([
                d3.min(sumstat, function(s) { return d3.min(s.values, function(v) { return v.value; }); }),
                d3.max(sumstat, function(s) { return d3.max(s.values, function(v) { return v.value; }); }) + maxSize
            ]);
        }
        else {
            y.domain([
                d3.min(sumstat, function(s) { return d3.min(s.values, function(v) { return v.value; }); }),
                d3.max(sumstat, function(s) { return d3.max(s.values, function(v) { return v.value; }); })
            ]);
        }

        svg.append('g')
            .call(d3.axisLeft(y));

        svg.selectAll('.line')
            .data(sumstat)
            .enter().append('path')
            .attr('fill', 'none')
            .attr('stroke', function(d) { return color(d.name); })
            .attr('stroke-width', 1.5)
            .attr('d', function(d) { return line(d.values); })

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

        if(fillArea) {
            svg.selectAll('.area')
                .data(sumstat)
                .enter().append('path')
                .attr('fill', function(d) { return color(d.name); })
                .attr('d', function(d) { return area(d.values); });
        }
    })
}