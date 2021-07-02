var tenmpbackground = [];
var tenmpbackhalo = [];
var tenmpbackcontour = [];

function Heat_stack_layer_contour(){

var params = consume(); // 파라미터 가져온다.
console.log(params);
// var xdim = 1920;
// var ydim = 1080;
var xdim = 720;
var ydim = 576;

function createPath(w,h){
  var bc = document.createElement("canvas");
  bc.width = w;
  bc.height = h;
  bc.ctx = bc.getContext("2d");
  return bc;
}
function draw(q) {

  let dArr = [-1,-1, 0,-1, 1,-1, -1,0, 1,0, -1,1, 0,1, 1,1], // offset array
      s = 1,  // thickness scale
      i = 0,  // iterator
      x = 1,  // final position
      y = 1;
  
  // draw images at offsets from the array scaled by s
  var imageData = tenmpbackground[q].ctx.getImageData(0, 0, tenmpbackground[q].width, tenmpbackground[q].height);
  var pixels = imageData.data;
  for (let i = 3, n = pixels.length; i < n; i += 4) {
        pixels[i] = pixels[i] > 0? 255 : 0
    }
  // var tmpcvs=createPath(1920,1080);
  var tmpcvs=createPath(720,576);
  tmpcvs.ctx.putImageData(imageData,0,0);
  for(; i < dArr.length; i += 2)
    tenmpbackcontour[q].ctx.drawImage(tmpcvs, x + dArr[i]*s, y + dArr[i+1]*s);
  
  // fill with color
  tenmpbackcontour[q].ctx.globalCompositeOperation = "source-in";
  tenmpbackcontour[q].ctx.fillStyle = "black";
  tenmpbackcontour[q].ctx.fillRect(0,0,tmpcvs.width, tmpcvs.height);

  tenmpbackcontour[q].ctx.globalCompositeOperation = "destination-out";
  tenmpbackcontour[q].ctx.drawImage(tmpcvs, x, y);

  
  // draw original image in normal mode
  tenmpbackcontour[q].ctx.globalCompositeOperation = "source-over";
  tenmpbackcontour[q].ctx.drawImage(tenmpbackground[q], x, y);
  ctx.drawImage(tenmpbackcontour[q], x, y);

  

}



var config = {
  container: c,
  radius: params['Radius'],
  maxOpacity: params['Max_opacity'],
  minOpacity: params['Min_opacity'],
  blur: params['Blur'],
  gradient: heat_colors[params['Colors']]
  };
  // create heatmap with configuration
  

  // a single datapoint

// multiple datapoints (for data initialization use setData!!)

var timecountmax = draw_clusted_center.length;
var temp_heatcomp=[];

for(var q = 0; q<timecountmax; q++)
{
    HI_stack[q] = h337.create(config);
    var dataPoints = [];

    for(var l = 0; l<draw_clusted_data[q].length; l+=3)
    {
      var dataPoint = {
      x: Math.round(draw_clusted_data[q][l+1]*(c.width/xdim)), // x coordinate of the datapoint, a number
      y: Math.round(draw_clusted_data[q][l+2]*(c.height/ydim)), // y coordinate of the datapoint, a number
      val: 1 // the value at datapoint(x, y)
    };

      dataPoints.push(dataPoint);
    }

    var data={
      min:0,
      max:params['Global_max'],
      data:dataPoints
    }


      HI_stack[q].setData(data);


    var heatmap_canvas = $('.heatmap-canvas')[q];
    heatmap_canvas.ctx=heatmap_canvas.getContext("2d");
    temp_heatcomp.push(heatmap_canvas);

}


clear_canvas();
draw_image();
for(q=0;q<timecountmax;q++)
{
  draw_clusted_center[q][0]=draw_clusted_center[q][0]*(c.width/xdim);
  draw_clusted_center[q][1]=draw_clusted_center[q][1]*(c.height/ydim);

  for(var w=0; w<draw_clusted_data[q].length;w+=3)
  {  
      draw_clusted_data[q][w+1]=draw_clusted_data[q][w+1]*(c.width/xdim);
      draw_clusted_data[q][w+2]=draw_clusted_data[q][w+2]*(c.height/ydim);    
  }
  


  // tenmpbackground[q] = createPath(1920,1080);
  // tenmpbackhalo[q] = createPath(1920,1080);
  tenmpbackground[q] = createPath(720,576);
  tenmpbackhalo[q] = createPath(720,576);
  tenmpbackground[q].ctx.drawImage($('.heatmap-canvas')[q],0,0);

  // tenmpbackcontour[q] = createPath(1920,1080);
  tenmpbackcontour[q] = createPath(720,576);
  tenmpbackcontour[q].ctx.drawImage($('.heatmap-canvas')[q],0,0);

}

ctx.globalAlpha = params['Alpha'];


ctx.strokeStyle="rgba(0,0,0,0.5)";
ctx.lineWidth = 2;

ctx.globalAlpha = params['Max_opacity'];


ctx.strokeStyle="rgba(0,0,0,1.0)";

for(q=0;q<timecountmax-1;q++)
{

    smudgeAmount=params['Smudge_amount'];
    var background = tenmpbackground[q];
    
    draw(q);
    if(q==timecountmax-2)
      draw(q+1);
    
}
ctx.globalAlpha = params['Alpha'];
ctx.globalCompositeOperation = "source-over";

//ctx.drawImage(temp_heatcomp[timecountmax-1],0,0);      


          ctx.fillStyle = "rgba(255, 0, 0,1)";
          ctx.beginPath();
          ctx.ellipse(draw_clusted_center[0][0],draw_clusted_center[0][1], 5, 5, 0, 0, 2 * Math.PI);
          ctx.fill();

  brush.ctx.fillstyle = "rgba(255, 255, 255, 1)";
  brush.ctx.globalCompositeOperation = "source-over";
  brush.ctx.beginPath();
  brush.ctx.ellipse(brushSize/2, brushSize/2, 1, 1, 0, 0, 2 * Math.PI);
  brush.ctx.fill();
  

}


function Heat_stack_layer(){

var params = consume(); // 파라미터 가져온다.
console.log(params);
// var xdim = 1920;
// var ydim = 1080;
var xdim = 720;
var ydim = 576;




var config = {
  container: c,
  radius: params['Radius'],
  maxOpacity: params['Max_opacity'],
  minOpacity: params['Min_opacity'],
  blur: params['Blur'],
  gradient: heat_colors[params['Colors']]
  };
  // create heatmap with configuration
  

  // a single datapoint

// multiple datapoints (for data initialization use setData!!)

var timecountmax = draw_clusted_center.length;
var temp_heatcomp=[];

for(var q = 0; q<timecountmax; q++)
{
    HI_stack[q] = h337.create(config);
    var dataPoints = [];

    for(var l = 0; l<draw_clusted_data[q].length; l+=3)
    {
      var dataPoint = {
      x: Math.round(draw_clusted_data[q][l+1]*(c.width/xdim)), // x coordinate of the datapoint, a number
      y: Math.round(draw_clusted_data[q][l+2]*(c.height/ydim)), // y coordinate of the datapoint, a number
      val: 1 // the value at datapoint(x, y)
    };

      dataPoints.push(dataPoint);
    }

    var data={
      min:0,
      max:params['Global_max'],
      data:dataPoints
    }


      HI_stack[q].setData(data);


    var heatmap_canvas = $('.heatmap-canvas')[q];
    heatmap_canvas.ctx=heatmap_canvas.getContext("2d");
    temp_heatcomp.push(heatmap_canvas);

}


clear_canvas();
draw_image();
for(q=0;q<timecountmax;q++)
{
  draw_clusted_center[q][0]=draw_clusted_center[q][0]*(c.width/xdim);
  draw_clusted_center[q][1]=draw_clusted_center[q][1]*(c.height/ydim);

  for(var w=0; w<draw_clusted_data[q].length;w+=3)
  {  
      draw_clusted_data[q][w+1]=draw_clusted_data[q][w+1]*(c.width/xdim);
      draw_clusted_data[q][w+2]=draw_clusted_data[q][w+2]*(c.height/ydim);    
  }

}

ctx.globalAlpha = params['Alpha'];


ctx.strokeStyle="rgba(0,0,0,0.5)";
ctx.lineWidth = 2;

ctx.globalAlpha = params['Max_opacity'];


ctx.strokeStyle="rgba(0,0,0,1.0)";

for(q=0;q<timecountmax-1;q++)
{

    smudgeAmount=params['Smudge_amount'];
    var background = tenmpbackground[q];
    
    ctx.drawImage(temp_heatcomp[q],0,0);
    
    if(q==timecountmax-2)
      ctx.drawImage(temp_heatcomp[q+1],0,0);
    
}
ctx.globalAlpha = params['Alpha'];
ctx.globalCompositeOperation = "source-over";

//ctx.drawImage(temp_heatcomp[timecountmax-1],0,0);      


          ctx.fillStyle = "rgba(255, 0, 0,1)";
          ctx.beginPath();
          ctx.ellipse(draw_clusted_center[0][0],draw_clusted_center[0][1], 5, 5, 0, 0, 2 * Math.PI);
          ctx.fill();

  

}