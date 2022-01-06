function start(w, h, filename, link='NASA') {
    var svg = document.getElementsByTagName('svg');
    var image, temp;

    if(svg != null) {
        image = svg[0];
        temp = svg[1];
    }

    if(temp != null) temp.remove();

    d3.select('body')
        .append('div')
        .attr('class', 'sketch');

    var sketch = document.getElementsByClassName('sketch')[0];
    sketch.appendChild(image);

    d3.select('.sketch')
        .append('div')
        .attr('class', 'inputs');

    d3.select('.inputs')
        .append('form')
        .attr('action', '/' + link)
        .attr('method', 'POST')
        .attr('class', 'next')

     d3.select('.inputs').append('div')
        .attr('class', 'reset')

    d3.select('.reset')
        .append('input')
        .attr('type', 'submit')
        .attr('value', 'Reset')
        .attr('class', 'resetbutton')
        .attr('onclick', 'deleteAllPath();')
        .style('margin-right', '15px');

    d3.select('.reset')
        .append('input')
        .attr('type', 'submit')
        .attr('value', 'Save')
        .attr('class', 'savebutton')
        .attr('onclick', 'saveImage(\'' + filename + '\');');

    var div = document.getElementsByTagName('div');
    div[0].remove();

    appendSketchSVG(w, h);
}

var width, height;
function appendSketchSVG(w, h) {
    width = w, height = h;

    var ptdata = [];
    var path;
    var drawing = false;

    var line = d3.line()
        .curve(d3.curveBasis)
        .x(function(d,i) { return d.x; })
        .y(function(d,i) { return d.y; })

    var svg = d3.select('.sketch')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .attr('class', 'sketchpath')
        .style('position', 'absolute')
        .style('top', '0px')
        .style('left', '0px');

    svg.on('mousedown', listen)
        .on('mouseup', ignore)
        .on('mouseleave', ignore);

    function listen() {
        drawing = true;
        ptdata = [];

        path = svg.append('path')
            .data([ptdata])
            .attr('class', 'line')
            .attr('d', line)
            .style('fill', 'none')
            .style('stroke', '#000')
            .style('stroke-width', '2px')
            .style('stroke-linejoin', 'round');;

        svg.on('mousemove', onmove);
    }

    function ignore() {
        svg.on('mousemove', null);
        if(!drawing) return;
        drawing = false;

        tick();
    }

    function onmove(e) {
        var point;

        point = d3.mouse(this);
        ptdata.push({x:point[0], y:point[1]});
        tick();
    }

    function tick() {
        path.attr('d', function(d) { return line(d); })
    }
}

function saveImage(filename) {
    var div = document.getElementsByClassName('sketch')[0];
    html2canvas(div).then(function(canvas) {
        var myImage = canvas.toDataURL();
        downloadURI(myImage, filename + '.png')
    })

    function downloadURI(uri, name){
        console.log(uri)
        var link = document.createElement("a")
        link.download = name;
        link.href = uri;
        document.body.appendChild(link);
        link.click();
        makeNextButton();
    }
}

function makeNextButton() {
    d3.select('.resetbutton')
        .style('display', 'none');
    d3.select('.savebutton')
        .style('display', 'none');

    d3.select('.next')
        .append('input')
        .attr('type', 'submit')
        .attr('value', 'Next')
        .style('position', 'absolute')
        .style('left', '480px');
}

function deleteAllPath() {
    var paths = document.getElementsByClassName('sketchpath')[0];
    paths.remove();
    appendSketchSVG(width, height);
}