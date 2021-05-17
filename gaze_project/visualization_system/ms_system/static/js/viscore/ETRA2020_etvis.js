var tenmpbackground = [];
var tenmpbackhalo = [];
var tenmpbackcontour = [];
function draw_etvis2020(){
  var params = consume(); // 파라미터 가져온다.
  var xdim = 1920;
  var ydim = 1080;
  var featureColors = ["#8da0cb", "#fc8d62", "#66c2a5"];

  var config = {
    container: c,
    minIdx: params['minIdx'],
    maxIdx: params['maxIdx'],
    maxFixationTime: params['maxFixationTime'],
    fixationRadius: params['fixationRadius'],
    fixationWidth: params['fixationWidth'],
    fixationTimeRadius: params['fixationTimeRadius'],
    fixationTimeWidth: params['fixationTimeWidth'],
    saccadeWidth: params['saccadeWidth'],
    saccadeGradient: params['saccadeGradient']
  };

  clear_canvas();
  draw_image();

  /*
  var fixationPoints = [];
  for(var l=0; l<draw_clusted_center.length; l++){
    var vsi = 0;
    var vsc = 0;
    var vso = 0;
    var vssmap = 0;
    var countPoint = 0;
    for(var m=0; m<draw_clusted_data[l].length; m+=3){
      var _xIdx = Math.round(draw_clusted_data[l][m+1]*(c.width/xdim));
      var _yIdx = Math.round(draw_clusted_data[l][m+2]*(c.height/ydim));
      vsi += vs_intensity_feature[_xIdx][_yIdx];
      vsc += vs_color_feature[_xIdx][_yIdx];
      vso += vs_orientation_feature[_xIdx][_yIdx];
      //vssmap += vs_saliency_feature[_xIdx][_yIdx];
      if(vssmap < vs_saliency_feature[_xIdx][_yIdx]){
        vssmap = vs_saliency_feature[_xIdx][_yIdx]
      }
      countPoint++;
    }
    vsi /= countPoint;
    vsc /= countPoint;
    vso /= countPoint;
    //vssmap /= countPoint;
    //console.log("point count: "+countPoint+", vs_i: "+vsi+", vs_c: "+vsc+", vs_o: "+vso);
    var fixationPoint = {
      x: Math.round(draw_clusted_center[l][0]*(c.width/xdim)),
      y: Math.round(draw_clusted_center[l][1]*(c.height/ydim)),
      vsi: vsi,
      vsc: vsc,
      vso: vso,
      vssmap: vssmap,
      num: countPoint
    };
    
    fixationPoints.push(fixationPoint);

  }

  var fixationLen = fixationPoints.length;

  var prev_x = 0;
  var prev_y = 0;
  var prev_maxVSfeature = 0;
  var firstFixationFlag = 0;
  for(q=0; q<fixationLen; q++){
    // get fixation point coordinate
    var _x = fixationPoints[q].x;
    var _y = fixationPoints[q].y;

    // get visual saliency features
    var vsRatioData = [0, 0, 0];
    var _vsi = fixationPoints[q].vsi;
    var _vsc = fixationPoints[q].vsc;
    var _vso = fixationPoints[q].vso;
    var _vssmap = fixationPoints[q].vssmap;
    console.log("q: "+q+", sm: "+_vssmap);

    var vs_total =  _vsi + _vsc + _vso;
    vsRatioData[0] = Math.round((_vsi/vs_total)*100);
    vsRatioData[1] = Math.round((_vsc/vs_total)*100);
    vsRatioData[2] = Math.round((_vso/vs_total)*100);
    if(vsRatioData[0]+vsRatioData[1]+vsRatioData[2] > 100){
      var _extra = 100 - (vsRatioData[0]+vsRatioData[1]+vsRatioData[2]);
      if(_extra %3 == 0){
        vsRatioData[0] += (_extra/3);
        vsRatioData[1] += (_extra/3);
        vsRatioData[2] += (_extra/3);
      }else{
        vsRatioData[0] += _extra;
      }

    }else if(vsRatioData[0]+vsRatioData[1]+vsRatioData[2] < 100){
      var _extra = (vsRatioData[0]+vsRatioData[1]+vsRatioData[2]) - 100;
      if(_extra %3 == 0){
        vsRatioData[0] -= (_extra/3);
       vsRatioData[1] -= (_extra/3);
        vsRatioData[2] -= (_extra/3);
      }else{
        vsRatioData[0] -= _extra;
      }
    }

    // get max visual saliency feature channel
    var _curMaxVSFeature = 0;
    var _biggerIdx = 0;
    var _biggerVal = 0;
    if(vsRatioData[0] > vsRatioData[1]){
      _biggerVal = vsRatioData[0];
      _biggerIdx = 0;
    }else{
      _biggerVal = vsRatioData[1];
      _biggerIdx = 1;
    }
    if(_biggerVal < vsRatioData[2]){
      _biggerVal = vsRatioData[2];
      _biggerIdx = 2;
    }
    _curMaxVSFeature = _biggerIdx;


    // filter for drawing fixation points
    // default values are 0, it means draw every fixation points.
    if(config.minIdx != 0 && config.maxIdx != 0){
      if (q < config.minIdx-1 || q > config.maxIdx){
        prev_x = _x;
        prev_y = _y;
        prev_maxVSfeature = _curMaxVSFeature;
        continue;
      }
    }
    
    if(firstFixationFlag==0){
      prev_x = _x;
      prev_y = _y;
      prev_maxVSfeature = _curMaxVSFeature;
    }else{
      // draw saccade
      var _grad = ctx.createLinearGradient(prev_x, prev_x, _x, _y);
      _grad.addColorStop(0, featureColors[prev_maxVSfeature]);
      _grad.addColorStop(1, featureColors[_curMaxVSFeature]);

      // darw link background (if saccade link color == gradient)
      if(config.saccadeGradient != 0){
        ctx.beginPath();
        ctx.strokeStyle = "black";
        ctx.lineWidth = config.saccadeWidth + 1;
        ctx.moveTo(prev_x, prev_y);
        ctx.lineTo(_x, _y);
        ctx.stroke();
        ctx.closePath();
      }

      ctx.beginPath();
      // set saccade link color
      // default value is 0. If config.saccadeGradient is not 0, saacade link color = gradient
      if(config.saccadeGradient == 0){
        ctx.strokeStyle = "black";
      }else{
        ctx.strokeStyle = _grad;
      }
      ctx.lineWidth = config.saccadeWidth;
      ctx.moveTo(prev_x, prev_y);
      ctx.lineTo(_x, _y);
      ctx.stroke();
      ctx.closePath();
    }
    
    // draw fixation: black background
    ctx.beginPath();
    ctx.fillStyle = "black";
    ctx.moveTo(_x, _y);
    ctx.arc(_x, _y, config.fixationRadius+config.fixationWidth, 0, 2*Math.PI);
    ctx.fill();
    ctx.closePath();

    // draw fixation: visual saliency chart
    var df = 0;
    for(var m=0; m<vsRatioData.length; m++){
      ctx.beginPath();
      ctx.fillStyle = featureColors[m];
      ctx.moveTo(_x, _y);
      ctx.arc(_x, _y, config.fixationRadius, df, df+((Math.PI*2)*(vsRatioData[m]/100)), false);
      ctx.lineTo(_x, _y)
      ctx.fill();
      df += (Math.PI*2)*(vsRatioData[m]/100);
    }
    ctx.closePath();

    // draw fixation: fixation duration background
    var fdRadius = config.fixationTimeRadius;
    var vsColorLevel = _vssmap * 255//rgbToHex(_vssmap * 255);
    vsColorLevel = Math.round(255-vsColorLevel);
    var saliencyLevelColor = rgbToHex(vsColorLevel, vsColorLevel, vsColorLevel)
    if(fdRadius<3){
      fdRadius = 3;
    }
    ctx.beginPath();
    ctx.fillStyle = "white";
    ctx.fillStyle = saliencyLevelColor;
    ctx.moveTo(_x, _y);
    ctx.arc(_x, _y, fdRadius, 0, 2*Math.PI);
    ctx.fill();
    ctx.closePath();

    // draw fixation: fixation duration chart
    _fdColor = ["#636363","white"];
    var _maxPointsInFixation = 12;
    if(config.maxFixationTime == 0){
      _maxPointsInFixation = 12;
    }else{
      _maxPointsInFixation = config.maxFixationTime;
    }
    
    gpointsInFixation = fixationPoints[q].num;
    //console.log("raw fixation duration: "+gpointsInFixation);
    if(gpointsInFixation > _maxPointsInFixation){
      gpointsInFixation = _maxPointsInFixation;
    }
    _fdData = [0, 100];
    _fdData[0] = Math.round((gpointsInFixation/_maxPointsInFixation)*100);
    _fdData[1] = 100-_fdData[0];
    //console.log(_fdData)
    var fdf = 0;
    var _fdGap = config.fixationTimeWidth;
    if(_fdGap > fdRadius-1){
      _fdGap = fdRadius-1;
    }
    for(var m=0; m<_fdData.length; m++){
      ctx.beginPath();
      ctx.fillStyle = _fdColor[m];
      ctx.moveTo(_x, _y);
      ctx.arc(_x, _y, fdRadius-_fdGap, fdf, fdf+((Math.PI*2)*(_fdData[m]/100)), false);
      ctx.lineTo(_x, _y)
      ctx.fill();
      fdf += (Math.PI*2)*(_fdData[m]/100);
    }
    ctx.closePath();

    // darw start point highlighting
    if(firstFixationFlag==0){
      ctx.beginPath();
      ctx.fillStyle = "#ef3b2c";
      ctx.moveTo(_x, _y);
      ctx.arc(_x, _y, _fdGap, 0, 2*Math.PI);
      ctx.fill();
      ctx.closePath();
    }
    

    prev_x = _x;
    prev_y = _y;
    firstFixationFlag = 1;
  }
  */

}

function rgbToHex(r, g, b) {
  return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}