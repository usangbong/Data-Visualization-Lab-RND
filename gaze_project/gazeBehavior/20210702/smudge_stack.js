var tenmpbackground = [];
var tenmpbackhalo = [];
var tenmpbackcontour = [];
function draw_heatmudge_stack(){
console.log("draw_heatmudge_stack");

var params = consume(); // 파라미터 가져온다.
console.log(params);
// var xdim = 1920;
// var ydim = 1080;
var xdim = 720;
var ydim = 576;

//var background = createBackground();
var brushSize = params['Brush_size'];
var bs = brushSize;
var bsh = bs / 2;
var smudgeAmount = params['Smudge_amount']; // values from 0 none to 1 full


var grad = ctx.createRadialGradient(bsh,bsh,0,bsh,bsh,bsh);
grad.addColorStop(0,"rgba(255,255,255,1)");
grad.addColorStop(1,"rgba(255,255,255,0.0)");

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

function brushFrom(ctx,x,y){
  brush.ctx.globalCompositeOperation = "source-over";
  brush.ctx.globalAlpha = smudgeAmount;
  brush.ctx.drawImage(ctx,-(x - bsh),-(y - bsh));
  //brush.ctx.fillRect(x,y,-(x - bsh),-(y - bsh));
  brush.ctx.globalCompositeOperation = "destination-in";
  brush.ctx.globalAlpha = smudgeAmount;
  brush.ctx.fillStyle = grad;
  brush.ctx.fillRect(0,0,bs,bs);
/*
  brush.ctx.beginPath();
  brush.ctx.arc(brushSize/2, brushSize/2, brushSize/2, 0, 2 * Math.PI);
  brush.ctx.fill();*/

  
}

function draw(q) {

  let dArr = [-1,-1, 0,-1, 1,-1, -1,0, 1,0, -1,1, 0,1, 1,1], // offset array
      s = 2,  // thickness scale
      i = 0,  // iterator
      x = 2,  // final position
      y = 2;
  
  // draw images at offsets from the array scaled by s
  for(; i < dArr.length; i += 2)
    tenmpbackcontour[q].ctx.drawImage(tenmpbackground[q], x + dArr[i]*s, y + dArr[i+1]*s);
  
  // fill with color
  tenmpbackcontour[q].ctx.globalCompositeOperation = "source-in";
  tenmpbackcontour[q].ctx.fillStyle = "black";
  tenmpbackcontour[q].ctx.fillRect(0,0,tenmpbackcontour[q].width, tenmpbackcontour[q].height);
  
  // draw original image in normal mode
  tenmpbackcontour[q].ctx.globalCompositeOperation = "source-over";
  tenmpbackcontour[q].ctx.drawImage(tenmpbackground[q], x, y);
  ctx.drawImage(tenmpbackcontour[q], 0, 0);

  

}



var config = {
  container: c,
  radius: params['Radius'],
  maxOpacity: 1,//params['Max_opacity'],
  minOpacity: 1,//params['Min_opacity'],
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


if(params['micro']==0)
{
  ctx.strokeStyle="rgba(0,0,0,1.0)";

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
}


for(q=0;q<timecountmax-1;q++)
{

    smudgeAmount=params['Smudge_amount'];
    var background = tenmpbackground[q];
        var dx = draw_clusted_center[q+1][0] - draw_clusted_center[q][0];
        var dy = draw_clusted_center[q+1][1] - draw_clusted_center[q][1];
        var dist = Math.sqrt(dx*dx+dy*dy);
        
        for(var j = 0;j < dist; j += 1){
          var ni = j / dist;
          brushFrom(background,draw_clusted_center[q][0] + dx * ni,draw_clusted_center[q][1] + dy * ni);
          ni = (j+1) / dist;
          
          tenmpbackground[q].ctx.drawImage(brush,draw_clusted_center[q][0] + dx * ni - bsh,draw_clusted_center[q][1] + dy * ni - bsh);
          tenmpbackhalo[q].ctx.drawImage(brush,draw_clusted_center[q][0] + dx * ni - bsh,draw_clusted_center[q][1] + dy * ni - bsh);
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
        
        brush.ctx.clearRect(0,0,bs,bs); /// clear brush if not used
        
    
    
    draw(q);
    if(q==timecountmax-2)
      draw(q+1);
    
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

if(params['micro']==1)
{
  ctx.strokeStyle="rgba(0,0,0,1.0)";

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

