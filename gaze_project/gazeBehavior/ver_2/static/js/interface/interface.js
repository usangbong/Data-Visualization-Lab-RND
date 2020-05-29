let stiGrid = [];
let AOIarray = [];
let selectedAppendCell = [];
//let AOIcolorBrewer_12class_set3 = ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f"];
let AOIcolorBrewer_12class_set3 = ["#e31a1c", "#a6cee3", "#33a02c", "#ff7f00", "#b15928", "#ffff99", "#6a3d9a", "#fdbf6f", "#b2df8a", "#1f78b4", "#fb9a99", "#cab2d6"];
let SELECTED_AOI = -999;
let selectedDeleteCell = [];

let temp = [];
let __t = [];
let _t = {
	'x': 412.4542124669535, 'y': 306.7882471890983, 'duration': 47, 'clss': 0
};
__t.push(_t);
_t = {
	'x': 410.989011, 'y': 311.8541033, 'duration': 1, 'clss': 3
};
__t.push(_t);
_t = {
	'x': 537.7335649980503, 'y': 301.41225397938206, 'duration': 16, 'clss': 1
};
__t.push(_t);
_t = {
	'x': 692.3076923, 'y': 284.4984802, 'duration': 1, 'clss': 2
};
__t.push(_t);
_t = {
	'x': 722.469400633399, 'y': 268.30750977413163, 'duration': 49, 'clss': 0
};
__t.push(_t);
_t = {
	'x': 740.6593407, 'y': 260.7902736, 'duration': 1, 'clss': 3
};
__t.push(_t);
_t = {
	'x': 750.7455507393778, 'y': 245.07076847017288, 'duration': 9, 'clss': 1
};
__t.push(_t);
_t = {
	'x': 756.043956, 'y': 213.3738602, 'duration': 1, 'clss': 2
};
__t.push(_t);
temp.push(__t);

// update data panel
let iDataColumns = $('#data_columns');
//iDataColumns.append("<br>");
//let dlColumns = $(`
//	<selectgroup>
//       <option value="d_x">x</option>
//        <option value="d_y">y</option>
//    </selectgroup>
//`);

//iDataColumns.append(dlColumns);

let iMeasurement = $('#data_measurement');
iMeasurement.append("<br>");
let dlMeasurement = $(`
	<input type='radio' value='m_duration' checked/>
	<label>duration</label>
	<input type='radio' value='m_pupil_diameter' />
	<label>pupil diameter</label>
`);
iMeasurement.append(dlMeasurement);

let iEvent = $('#data_event');
iEvent.append("<br>");
let dlEvent = $(`
	<input type='checkbox' id="e_fix" name='e_fix' checked/>
	<label for="e_fix">fixation</label>
	<input type='checkbox' id="e_sac" name='e_sac' checked/>
	<label for="e_sac">saccade</label>
	<input type='checkbox' id="e_pso" name='e_pso' />
	<label for="e_pso">PSO</label>
	<input type='checkbox' id="e_bli" name='e_bli' />
	<label for="e_bli">blink</label>
	<input type='checkbox' id="e_unk" name='e_unk' />
	<label for="e_unk">unknown</label>
`);
iEvent.append(dlEvent);



drawGridHeat_fixDur(temp);

function initInterface(){
        
}

function drawGridHeat_fixDur(dataset){
	console.log("drawGridHeat_fixDur");
	
	let dim_1 = [];
	let dim_2 = [];
	let _value = [];
	for(let i=0; i<dataset.length; i++){
		let _v = [];
		
		for(let j=0; j<dataset[i].length; j++){
			dim_2.push("t"+(j+1).toString());
			_v.push(dataset[i][j].duration);
		}
		dim_1.push("o"+(i+1).toString());
		_value.push(_v);
	}

	// make index data (instead *.tsv file)
	let indexData = [];
	for(let i=0; i<dim_1.length; i++){
		if (i==0){
			indexData.push(["dim1", "dim2"]);
		}
		for(let j=0; j<dim_2.length; j++){
			indexData.push([i+1, j+1]);
		}
	}

	// make input data: index & value
	let inputdata = [];
	for(let i=1; i<indexData.length; i++){
		let _row = [indexData[i][0], indexData[i][1], _value[indexData[i][0]-1][i-1]];
		inputdata.push(_row);
	}
	//console.log(inputdata);

	//UI configuration
	const margin = { top: 50, right: 0, bottom: 100, left: 30 },
		width = 400 - margin.left - margin.right,
		height = 430 - margin.top - margin.bottom,
		gridSize = Math.floor(width / 10),
		legendElementWidth = gridSize*1,
		buckets = 9,
		colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"]; // alternatively colorbrewer.YlGnBu[9]

	var svg = d3.select("body").append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	const yLabel = svg.selectAll(".yLabel")
		.data(dim_1)
		.enter().append("text")
			.text(function(d){return d;})
			.attr("x",0)
			.attr("y", function(d, i){return i*gridSize;})
		.style("text-anchor", "end")
		.attr("transform", "translate(-6,"+gridSize/1.5+")");

	const xLabel = svg.selectAll(".xLabel")
		.data(dim_2)
		.enter().append("text")
			.text(function(d){return d;})
			.attr("x", function(d, i){return i*gridSize;})
			.attr("y",0)
		.style("text-anchor", "middle")
		.attr("transform", "translate(" + gridSize / 2 + ", -6)");

	const heatmapChart = function(_data){
		//console.log(_data);
		const colorScale = d3.scaleQuantile()
            .domain([0, buckets - 1, d3.max(_data, function(d){return d[2];})])
            .range(colors);

        const cards = svg.selectAll(".card")
        	.data(_data, function(d){return d[0]+':'+d[1];});
    	cards.append("title");

    	cards.enter().append("rect")
    		.attr("x", function(d){return (d[1]-1)*gridSize;})
    		.attr("y", function(d){return (d[0]-1)*gridSize;})
    		.attr("rx", 4)
    		.attr("ry", 4)
    		.attr("width", gridSize)
    		.attr("height", gridSize)
    		.style("fill", colors[0])
		.merge(cards)
			.transition()
			.duration(1000)
			.style("fill", function(d){return colorScale(d[2]);});

		cards.select("title").text(function(d){return d[2];});
		cards.exit().remove();

		const legend = svg.selectAll(".legend")
			.data([0].concat(colorScale.quantiles()), function(d){return d;});

		const legend_g = legend.enter().append("g")
			.attr("class", "legend");

		legend_g.append("rect")
			.attr("x", function(d, i){return legendElementWidth*i;})
			.attr("y", height)
			.attr("width", legendElementWidth)
			.attr("height", gridSize/2)
			.style("fill", function(d, i){return colors[i];});

		legend_g.append("text")
			.attr("class", "mono")
			.text(function(d){return "≥ "+Math.round(d);})
			.attr("x", function(d, i){return legendElementWidth*i;})
			.attr("y", height + gridSize);

		legend.exit().remove();
	}
	heatmapChart(inputdata);
}

selectAOIgrid([0,0], 10, 10);

function selectAOIgrid(dataset, setRow, setCol){
	// UI setting: "ADD" & "CLEAR" button
	let AOIselector = $('#aoi_selector');
	AOIselector.append("<br>");

	let xpos = 5;
	let ypos = 5;
	let width = 30;
	let height = 30;
	let click = 0;
	let opacityVal = 0.4;

	for(let _r=0; _r<setRow; _r++){
		let _row = [];

		for(let _c=0; _c<setCol; _c++){
			let _col = {
				x: xpos,
				y: ypos,
				width: width,
				height: height,
				click: click,
				group: 0
			};

			_row.push(_col);
			xpos += width;
		}
		stiGrid.push(_row);

		xpos = 5;
		ypos += height;
	}

	d3.select("#aoi_selector").append("button")
		.text("ADD")
		.on("click", function(){
			SELECTED_AOI = -999;
			if(selectedAppendCell.length != 0){
				// push grid cell array in AOIarray
				let _add = [];
				for(let i=0; i<selectedAppendCell.length; i++){
					_add.push(selectedAppendCell[i])
					let _r = selectedAppendCell[i][0];
					let _c = selectedAppendCell[i][1];

					// set AOI group
					stiGrid[_r][_c].group = AOIarray.length+1;
					//stiGrid[_r][_c].click = -999;
					//console.log(stiGrid[_r][_c]);
				}
				AOIarray.push(_add);

				// clear selectedAppendCell
				selectedAppendCell = [];
			}

			let grid = d3.select("#aoi_selector").selectAll("svg");
			let row = grid.selectAll(".row")
				.data(stiGrid);

			let column = row.selectAll(".square")
				.data(function(d){return d;});

			column.exit().remove();
			column.enter().append("rect")
				.attr("x", 0)
				.attr("y", 0)
				.attr("opacity", opacityVal)
				.attr("width", function(d){return d.width;})
				.attr("height", function(d){return d.height;})
				.style("fill", "red")
				.style("stroke", "#222");

			column.transition()
				.duration(500)
				.attr("opacity", opacityVal)
				.attr("x", function(d){return d.x;})
				.attr("y", function(d){return d.y;})
				.style("fill", function(d, i){
					if(d.group == 0){
						return "#fff";
					}else{
						return AOIcolorBrewer_12class_set3[(d.group)+1];
					}
				});
		});

	d3.select("#aoi_selector").append("button")
		.text("DELETE")
		.on("click", function(){
			if(selectedDeleteCell.length != 0){
				// push grid cell array in AOIarray
				let _dell = [];
				for(let i=0; i<selectedDeleteCell.length; i++){
					_dell.push(selectedDeleteCell[i])
					let _r = selectedDeleteCell[i][0];
					let _c = selectedDeleteCell[i][1];

					// set AOI group
					stiGrid[_r][_c].group = 0;
					stiGrid[_r][_c].click = 0;
					//console.log(stiGrid[_r][_c]);
				}
				for(let i=0; i<_dell.length; i++){
					let dellIdx = 0;
					for(let j=0; j<AOIarray[SELECTED_AOI-1].length; j++){
						if((AOIarray[SELECTED_AOI-1][j][0] == _dell[i][0]) && (AOIarray[SELECTED_AOI-1][j][1] == _dell[i][1])){
							dellIdx = j;
							break;
						}

					}
					AOIarray[SELECTED_AOI-1].splice(dellIdx,1);
				}

				// clear selectedDeleteCell
				selectedDeleteCell = [];
			}
			SELECTED_AOI = -999;

			let grid = d3.select("#aoi_selector").selectAll("svg");
			let row = grid.selectAll(".row")
				.data(stiGrid);

			let column = row.selectAll(".square")
				.data(function(d){return d;});

			column.exit().remove();
			column.enter().append("rect")
				.attr("x", 0)
				.attr("y", 0)
				.attr("opacity", opacityVal)
				.attr("width", function(d){return d.width;})
				.attr("height", function(d){return d.height;})
				.style("fill", "red")
				.style("stroke", "#222");

			column.transition()
				.duration(500)
				.attr("opacity", opacityVal)
				.attr("x", function(d){return d.x;})
				.attr("y", function(d){return d.y;})
				.style("fill", function(d, i){
					if(d.group == 0){
						return "#fff";
					}else{
						return AOIcolorBrewer_12class_set3[(d.group)+1];
					}
				});
		});

	let grid = d3.select("#aoi_selector").append("svg")
		.attr("width", "310px")
		.attr("height", "310px");

	let stimulus = grid.append("image")
		.attr("xlink:href", "http://127.0.0.1:8000/static/stimulus/U0121_1RTE.jpg")
		.attr("width", "310px")
		.attr("height", "310px");


	let row = grid.selectAll(".row")
		.data(stiGrid)
		.enter().append("g")
		.attr("class", "row");

	let column = row.selectAll(".square")
		.data(function(d){return d;})
		.enter().append("rect")
		.attr("class", "square")
		.attr("opacity", opacityVal)
		.attr("x", function(d){return d.x;})
		.attr("y", function(d){return d.y;})
		.attr("width", function(d){return d.width;})
		.attr("height", function(d){return d.height;})
		.style("fill", "#fff")
		.style("stroke", "#222")
		.on("click", function(d, i){
			d.click++;
			let gridArray = [Math.floor(d.y/d.height), i];
			//console.log(gridArray);
			if(d.group==0){
				if((d.click)%2==0){ 
					d3.select(this).style("fill", "#fff");
					selectedAppendCell.splice(selectedAppendCell.indexOf(gridArray),1);
				}
				if((d.click)%2==1){ 
					d3.select(this).style("fill", AOIcolorBrewer_12class_set3[0]);
					selectedAppendCell.push(gridArray);
				}
			}else{
				// d.group!=0
				if(SELECTED_AOI < 0){
					SELECTED_AOI = d.group;
				}

				if(SELECTED_AOI == d.group){
					if((d.click)%2==0){ 
						d3.select(this).style("fill", "black");
						selectedDeleteCell.push(gridArray);
					}
					if((d.click)%2==1){ 
						d3.select(this).style("fill", AOIcolorBrewer_12class_set3[d.group+1]);
						selectedDeleteCell.splice(selectedDeleteCell.indexOf(gridArray),1);
					}
				}	
			}
			//console.log(selectedAppendCell);
		});
}


