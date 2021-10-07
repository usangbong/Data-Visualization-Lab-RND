def svg_vlSpec(cnt_create, vlSpec):
    svg = '''
        var vlSpec = ''' + str(vlSpec) + ''';
        vegaEmbed('#vis''' + str(cnt_create) + ''' #vlSpec', vlSpec, {"actions": false});
    '''
    return svg

def svg_bar1(cnt_create, max_value):
    svg = '''
        var margin_bar = {''' + '''top: 20, right: 60, bottom: 50, left: 60},
            width = 500 - margin_bar.left - margin_bar.right,
            height = 280 - margin_bar.top - margin_bar.bottom;

        var svg_bar1_''' + str(cnt_create) + ''' = d3v4.select("#vis''' + str(cnt_create) + ''' #bar1")
            .append("svg")
                .attr("width", width + margin_bar.left + margin_bar.right)
                .attr("height", height + margin_bar.top + margin_bar.bottom)
            .append("g")
                .attr("transform",
                    "translate(" + margin_bar.left + "," + margin_bar.top + ")");

        d3v4.csv("static/data/bar_''' + str(cnt_create) + '''.csv", function(data) {
            var bar_subgroups = data.columns.slice(1)
            var bar_groups = d3v4.map(data, function(d){return(d.index)}).keys()

            var x1 = d3v4.scaleBand()
                .domain(bar_groups)
                .range([0, width - 150])
                .padding([0.2])
            svg_bar1_''' + str(cnt_create) + '''.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3v4.axisBottom(x1).tickSize(0));

            var y1 = d3v4.scaleLinear()
                .domain([0, ''' + str(max_value) + '''])
                .range([height, 0]);
            svg_bar1_''' + str(cnt_create) + '''.append("g")
                .call(d3v4.axisLeft(y1));

            var xSubgroup = d3v4.scaleBand()
                .domain(bar_subgroups)
                .range([0, x1.bandwidth()])
                .padding([0.05])

            var color = d3v4.scaleOrdinal()
                .domain(bar_subgroups)
                .range(['#377eb8','#4daf4a'])

            svg_bar1_''' + str(cnt_create) + '''.append("g")
                .selectAll("g")
                .data(data)
                .enter()
                .append("g")
                .attr("transform", function(d) { return "translate(" + x1(d.index) + ",0)"; })
                .selectAll("rect")
                .data(function(d) { return bar_subgroups.map(function(key) { return {key: key, value: d[key]}; }); })
                .enter().append("rect")
                .attr("x", function(d) { return xSubgroup(d.key); })
                .attr("y", function(d) { return y1(d.value); })
                .attr("width", xSubgroup.bandwidth())
                .attr("height", function(d) { return height - y1(d.value); })
                .attr("fill", function(d) { return color(d.key); });
            })

        svg_bar1_''' + str(cnt_create) + '''.append("circle").attr("cx", 240).attr("cy", 0).attr("r", 6).style("fill", "#377eb8")
        svg_bar1_''' + str(cnt_create) + '''.append("text").attr("x", 250).attr("y", 0).text("missing").style("font-size", "15px").attr("alignment-baseline","middle")
        svg_bar1_''' + str(cnt_create) + '''.append("circle").attr("cx", 240).attr("cy", 20).attr("r", 6).style("fill", "#4daf4a")
        svg_bar1_''' + str(cnt_create) + '''.append("text").attr("x", 250).attr("y", 20).text("extreme").style("font-size", "15px").attr("alignment-baseline","middle")
    '''
    return svg

def svg_bar2(cnt_create, max_value):
    svg = '''
        var svg_bar2_''' + str(cnt_create) + ''' = d3v4.select("#vis''' + str(cnt_create) + ''' #bar2")
            .append("svg")
                .attr("width", width + margin_bar.left + margin_bar.right)
                .attr("height", height + margin_bar.top + margin_bar.bottom)
            .append("g")
                .attr("transform",
                    "translate(" + margin_bar.left + "," + margin_bar.top + ")");

        d3v4.csv("static/data/bar_''' + str(cnt_create) + '''.csv", function(data) {
            var bar_subgroups = data.columns.slice(1)
            var bar_groups = d3v4.map(data, function(d){return(d.index)}).keys()

            var x2 = d3v4.scaleBand()
                .domain(bar_groups)
                .range([0, width - 150])
                .padding([0.5])
            svg_bar2_''' + str(cnt_create) + '''.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3v4.axisBottom(x2).tickSizeOuter(0));

            var y2 = d3v4.scaleLinear()
                .domain([0, ''' + str(max_value) + '''])
                .range([height, 0]);
            svg_bar2_''' + str(cnt_create) + '''.append("g")
                .call(d3v4.axisLeft(y2));

            var color = d3v4.scaleOrdinal()
                .domain(bar_subgroups)
                .range(['#377eb8','#4daf4a'])

            var stackedData = d3v4.stack()
                .keys(bar_subgroups)
                (data)

            svg_bar2_''' + str(cnt_create) + '''.append("g")
                .selectAll("g")
                .data(stackedData)
                .enter().append("g")
                .attr("fill", function(d) { return color(d.key); })
                .selectAll("rect")

                .data(function(d) { return d; })
                .enter().append("rect")
                    .attr("x", function(d) { return x2(d.data.index); })
                    .attr("y", function(d) { return y2(d[1]); })
                    .attr("height", function(d) { return y2(d[0]) - y2(d[1]); })
                    .attr("width", x2.bandwidth())
            })

        svg_bar2_''' + str(cnt_create) + '''.append("circle").attr("cx", 240).attr("cy", 0).attr("r", 6).style("fill", "#377eb8")
        svg_bar2_''' + str(cnt_create) + '''.append("text").attr("x", 250).attr("y", 0).text("missing").style("font-size", "15px").attr("alignment-baseline","middle")
        svg_bar2_''' + str(cnt_create) + '''.append("circle").attr("cx", 240).attr("cy", 20).attr("r", 6).style("fill", "#4daf4a")
        svg_bar2_''' + str(cnt_create) + '''.append("text").attr("x", 250).attr("y", 20).text("extreme").style("font-size", "15px").attr("alignment-baseline","middle")
    '''
    return svg

def svg_heatmap(cnt_create, col, target_col, state, div_name):
    svg = '''
        var margin_heatmap = {''' + '''top: 20, right: 60, bottom: 50, left: 60},
            width = 500 - margin_heatmap.left - margin_heatmap.right,
            height = 280 - margin_heatmap.top - margin_heatmap.bottom;

        var svg_heatmap''' + str(state) + '''_''' + str(cnt_create) + ''' = d3v4.select("#vis''' + str(cnt_create) + ''' #''' + str(div_name) + '''")
            .append("svg")
            .attr("width", width + margin_heatmap.left + margin_heatmap.right)
            .attr("height", height + margin_heatmap.top + margin_heatmap.bottom)
            .append("g")
            .attr("transform",
                    "translate(" + margin_heatmap.left + "," + margin_heatmap.top + ")");

        var heatmap_groups = ''' + str(col) + '''
        var heatmap_y = ["20", "40", "60", "80", "100", "120", "140", "160", "180", "200"]

        var x = d3v4.scaleBand()
            .range([ 0, width - 100])
            .domain(heatmap_groups)
            .padding(0.01);
        svg_heatmap''' + str(state) + '''_''' + str(cnt_create) + '''.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3v4.axisBottom(x))

        var y = d3v4.scaleBand()
            .range([ height, 10 ])
            .domain(heatmap_y)
            .padding(0.01);
        svg_heatmap''' + str(state) + '''_''' + str(cnt_create) + '''.append("g")
            .call(d3v4.axisLeft(y));

        var color1 = d3v4.scaleLinear()
            .range(["white", "#464646"])
            .domain([1, 100])

        var color2 = d3v4.scaleLinear()
            .range(["white", "red"])
            .domain([1, 100])

        d3v4.csv("static/data/heatmap''' + str(state) + '''_''' + str(cnt_create) + '''.csv", function(data) {
        var tooltip = d3v4.select("#vis''' + str(cnt_create) + ''' #''' + str(div_name) + '''")
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "2px")
            .style("border-radius", "5px")
            .style("padding", "5px")

        svg_heatmap''' + str(state) + '''_''' + str(cnt_create) + '''.selectAll()
            .data(data, function(d) {return d.index + ':' + d.y;})
            .enter()
            .append("rect")
            .attr("x", function(d) { return x(d.index) })
            .attr("y", function(d) { return y(d.y) })
            .attr("width", x.bandwidth() )
            .attr("height", y.bandwidth() )
            .style("fill", function(d) {
                if (d.index == "''' + str(target_col) + '''") { return color2(d.value * 20); }
                else { return color1(d.value * 20); }
                })
        })

        svg_heatmap''' + str(state) + '''_''' + str(cnt_create) + '''.append("text")
            .attr("x", 0)
            .attr("y", 0)
            .attr("text-anchor", "left")
            .style("font-size", "14px")
            .style("fill", "#464646")
            .style("max-width", 400)
            .text("show missing value distribution");
    '''
    return svg

def svg_histogram(cnt_create, col, target_col, lower, upper, state, div_name):
    svg = '''
        var margin_histogram = {''' + '''top: 20, right: 60, bottom: 50, left: 60},
            width = 500 - margin_histogram.left - margin_histogram.right,
            height = 280 - margin_histogram.top - margin_histogram.bottom;

        var svg_histogram''' + str(state) + '''_''' + str(cnt_create) + ''' = d3v4.select("#vis''' + str(cnt_create) + ''' #''' + div_name + '''")
            .append("svg")
            .attr("width", width + margin_histogram.left + margin_histogram.right)
            .attr("height", height + margin_histogram.top + margin_histogram.bottom)
            .append("g")
            .attr("transform",
                    "translate(" + margin_histogram.left + "," + margin_histogram.top + ")");

        d3v4.csv("static/data/histogram''' + str(state) + '''_''' + str(cnt_create) + '''.csv", function(data) {
        var x = d3v4.scaleLinear()
            .domain([d3v4.min(data, function(d) { return +d.''' + str(target_col) + '''; }), d3v4.max(data, function(d) { return +d.''' + str(target_col) + '''; })])
            .range([0, width - 150]);
        svg_histogram''' + str(state) + '''_''' + str(cnt_create) + '''.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3v4.axisBottom(x));

        var histogram = d3v4.histogram()
            .value(function(d) { return d.''' + str(target_col) + '''; })
            .domain(x.domain())
            .thresholds(x.ticks(70));

        var bins = histogram(data);

        var y = d3v4.scaleLinear()
            .range([height, 10]);
            y.domain([0, d3v4.max(bins, function(d) { return d.length; })]);
        svg_histogram''' + str(state) + '''_''' + str(cnt_create) + '''.append("g")
            .call(d3v4.axisLeft(y));

        svg_histogram''' + str(state) + '''_''' + str(cnt_create) + '''.selectAll("rect")
            .data(bins)
            .enter()
            .append("rect")
                .attr("x", 1)
                .attr("transform", function(d) { return "translate(" + x(d.x0) + "," + y(d.length) + ")"; })
                .attr("width", function(d) { return x(d.x1) - x(d.x0) - 1 ; })
                .attr("height", function(d) { return height - y(d.length); })
                .style("fill", function(d) {
                    if (d.x0 > ''' + str(upper) + ''') { return "red"; }
                    else if (d.x0 < ''' + str(lower) + ''') { return "red"; }
                    else { return "grey"; }
                })
        });

        svg_histogram''' + str(state) + '''_''' + str(cnt_create) + '''.append("text")
            .attr("x", 0)
            .attr("y", 0)
            .attr("text-anchor", "left")
            .style("font-size", "14px")
            .style("fill", "grey")
            .style("max-width", 400)
            .text("show extreme value distribution");
    '''
    return svg