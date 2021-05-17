var tenmpbackground = [];
var tenmpbackhalo = [];
var tenmpbackcontour = [];
function draw_ev2020(){

var params = consume(); // 파라미터 가져온다.
console.log(params);
var xdim = 1920;
var ydim = 1080;

//var background = createBackground();
var brushSize = params['Brush_size'];
var bs = brushSize;
var bsh = bs/2;
var smudgeAmount = params['Smudge_amount']; // values from 0 none to 1 full
var F=false;
var savedColor;
var grad = ctx.createRadialGradient(bsh,bsh,0,bsh,bsh,bsh);
grad.addColorStop(0,"rgba(255,255,255,1)");
grad.addColorStop(1,"rgba(255,255,255,0)");


var brush = createCanvas(brushSize)

function createCanvas(w,h = w){
  var bc = document.createElement("canvas");
  bc.width = w;
  bc.height = h;
  bc.ctx = bc.getContext("2d");
  return bc;
}
function createPath(w,h){
  var bc = document.createElement("canvas");
  bc.width = w;
  bc.height = h;
  bc.ctx = bc.getContext("2d");
  return bc;
}


function brushFrom(ctx,x,y,step){
  //step == x1,y1 => x2,y2 
  //if step > 0.65
  if(step<0.2)
  {
    smudgeAmount = 1;
  }else if(step<0.3){
    smudgeAmount = 0.8;
  }else if(step<0.4){
    smudgeAmount = 0.5;
  }
  else
  {
    smudgeAmount = params['Smudge_amount'];  
  }
  
  brush.ctx.globalCompositeOperation = "source-over";
  brush.ctx.globalAlpha = smudgeAmount;
  brush.ctx.drawImage(ctx,-(x - bsh),-(y - bsh));
  brush.ctx.globalCompositeOperation = "destination-in";
  brush.ctx.globalAlpha = smudgeAmount;
  brush.ctx.fillStyle = grad; 
  brush.ctx.fillRect(0,0,bs,bs);
  
  var bsp = brush.ctx.getImageData(bsh, bsh, 1, 1).data;
  if(bsp[3]==0)
  {
    F = true;
  } else if(bsp[0] != 0 && bsp[1] != 0 && bsp[2] != 0 && bsp[3] != 0){
    console.log(savedColor);
    savedColor = bsp;
  }
  
  /**
  if(F==true)
  {
    brush.ctx.fillStyle = "rgba(0,0,0,1)"; 
    brush.ctx.fillRect(0,0, bs, bs);
    //brush.ctx.arc(-(x - bsh),-(y - bsh), 10, 0, 2 * Math.PI);
    //brush.ctx.fill(); 
  }
**/
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
  var tmpcvs=createPath(1920,1080);
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
  ctx.drawImage(tenmpbackcontour[q], x*0.5, y*0.5);

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
  


  tenmpbackground[q] = createPath(1920,1080);
  tenmpbackhalo[q] = createPath(1920,1080);
  tenmpbackground[q].ctx.drawImage($('.heatmap-canvas')[q],0,0);

  tenmpbackcontour[q] = createPath(1920,1080);
  tenmpbackcontour[q].ctx.drawImage($('.heatmap-canvas')[q],0,0);

}

ctx.globalAlpha = params['Alpha'];


ctx.strokeStyle="rgba(0,0,0,0.5)";
ctx.lineWidth = 2;

ctx.globalAlpha = params['Max_opacity'];


ctx.strokeStyle="rgba(0,0,0,1.0)";
/*
for(q=0;q<timecountmax;q++)
{
ctx.beginPath();
        ctx.moveTo(draw_clusted_data[q][1], draw_clusted_data[q][2]);
        for(var w = 3; w<draw_clusted_data[q].length;w+=3)
        {
          ctx.lineTo(draw_clusted_data[q][w+1], draw_clusted_data[q][w+2]);  
        }
        ctx.stroke(); 
}
*/

for(q=0;q<timecountmax-1;q++)
{

    smudgeAmount=params['Smudge_amount'];
    var background = tenmpbackground[q];
    var dx = draw_clusted_center[q+1][0] - draw_clusted_center[q][0];
    var dy = draw_clusted_center[q+1][1] - draw_clusted_center[q][1];
    var dist = Math.sqrt(dx*dx+dy*dy);

    var _tx = 0;
    var _ty = 0;

    for(var j = 0; j < dist; j += 1)
    {
      var ni = j / dist;
      brushFrom(background, draw_clusted_center[q][0] + dx * ni, draw_clusted_center[q][1] + dy * ni, ni);
      ni = (j+1) / dist;
      
      tenmpbackground[q].ctx.drawImage(brush,draw_clusted_center[q][0] + dx * ni - bsh,draw_clusted_center[q][1] + dy * ni - bsh);
      tenmpbackhalo[q].ctx.drawImage(brush,draw_clusted_center[q][0] + dx * ni - bsh,draw_clusted_center[q][1] + dy * ni - bsh);

      _tx = draw_clusted_center[q][0] + dx * (j / dist);
      _ty = draw_clusted_center[q][1] + dy * (j / dist);
      if(F == true){    
          break;
      }
/*
      if(q ==11 && j%16==0)
      {

          var img    = createCanvas(500,100);
          img.ctx = img.getContext("2d");
          img.ctx.drawImage(tenmpbackhalo[q], 200, 400, 500, 100, 0, 0, 500, 100);

          var img_src = img.toDataURL("image/png");

          $( "body" ).append( '<img src="'+img_src+'"/>' );
      }
      */
    }
    
    tenmpbackground[q].ctx.beginPath();
    tenmpbackground[q].ctx.moveTo(_tx, _ty);
    tenmpbackground[q].ctx.lineTo(draw_clusted_center[q+1][0], draw_clusted_center[q+1][1]);
    tenmpbackground[q].ctx.lineWidth = 6;
    //tenmpbackground[q].ctx.strokeStyle = "rgba(0, 0, 0, 0.7)";
    //console.log(savedColor);
    tenmpbackground[q].ctx.strokeStyle = "rgba("+savedColor[0]+","+savedColor[1]+","+savedColor[2]+", 0.5)";
    tenmpbackground[q].ctx.stroke();

    brush.ctx.clearRect(0,0,bs,bs); /// clear brush if not used

    
    draw(q);
    if(q==timecountmax-2)
      draw(q+1);
    
    F=false;
}



ctx.globalAlpha = params['Alpha'];
ctx.globalCompositeOperation = "source-over";

//ctx.drawImage(temp_heatcomp[timecountmax-1],0,0);      

function calcAngleDegrees(x, y) {
  return Math.atan2(y, x)+(90* (Math.PI/180));
}

for(q=0;q<timecountmax;q++)
{
  ctx.drawImage(tenmpbackhalo[q],0,0);
        if(q<timecountmax-1)
        {
          var dx = draw_clusted_center[q+1][0] - draw_clusted_center[q][0];
        var dy = draw_clusted_center[q+1][1] - draw_clusted_center[q][1];
        var dist = Math.sqrt(dx*dx+dy*dy);
        console.log();
        var xgrid = Math.cos(calcAngleDegrees(dx,dy));
        var ygrid = Math.sin(calcAngleDegrees(dx,dy));
        var strength = bsh;

        
      ctx.strokeStyle="rgba(255,255,255,1)";
        ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(draw_clusted_center[q][0], draw_clusted_center[q][1]);/*
        for(var j = 0;j < dist; j += 15){
          var ni = j / dist;
          var ni2 = (j+15) / dist;
          
          var tmp_str_val = Math.floor((draw_clusted_std[q]*(1-ni)+draw_clusted_std[q+1]*ni)*strength);
          

          ctx.bezierCurveTo(draw_clusted_center[q][0] + dx * ni+xgrid*tmp_str_val, draw_clusted_center[q][1] + dy * ni+ygrid*tmp_str_val,draw_clusted_center[q][0] + dx * ni2+xgrid*tmp_str_val, draw_clusted_center[q][1] + dy * ni2+ygrid*tmp_str_val, draw_clusted_center[q][0] + dx * ni2, draw_clusted_center[q][1] + dy * ni2);
          
          
          
          strength*=-1;
          }       */
          ctx.lineTo(draw_clusted_center[q+1][0], draw_clusted_center[q+1][1]);
        ctx.stroke();
        }   
}


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

