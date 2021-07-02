function clear_canvas(){
  ctx.clearRect(0, 0, c.width, c.height);
}

function draw_image(){
  var s = "image_"+$('#imageselector option:selected').val();
  console.log(s);
  var img = document.getElementById(s);

    if(img.width>img.height)
    {
      var temp = mxvis/img.width;
      img.width*=temp;
      img.height*=temp;
    }
    else
    {
     var temp = myvis/img.height;
     img.width*=temp;
     img.height*=temp;
    }

    c.width=img.width;
    c.height=img.height;

    if(sb_back == true)
      ctx.drawImage(img, 0, 0, c.width, c.height);

    /* 해상도 이슈 발생시  pica를 사용함. node.js 컴파일후 추가해둠. 4장의 사진은 문제 없어보임.
    pica.resize(img, c, {
      quality:3,
      unsharpAmount: 0,
      unsharpRadius: 0,
      unsharpThreshold: 0
    });
    */
}

function draw_vis(s){

  clear_canvas();//clear canvas -> 필요시 이미지 투명도 변수가 필요할 수도 있음 -> draw_image 함수에서 tint를 설정하던가 레이어를 분기할것.
  draw_image();

  switch(s){
    case "Scan-path":
      Scan_path();
      console.log("Vis for Scan-path");
    break;

    case "Point-based":
      Point_based();
      console.log("Vis for Point-based");
    break;

    case "Heatmap":
      Heatmap();
      console.log("Vis for Heatmap");
    break;

    case "Heat-flow":
      Heat_flow();
      console.log("Vis for Heat-flow");
    break;

    case "Heat-stack":
      Heat_stack();
      console.log("Vis for Heat-stack");
    break;

    case "Heat-stack-none-etc":
      Heat_stack_etc();
      console.log("Vis for Heat-stack");
    break;

    case "Heat-stack-none-saccade":
      Heat_stack_saccade();
      console.log("Vis for Heat-stack-none-saccade");
    break;

    case "Heat-layer":
      Heat_layer();
      console.log("Vis for Heat-layer");
    break;

    case "Heat-layer-contour":
      Heat_layer_contour();
      console.log("Vis for Heat-layer-contour");
    break;

    case "EV2020":
      Vis_EV2020();
      console.log("Vis for EV2020");
    break;

    case "ETRA2020-ETVIS":
      Vis_ETRA2020_ETVIS();
      console.log("Vis for ETRA2020-ETVIS");
    break;

    case "Euro2020-Short":
      Vis_EuroVis2020_Short();
      console.log("Vis for EuroVis2020-Short");
    break;


    default:
    console.log("Out of range ~ ~ :> ");

  }

}

//Canvas 는 하나를 공유하고 setup -> draw 단계의 태스크 프레임형식을 사용하기 때문에 문제가 없음.
//함수내에서 canvas = c , 2DContext = ctx 를 사용해 시각화 작업을 수행한다.
//시각화 작업에서 필요한 연산들은 자바스크립트의 경우 다른 home.html에서 다른 js파일을 추가하는것으로 대체한다.  위치는 js/viscore/.
//파이썬연산은 jquery의 ajax로 비동기식으로 처리함.
//!!!!!!!! consume.js에 파라미터 목록에 있는 input tag들을 id와 value 쌍으로 흡입하고 오브젝트단위로 리턴합니다.!!!!!!!!!
// checkbox 의 경우 컨슘이 안될수도 있으니 확인이 필요함.


function Scan_path(){
    // var xdim = 1920;
    // var ydim = 1080;
    var xdim = 720;
    var ydim = 576;

    var params = consume();
    var count=0;
    for (var k in params) {
         if(params[k]==0)
          count++;
    }

   var config = {
      container: c,
      dbscanEpsilon: params['DBSCAN_epsilon'],
      dbscanMinPts: params['DBSCAN_min_points'],
      dbscanCluSize: params['DBSCAN_cluster_size'],
      dbscanTimeWeight: params['DBSCAN_time_weight'],
      fixSizeWeight: params['Fixation_size_weight'],
      linkWidth: params['Link_width'],
      fixColor: params['Fixation_color'],
      fixOuterlineColor: params['Fixation_outer-line_color'],
      linkColor: params['Link_color'],
      linkHaloColor: params['Link_halo_color'],
      opacity: params['Alpha'],
  };
  DBSCAN_CONFIG['ep']=params['DBSCAN_epsilon'];
  DBSCAN_CONFIG['mp']=params['DBSCAN_min_points'];
  DBSCAN_CONFIG['cs']=params['DBSCAN_cluster_size'];
  DBSCAN_CONFIG['tw']=params['DBSCAN_time_weight'];

  var dataPoints = [];
  console.log("draw_clusted_center.length")
  console.log(draw_clusted_center.length)
  console.log("draw_clusted_center")
  console.log(draw_clusted_center)
  

  //draw_clusted_center[0][0] = 896.9737;
  //draw_clusted_center[0][1] = 285.3354;
  //draw_clusted_center[1][0] = 897.6041;
  //draw_clusted_center[1][1] = 281.7395;
  //draw_clusted_center[2][0] = 890.2901;
  //draw_clusted_center[2][1] = 284.5290;
  //draw_clusted_center[3][0] = 902.2745;
  //draw_clusted_center[3][1] = 277.1244;
  //draw_clusted_center[4][0] = 893.8851;
  //draw_clusted_center[4][1] = 275.4944;
  //draw_clusted_center[5][0] = 1279.6923;
  //draw_clusted_center[5][1] = 497.1541;
  //draw_clusted_center[6][0] = 907.6964;
  //draw_clusted_center[6][1] = 647.9094;

  for(var l=0; l<draw_clusted_center.length; l++){
    //console.log(draw_clusted_center[l][0])
      var dataPoint = {
        x: Math.round(draw_clusted_center[l][0]*(c.width/xdim)),
        y: Math.round(draw_clusted_center[l][1]*(c.height/ydim))
    };
    
    dataPoints.push(dataPoint);
  }
  

  //console.log(dataPoints)
  // draw link between fixations
  ctx.beginPath();
  for(var l=0; l<dataPoints.length-1; l++){
      ctx.strokeStyle = "black";
      ctx.width = 4;
      ctx.moveTo(dataPoints[l].x, dataPoints[l].y);
      ctx.lineTo(dataPoints[l+1].x, dataPoints[l+1].y);
  }
  ctx.stroke();
  ctx.closePath();

  ctx.beginPath();
  for(var l=0; l<dataPoints.length-1; l++){
      ctx.strokeStyle = "red";
      ctx.width = 3;
      ctx.moveTo(dataPoints[l].x, dataPoints[l].y);
      ctx.lineTo(dataPoints[l+1].x, dataPoints[l+1].y);
  }
  ctx.stroke();
  ctx.closePath();

  // draw fixation points
  ctx.beginPath();
  for(var l=0; l<dataPoints.length; l++){
      ctx.fillStyle = "black";
      ctx.moveTo(dataPoints[l].x, dataPoints[l].y);
      ctx.arc(dataPoints[l].x, dataPoints[l].y, 10, 0, 2*Math.PI, true);
  }
  ctx.fill();
  ctx.closePath();

  // draw fixation points
  ctx.beginPath();
  for(var l=0; l<dataPoints.length; l++){
      ctx.fillStyle = "red";
      ctx.moveTo(dataPoints[l].x, dataPoints[l].y);
      ctx.arc(dataPoints[l].x, dataPoints[l].y, 9, 0, 2*Math.PI, true);
  }
  ctx.fill();
  ctx.closePath();

}

function Point_based(){
    // var xdim = 1920;
    // var ydim = 1080;
    var xdim = 720;
    var ydim = 576;

    var params = consume();

    var count=0;
    for (var k in params) {
         if(params[k]==0)
          count++;
    }

   var config = {
      container: c,
      radius: params['Radius'],
      outerLineWidth: params['Outer_line_width'],
      pointColor: params['Point_color'],
      outerLineColor: params['Outer_line_color'],
      linkWidth: params['link_width'],
      linkColor: params['link_color'],
      //opacity: params['Alpha'],
      linkDrawableFlag: params['Saccade_flag']
   };

    var dataPoints = [];
    for(var l = 0; l<draw_data.length; l++)
    {
      var dataPoint = {
      x: Math.round(draw_data[l]['x']*(c.width/xdim)), // x coordinate of the datapoint, a number
      y: Math.round(draw_data[l]['y']*(c.height/ydim)), // y coordinate of the datapoint, a number
      value: 5 // the value at datapoint(x, y)
    };
      dataPoints.push(dataPoint);
    }

    if(config.linkDrawableFlag == 1){
        ctx.beginPath();
        for(var i=0; i<dataPoints.length-1; i++){
            ctx.strokeStyle = "black";
            ctx.width = config.linkWidth+1;
            ctx.moveTo(dataPoints[i].x, dataPoints[i].y);
            ctx.lineTo(dataPoints[i+1].x, dataPoints[i+1].y);
        }
        ctx.stroke();
        ctx.closePath();

        ctx.beginPath();
        for(var i=0; i<dataPoints.length-1; i++){
            ctx.strokeStyle = "black";
            ctx.width = config.linkWidth;
            ctx.moveTo(dataPoints[i].x, dataPoints[i].y);
            ctx.lineTo(dataPoints[i+1].x, dataPoints[i+1].y);
        }
        ctx.stroke();
        ctx.closePath();
    }

    ctx.beginPath();
    for(var i=0; i<dataPoints.length; i++){
        ctx.fillStyle = "black";
        ctx.moveTo(dataPoints[i].x, dataPoints[i].y);
        ctx.arc(dataPoints[i].x, dataPoints[i].y, config.radius, 0, 2*Math.PI, true);
    }
    ctx.fill();
    ctx.closePath();

    ctx.beginPath();
    for(var i=0; i<dataPoints.length; i++){
        ctx.fillStyle = "red";
        ctx.moveTo(dataPoints[i].x, dataPoints[i].y);
        ctx.arc(dataPoints[i].x, dataPoints[i].y, config.radius-config.outerLineWidth, 0, 2*Math.PI, true);
    }
    ctx.fill();
    ctx.closePath();



}

function Heatmap(){
  // 중간 생산자 방지를 위해 삭제
  // var xdim = 1920;
  // var ydim = 1080;
  var xdim = 720;
  var ydim = 576;
  if($( ".heatmap-canvas" ).length>0)

      $( ".heatmap-canvas" ).remove();


  var params = consume(); // 파라미터 가져온다.

  var count=0;
  for (var k in params) {
       if(params[k]==0)
        count++;
  }


  console.log(count);
  if(count==5)
    return;


var config = {
  container: c,
  radius: params['Radius'],
  maxOpacity: params['Max_opacity'],
  minOpacity: params['Min_opacity'],
  blur: params['Blur'],
  opacity: params['Opacity'],
  gradient: heat_colors[params['Colors']]
  };
  // create heatmap with configuration
  heatmapInstance = h337.create(config);

  // a single datapoint

// multiple datapoints (for data initialization use setData!!)
var dataPoints = [];
console.log(draw_clusted_data)
for(var l = 0; l<draw_clusted_data.length; l++){
  for(var ll = 0; ll<draw_clusted_data[l].length; ll+=3){
    var dataPoint = {
      x: Math.round(draw_clusted_data[l][ll+1]*(c.width/xdim)), // x coordinate of the datapoint, a number
      y: Math.round(draw_clusted_data[l][ll+2]*(c.height/ydim)), // y coordinate of the datapoint, a number
    val: 1 // the value at datapoint(x, y)
    };
  }
  dataPoints.push(dataPoint);
}

//for(var l = 0; l<draw_data.length; l++)
//{
//  var dataPoint = {
//  x: Math.round(draw_data[l]['x']*(c.width/xdim)), // x coordinate of the datapoint, a number
//  y: Math.round(draw_data[l]['y']*(c.height/ydim)), // y coordinate of the datapoint, a number
//  val: 1 // the value at datapoint(x, y)
//};
//  dataPoints.push(dataPoint);
//}

var data={
  min:0,
  max:params['Global_max'],
  data:dataPoints
}


  heatmapInstance.setData(data);
console.log(dataPoints);

var heatmap_canvas = $('.heatmap-canvas')[0];

ctx.drawImage(heatmap_canvas,0,0);



}

function Heat_flow(){
  draw_heatmudge();
}

function Heat_stack(){
  draw_heatmudge_stack();
}

function Heat_stack_etc(){
  draw_heatmudge_stack_etc();
}

function Heat_stack_saccade(){
  draw_heatmudge_stack_saccade();
}

function Heat_layer(){
  Heat_stack_layer();
}

function Heat_layer_contour(){
  Heat_stack_layer_contour();
}

function Vis_EV2020(){
  draw_ev2020();
}

function Vis_ETRA2020_ETVIS(){
  draw_etvis2020();
}

function Vis_EuroVis2020_Short(){
  draw_short_eurovis2020();
}

function canvas_image_down(cvs)
{
var imageData = cvs.toDataURL();
var tmpLink = document.createElement( 'a' );
tmpLink.download = 'image.png'; // set the name of the download file
tmpLink.href = imageData;
document.body.appendChild( tmpLink );
tmpLink.click();
document.body.removeChild( tmpLink );

}
