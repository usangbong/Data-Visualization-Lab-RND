function draw_heatmudge(){

var params = consume(); // 파라미터 가져온다.

// var xdim = 1920;
// var ydim = 1080;
var xdim = 720;
var ydim = 576;

const background = createBackground();
var brushSize = params['Brush_size'];
const bs = brushSize;
const bsh = bs / 2;
var smudgeAmount = params['Smudge_amount']; // values from 0 none to 1 full

var dataPoints = [];


// brush gradient for feather
var grad = ctx.createRadialGradient(bsh,bsh,0,bsh,bsh,bsh);
grad.addColorStop(0,"rgba(255,255,255,1)");
grad.addColorStop(1,"rgba(0,0,0,0)");
var brush = createCanvas(brushSize)

// creates an offscreen canvas
function createCanvas(w,h = w){
  var bc = document.createElement("canvas");
  bc.width = w;
  bc.height = h;
  bc.ctx = bc.getContext("2d");
  return bc;
}

// get the brush from source ctx at x,y
function brushFrom(ctx,x,y){
  brush.ctx.globalCompositeOperation = "source-over";
  brush.ctx.globalAlpha = smudgeAmount;
  brush.ctx.drawImage(ctx,-(x - bsh),-(y - bsh));
  brush.ctx.globalCompositeOperation = "destination-in";
  brush.ctx.globalAlpha = smudgeAmount;
  brush.ctx.fillStyle = grad;
  //brush.ctx.fillRect(0,0,bs,bs);
  brush.ctx.beginPath();
  brush.ctx.arc(brushSize/2, brushSize/2, brushSize/2, 0, 2 * Math.PI);
  brush.ctx.fill();
}
  
// short cut vars 
var w = c.width;
var h = c.height;
var cw = w / 2;  // center 
var ch = h / 2;
var globalTime;
var lastX;
var lastY;

// update background is size changed
function createBackground(){
    
    var tempheat=$('.heatmap-canvas')[0];
    tempheat.ctx = tempheat.getContext("2d");
    return tempheat;
}


for(var l = 0; l<draw_data.length; l++)
{
  var dataPoint = {
  x: Math.round(draw_data[l]['x']*(c.width/xdim)),
  y: Math.round(draw_data[l]['y']*(c.height/ydim))
};

  dataPoints.push(dataPoint);
}

console.log(draw_data);

for(var i = 0; i<draw_data.length-1;i++)
{
  //ctx.drawImage(background,0,0);

    var dx = dataPoints[i+1]['x'] - dataPoints[i]['x'];
    var dy = dataPoints[i+1]['y'] - dataPoints[i]['y'];
    var dist = Math.sqrt(dx*dx+dy*dy);
    for(var j = 0;j < dist; j += 1){
      var ni = j / dist;
      brushFrom(background,dataPoints[i]['x'] + dx * ni,dataPoints[i]['y'] + dy * ni);
      ni = (j+1) / dist;
      background.ctx.drawImage(brush,dataPoints[i]['x'] + dx * ni - bsh,dataPoints[i]['y'] + dy * ni - bsh);
    }
    console.log(i/draw_data.length);
    brush.ctx.clearRect(0,0,bs,bs); /// clear brush if not used
}
  

clear_canvas();
draw_image();
ctx.globalAlpha = params['Alpha'];
ctx.drawImage(background,0,0)
}


