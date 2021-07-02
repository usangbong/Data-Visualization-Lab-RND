function draw_ETRA_ET4S(){
  var params = consume(); // get parameters
  // var xdim = 1024;
  // var ydim = 768;
  var xdim = 720;
  var ydim = 576;

  var config = {
    container: c,
    fixationRadius: params['fixationRadius'],
    dFixationRadius: params['dFixationRadius'],
    saccadeWidth: params['saccadeWidth'],
    imageAlpha: params['imageAlpha'],
    unselectedAlpha: params['unselectedAlpha'],
    selectedDViewAlpha: params['selectedDViewAlpha'],
    unselectedDViewAlpha: params['unselectedDViewAlpha'],
    fixLogType: params['fixLogType'],
  };
  
  clear_canvas();
  globalAlpha = config.imageAlpha;
  draw_image(globalAlpha);

  // interface: features information
  var _en_interface_height = 25;
  drawFeaturesInformations(c_fi, featureModelTexts, features_color, scanpathPixelEncodingSelect, _en_interface_height);
  
  analysis_clusted_data = [];
  for(var i=0; i<draw_clusted_center.length; i++){
    var _prev_x = 0;
    var _prev_y = 0;
    var _prev_ams = [0,0,0];
    var sequence_data = [];
    var sumLength = 0;
    for(var j=0; j<draw_clusted_center[i].length; j++){
      var _x = draw_clusted_center[i][j].x;
      var _y = draw_clusted_center[i][j].y;
      var _ams = [draw_clusted_center[i][j].am1, draw_clusted_center[i][j].am2, draw_clusted_center[i][j].am3];
      
      if(j==0){
        _prev_x = _x;
        _prev_y = _y;
        _prev_ams =_ams;
        continue;
      }
      var _l = getDistance(_prev_x, _prev_y, _x, _y);
      var _part = {
        x: _prev_x,
        y: _prev_y,
        l: _l,
        text: "data_"+i,
        am1: _prev_ams[0],
        am2: _prev_ams[1],
        am3: _prev_ams[2]
      }
      sequence_data.push(_part);
      sumLength+=_l;

      if(j == draw_clusted_center[i].length-1){
          var _part = {
          x: _x,
          y: _y,
          l: sumLength,
          text: "data_"+i,
          am1: _ams[0],
          am2: _ams[1],
          am3: _ams[2]
        }
        sequence_data.push(_part);
      }
      _prev_x = _x;
      _prev_y = _y;
      _prev_ams =_ams;
    }
    analysis_clusted_data.push(sequence_data);
  }

  radarChart_left = makeRadarChart(c_cl, featureModelTexts, features_color, 3);
  radarChart_right = makeRadarChart(c_cr, weightModelTexts, weightModels_color, 1);

  drawRadarChart(c_cl, radarChart_left, "Saliency features");
  drawRadarChart(c_cr, radarChart_right, "Score weight models");

  drawRadarInterface(c_cl);


  drawScaleInterface(c_icy, interface_BG_left_scale, "left");
  drawScaleInterface(c_icx, interface_BG_right_scale, "right");
  drawFittingBarGraph(c_b, 10, "_fitResData", interface_BG_left_scale, interface_BG_right_scale);


  gConfig_dfixation_radius = config.dFixationRadius;
  gConfig_duration_type = config.fixLogType;
  drawScanpathPixelView(c_d, fixationSaccade, orderedScanpathsIdx, gConfig_dfixation_radius, gConfig_duration_type);


  // draw a scanpath on the visual stimulus
  gConfig_gFixationRadius = config.fixationRadius;
  gConfig_gSaccadeWidth = config.saccadeWidth;
  drawScanpathOnStimulus(c, xdim, ydim, gConfig_gFixationRadius, gConfig_gSaccadeWidth);
}

function rgbToHex(r, g, b) {
  return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

function getDistance(sx, sy, ex, ey){
  var dis = 0;
  var _dis_x = ex-sx;
  var _dis_y = ey-sy;

  dis = Math.sqrt(Math.abs(_dis_x*_dis_x)+Math.abs(_dis_y*_dis_y));
  return dis;
}

function drawFixation(_context, _x, _y, _r, _c, _ga){
  _context.beginPath();
  _context.globalAlpha = _ga;
  _context.fillStyle = _c;
  _context.moveTo(_x, _y);
  _context.arc(_x, _y, _r, 0, 2*Math.PI);
  _context.fill();
  _context.closePath();
}

function drawRectFixation(_context, _x, _y, _m, _w, _h, _slw, _sc, _fc, _ga){
  _context.beginPath();
  _context.globalAlpha = _ga;
  if(_slw != 0){
    _context.lineWidth = _slw;
    _context.strokeStyle = _sc;
  }
  _context.fillStyle = _fc;
  if(_w == _h){
    _context.rect(_x-_m/2, _y-_m/2, _w, _h);
  }else{
    _context.rect(_x, _y-_m/2, _w, _h);
  }
  
  if(_slw != 0){
    _context.stroke();
  }
  _context.fill();
  _context.globalAlpha = 1.0;
}

function drawRectButton(_context, _x, _y, _m, _w, _h, _slw, _sc, _fc, _ga){
  _context.beginPath();
  _context.globalAlpha = _ga;
  if(_slw != 0){
    _context.lineWidth = _slw;
    _context.strokeStyle = _sc;
  }
  _context.fillStyle = _fc;
  if(_w == _h){
    _context.rect(_x-_m/2, _y-_m/2, _w, _h);
  }else{
    _context.rect(_x, _y-_m/2, _w, _h);
  }
  
  if(_slw != 0){
    _context.stroke();
  }
  _context.fill();
  _context.globalAlpha = 1.0;
}


function drawSaccade(_context, _sx, _sy, _ex, _ey, _w, _c, _ga){
  _context.beginPath();
  _context.globalAlpha = _ga;
  _context.strokeStyle = _c;
  _context.lineWidth = _w;
  _context.moveTo(_sx, _sy);
  _context.lineTo(_ex, _ey);
  _context.stroke();
  _context.closePath();
  _context.lineWidth = 1.0;
}

function drawDottedLiine(_context, _sx, _sy, _ex, _ey, _w, _c){
  _context.beginPath();
  _context.strokeStyle = _c;
  _context.lineWidth = _w;
  _context.setLineDash([1,1]);
  _context.moveTo(_sx, _sy);
  _context.lineTo(_ex, _ey);
  _context.stroke();
  _context.closePath();
  _context.setLineDash([]);
  _context.lineWidth = 1.0;
}

function roundRect(_context, x, y, w, h, radius, lw, c) {
  var r = x+w;
  var b = y+h;
  radius = 0;

  _context.beginPath();
  _context.strokeStyle = c;
  _context.lineWidth = lw;
  _context.moveTo(x+radius, y);
  _context.lineTo(r-radius, y);
  _context.quadraticCurveTo(r, y, r, y+radius);
  _context.lineTo(r, y+h-radius);
  _context.quadraticCurveTo(r, b, r-radius, b);
  _context.lineTo(x+radius, b);
  _context.quadraticCurveTo(x, b, x, b-radius);
  _context.lineTo(x, y+radius);
  _context.quadraticCurveTo(x, y, x+radius, y);
  _context.stroke();
  _context.lineWidth = 1.0;
}

function roundRectFill(_context, x, y, w, h, radius, lw, lc, fc, ga) {
  var r = x+w;
  var b = y+h;
  radius = 0;

  _context.beginPath();
  _context.globalAlpha = ga;
  _context.fillStyle = fc;
  _context.strokeStyle = lc
  _context.lineWidth = lw;
  _context.moveTo(x+radius, y);
  _context.lineTo(r-radius, y);
  _context.quadraticCurveTo(r, y, r, y+radius);
  _context.lineTo(r, y+h-radius);
  _context.quadraticCurveTo(r, b, r-radius, b);
  _context.lineTo(x+radius, b);
  _context.quadraticCurveTo(x, b, x, b-radius);
  _context.lineTo(x, y+radius);
  _context.quadraticCurveTo(x, y, x+radius, y);
  _context.stroke();
  _context.fill();
  _context.lineWidth = 1.0;
}

function drawText(_context, _center_x, _center_y, _c, _align, _size, _text){
  _context.lineWidth = 1.0;
  _context.font = _size+"px Arial";
  _context.fillStyle = _c;
  _context.textAlign = _align; // center
  _context.fillText(_text, _center_x,_center_y);
}

function drawRectFrame(_context, x, y, w, h, lw, _sc, _ga){
  _context.beginPath();
  _context.globalAlpha = _ga;
  _context.lineWidth = lw;
  _context.strokeStyle = _sc;
  _context.rect(x, y, w, h);
  _context.stroke();
  _context.globalAlpha = 1.0;
}

function drawFilledRect(_context, x, y, w, h, _fc, _ga){
  _context.beginPath();
  _context.globalAlpha = _ga;
  _context.fillStyle = _fc;
  _context.rect(x, y, w, h);
  _context.fill();
  _context.globalAlpha = 1.0;
}

function makeRadarChart(_c, _models, _colors, _initVal){
  var _context = _c.getContext("2d");

  var _radar = [];
  var _cx = _c.width/2;
  var _cy = _c.height/2;
  var _stepLen = 3*(_c.height/4)/10;
  var _radius = _stepLen*5;
  var _points = [];

  var _start_x = _cx;
  var _start_y = _cy+_radius;

  for(var i=0; i<_models.length; i++){
    var _angle = (360/_models.length)*i-90;
    var _rad = degreesToRadians(_angle);

    var _x = _cx+Math.cos(_rad)*_radius;
    var _y = _cy+Math.sin(_rad)*_radius;

    var _steps = [];
    for(var j=0; j<=5; j++){
      var _angle = (360/_models.length)*i-90;
      var _rad = degreesToRadians(_angle);
      var _r = _stepLen*j;

      var _stepx = _cx+Math.cos(_rad)*_r;
      var _stepy = _cy+Math.sin(_rad)*_r;
      var _sp = {
        sx:parseFloat(_stepx.toFixed(10)),
        sy:parseFloat(_stepy.toFixed(10))
      }
      _steps.push(_sp);
    }

    var point = {
      c_x: _cx,
      c_y: _cy,
      stepLen: _stepLen,
      radius: _radius,
      x: _x,
      y: _y,
      radians: _rad,
      color: _colors[i],
      steps: _steps,
      val: _initVal
    };
    _radar.push(point);
  }
  return _radar;
}

function degreesToRadians(degrees){
  const pi = Math.PI;
  if(degrees < 0){
    degrees+=360;
  }
  return degrees*(pi/180);
}

function drawRadarChart(_canvas, _radarChart, _title){
  var _context = _canvas.getContext("2d");
  // draw frame
  if(_radarChart.length !=- 0){
    var cx = _radarChart[0].c_x;
    var cy = _radarChart[0].c_y;
    for(var i=0; i<_radarChart.length; i++){
      var curx = _radarChart[i].x;
      var cury = _radarChart[i].y;
      _context.beginPath();
      _context.lineWidth = 1;
      _context.strokeStyle = _radarChart[i].color;
      _context.moveTo(cx, cy);
      _context.lineTo(curx, cury);
      _context.closePath();
      _context.stroke();

      for(var j=1; j<_radarChart[i].steps.length; j++){
        var _stepx = _radarChart[i].steps[j].sx;
        var _stepy = _radarChart[i].steps[j].sy;

        _context.beginPath();
        _context.fillStyle = "#525252";
        _context.moveTo(_stepx, _stepy);
        _context.arc(_stepx, _stepy, 2, 0, 2*Math.PI);
        _context.closePath();
        _context.fill();
      }
    }

    var curValuePoints = [];
    // draw radar
    for(var i=0; i<_radarChart.length; i++){
      var _cx = _radarChart[i].c_x;
      var _cy = _radarChart[i].c_y;
      var _pos = getRadarSelectedPos(i, _cx, _cy, _radarChart.length, _radarChart[i].stepLen, _radarChart[i].val);
      
      curValuePoints.push([_pos.x, _pos.y]);
    }

    _context.beginPath();
    _context.globalAlpha = 0.5;
    _context.fillStyle = "gray";
    for(var i=0; i<curValuePoints.length; i++){
      if(i==0){
        _context.moveTo(curValuePoints[i][0], curValuePoints[i][1]);
      }else{
        _context.lineTo(curValuePoints[i][0], curValuePoints[i][1]);
      }
    }
    _context.closePath();
    _context.fill();

    _context.globalAlpha = 0.7;
    for(var i=0; i<curValuePoints.length; i++){
      _context.beginPath();
      _context.fillStyle = _radarChart[i].color;
      _context.arc(curValuePoints[i][0], curValuePoints[i][1], 5, 0, 2*Math.PI);
      _context.closePath();
      _context.fill();
    }
    _context.globalAlpha = 1.0;

    for(var i=0; i<curValuePoints.length; i++){
      _context.beginPath();
      _context.strokeStyle = "black";
      _context.arc(curValuePoints[i][0], curValuePoints[i][1], 5, 0, 2*Math.PI);
      _context.closePath();
      _context.stroke();
    }


    // draw text
    for(var i=0; i<_radarChart.length; i++){
      var _cx = _radarChart[i].c_x;
      var _cy = _radarChart[i].c_y;
      var _pos = getRadarSelectedPos(i, _cx, _cy, _radarChart.length, _radarChart[i].stepLen, _radarChart[i].val);
      
      var _px = _pos.x;
      var _py = _pos.y;

      var tx = _px;
      var ty = _py;
      var tgap = 20;
      var tlen = 15;
      if(_px > _cx){
        tx += tgap;
        ty += tgap;
      }else if(_px == _cx){
        tx += (tgap+(tlen/2));
      }else{
        tx -= (tgap+tlen);
        ty += tgap;
      }
      var _weightedVal = _radarChart[i].val;
      if(_title == "Saliency features"){
        _weightedVal = getFeatureThreshold(i);

      }
      drawText(_context, tx, ty, blackTone_4d, "center", 15, _weightedVal.toFixed(2));
    }
  }
  var _font = 15;
  drawText(_context, _canvas.width/2, _canvas.height-_font, blackTone_4d, "center", _font, _title);
}

function drawRadarInterface(_canvas){
  _context = _canvas.getContext("2d");


}

function getRadarSelectedPos(_index, _cx, _cy, _num, _steplen, _val){
  var _angle = (360/_num)*_index-90;
  var _rad = degreesToRadians(_angle);
  var _r = _steplen*(_val/2);

  var _px = _cx+Math.cos(_rad)*_r;
  var _py = _cy+Math.sin(_rad)*_r;

  var _p = {
    x: parseFloat(_px.toFixed(10)),
    y: parseFloat(_py.toFixed(10))
  };

  return _p;
}

function getRotatedPos(_x, _y, _r, _rad){
  var _rx = _x+Math.cos(_rad)*_r;
  var _ry = _y+Math.sin(_rad)*_r;

  var _rPos = {
    x: parseFloat(_rx.toFixed(10)),
    y: parseFloat(_ry.toFixed(10))
  };
  
  return _rPos;
}

function drawFittingBarGraph(_canvas, _div, _fitResData, _interfaceLeft, _interfaceRight){
  var _context = _canvas.getContext("2d");
  var _canvasWidth = _canvas.width;
  var _canvasHeight = _canvas.height;

  var _divStandard_x = 10;
  var _divStandard_y = 25;

  var _cx = _canvasWidth/_divStandard_x;
  var _cy = (_divStandard_y-3)*_canvasHeight/_divStandard_y;

  var xAxis = {
    sx: _cx,
    sy: _cy,
    ex: (_divStandard_x-1)*_canvasWidth/_divStandard_x,
    ey: _cy
  };
  var yAxis = {
    sx: _cx,
    sy: _cy,
    ex: _cx,
    ey: 3*_canvasHeight/_divStandard_y
  };

  var _graphWidth = xAxis.ex - xAxis.sx;
  var _graphHeight = yAxis.ey - yAxis.sy;
  var _whRatio = _graphWidth/_graphHeight;
  var x_step = _graphWidth/_div;
  var y_step = _graphHeight/_div;
  // draw x-axis
  drawArrowLine(_context, 0, xAxis.sx, xAxis.sy, xAxis.ex+(x_step/2), xAxis.ey, 1, blackTone_4d, 1);
  // draw y-axis
  drawArrowLine(_context, 270, yAxis.sx, yAxis.sy, yAxis.ex, yAxis.ey+y_step, 1, blackTone_4d, 1);
  
  var halfLenStep = 4;
  var textGap = 15;
  var _h_lines = [];
  var _v_lines = [];
  for(var i=0; i<_div; i++){
    // draw x-axis steps
    drawSimpleLine(_context, xAxis.sx+x_step*(i+1), xAxis.sy-halfLenStep, xAxis.sx+x_step*(i+1), xAxis.sy+halfLenStep, 1, blackTone_4d, 1);
    if(i==0){
      drawText(_context, xAxis.sx-textGap, xAxis.sy+textGap, blackTone_4d, "center", 10, "0");
    }
    drawText(_context, xAxis.sx+x_step*(i+1), xAxis.sy+textGap, blackTone_4d, "center", 10, (i+1)*10);
    // draw y-axis steps
    drawSimpleLine(_context, yAxis.sx-halfLenStep, yAxis.sy+y_step*(i+1), yAxis.sx+halfLenStep, yAxis.sy+y_step*(i+1), 1, blackTone_4d, 1);
    drawText(_context, yAxis.sx-textGap, yAxis.sy+y_step*(i+1)+(textGap/3), blackTone_4d, "center", 10, (i+1)*10);
    
    // init & push vertical lines
    var _v = {
      sx: xAxis.sx+x_step*(i+1),
      sy: xAxis.sy,
      ex: xAxis.sx+x_step*(i+1),
      ey: -999
    };
    _v_lines.push(_v);
    // init & push horizontal lines
    var _h = {
      sx: yAxis.sx,
      sy: yAxis.sy+y_step*(i+1),
      ex: -999,
      ey: yAxis.sy+y_step*(i+1)
    };
    _h_lines.push(_h);
    // change temp ex and ey coordinate (-999) to calculated values
    if(i==_div-1){
      var _end_y = yAxis.sy+y_step*(i+1);
      var _end_x = xAxis.sx+x_step*(i+1);

      for(var j=0; j<_v_lines.length; j++){
        _v_lines[j].ey = _end_y;
      }
      for(var j=0; j<_h_lines.length; j++){
        _h_lines[j].ex = _end_x;
      }
    }
  }

  // draw vertical and horizontal lines for easy recognition
  for(var i=0; i<_v_lines.length; i++){
    drawSimpleLine(_context, _v_lines[i].sx, _v_lines[i].sy, _v_lines[i].ex, _v_lines[i].ey-10, 1, blackTone_87, 1);
  }

  for(var i=0; i<_h_lines.length; i++){
    drawSimpleLine(_context, _h_lines[i].sx, _h_lines[i].sy, _h_lines[i].ex+10, _h_lines[i].ey, 1, blackTone_87, 1);
  }

  // calculate fitting score
  // temp!!!!
  fittingScoreData = [];
  fittingScoreData.push(10);
  fittingScoreData.push(20);
  fittingScoreData.push(30);
  fittingScoreData.push(40);
  fittingScoreData.push(50);
  fittingScoreData.push(60);
  fittingScoreData.push(60);
  fittingScoreData.push(50);
  fittingScoreData.push(40);
  fittingScoreData.push(30);

  // draw bar graph
  var _weight = 0.1;
  for(var i=0; i<fittingScoreData.length; i++){
    var _w = x_step;
    var _h = (fittingScoreData[i]*_weight)*y_step;
    var _x = xAxis.sx+x_step*i;
    var _y = xAxis.ey;
    
    drawFilledRect(_context, _x, _y, _w, _h, blackTone_4d, 0.7);
  }

}

function drawArrowLine(_context, baseAngle, sx, sy, ex, ey, w, c, arrowSize){
  var _angle = [baseAngle+90+45, baseAngle+360-(90+45)];
  var _rad = [degreesToRadians(_angle[0]), degreesToRadians(_angle[1])];
  var _arrowHeadPos = [getRotatedPos(ex, ey, arrowSize, _rad[0]), getRotatedPos(ex, ey, arrowSize, _rad[1])];

  _context.beginPath();
  _context.strokeStyle = c;
  _context.fillStyle = c;
  _context.lineWidth = w;
  _context.moveTo(sx, sy);
  _context.lineTo(ex, ey);
  _context.lineTo(_arrowHeadPos[0].x, _arrowHeadPos[0].y);
  _context.arcTo(ex, ey, _arrowHeadPos[1].x, _arrowHeadPos[1].y, 10);
  _context.lineTo(ex, ey);
  _context.closePath();
  _context.stroke();
  _context.fill();
}

function drawSimpleLine(_context, _sx, _sy, _ex, _ey, _w, _c, _ga){
  _context.beginPath();
  _context.globalAlpha = _ga;
  _context.strokeStyle = _c;
  _context.lineWidth = _w;
  _context.moveTo(_sx, _sy);
  _context.lineTo(_ex, _ey);
  _context.stroke();
  _context.closePath();
}

function drawSimpleFillCircle(_context, _x, _y, _r, _c, _ga){
  _context.beginPath();
  _context.globalAlpha = _ga;
  _context.fillStyle = _c;
  _context.arc(_x, _y, _r, 0, 2*Math.PI);
  _context.closePath();
  _context.fill();
  _context.globalAlpha = 1.0;
}

function drawSimpleStrokeCircle(_context, _x, _y, _r, _lw, _c, _ga){
  _context.beginPath();
  _context.globalAlpha = _ga;
  _context.lineWidth = _lw;
  _context.strokeStyle = _c;
  _context.arc(_x, _y, _r, 0, 2*Math.PI);
  _context.closePath();
  _context.stroke();
  _context.globalAlpha = 1.0;
}

function drawScaleInterface(_canvas, _interface, _LorR){
  var _context = _canvas.getContext("2d");
  var _sx = _canvas.width/5;
  var _sy = _canvas.height/2; 
  var _ex = 4*_canvas.width/5;
  var _ey = _canvas.height/2;
  var _min = _interface.min;
  var _max = _interface.max;
  var _div = _interface.div;
  var _val = _interface.curVal;
  _sx += 30;
  _ex += 30;
  var _title = "NULL";
  if(_LorR == "left"){
    _title = "y-axis"
  }else{
    _title = "x-axis"
  }
  
  var _f = 15;
  var _tgap = _f*3;
  drawText(_context, _sx-_tgap, (_canvas.height/4)+(_f/2), blackTone_4d, "center", 15, _title);
  drawText(_context, _sx-_tgap, (2*_canvas.height/4)+(_f/2), blackTone_4d, "center", 15, "scale");
  drawText(_context, _sx-_tgap, (3*_canvas.height/4)+(_f/2), blackTone_4d, "center", 15, "interface");


  drawSimpleLine(_context, _sx, _sy, _ex, _ey, 1, blackTone_4d, 1);
  var _step = (_ex-_sx)/(_div-1);
  if(_interface.stepLen == -999){
    _interface.stepLen = _step;
  }
  var _valStep = (_max-_min)/_div;

  // draw steps
  var halfLenStep = 5;
  for(var i=0; i<_div; i++){
    var _x = _sx+_step*i;
    var _y = _sy;
    drawSimpleLine(_context, _x, _y-halfLenStep, _x, _y+halfLenStep, 1, blackTone_4d, 1);
    drawText(_context, _x, _y+(halfLenStep*3), blackTone_4d, "center", 10, (i+1)*_interface.scale);
  }

  // draw val indicator
  var _vi_max = _interface.max;
  var _vi_min = _interface.min;
  var _curVal = _interface.curVal;
  var _vi_x = ((_ex-_sx)*(_curVal-1))/(_vi_max-_vi_min);
  var _vi_y = _sy;
  var _vi_r = 6;
  drawSimpleFillCircle(_context, _sx+_vi_x, _vi_y, _vi_r, "red", 0.5);
  drawSimpleStrokeCircle(_context, _sx+_vi_x, _vi_y, _vi_r, 1,"black", 0.5);

}

function drawFeaturesInformations(_canvas, _featureTexts, _featureColors, _encodings, _encodingHeight){
  var _context = _canvas.getContext("2d");

  // draw frame
  drawRectFrame(_context, 0, 0, _canvas.width, _canvas.height-_encodingHeight, 2, blackTone_00, 1);

  // draw icon & text
  var _lrMargin = 10;
  var _oneSpaceWidth = (_canvas.width-_lrMargin*2)/_featureTexts.length;
  var _oneIconWidth = _oneSpaceWidth/5;
  var _oneTextWidth = 3*_oneSpaceWidth/5;
  var _oneGapWidth = _oneSpaceWidth/5;
  var _y = (_canvas.height-_encodingHeight)/2;
  var _h = (_canvas.height-_encodingHeight)/3;
  var _fontSize = _h+5;

  for(var i=0; i<_featureTexts.length; i++){
    var _x = _lrMargin+_oneIconWidth*(i)+_oneTextWidth*(i)+_oneGapWidth*(i);
    drawFilledRect(_context, _x, _y-(_h/2), _oneIconWidth, _h, _featureColors[i], 1);
    var _tx = _x+(_oneIconWidth*2);
    if(_featureTexts[i] == "Orientation"){
      _tx = _x+(_oneIconWidth*2.5);
    }else if(_featureTexts[i] == "Log spectrum"){
      _tx = _x+(_oneIconWidth*2.5);
    }
    
    drawText(_context, _tx, _y+(_fontSize/3), blackTone_4d, "center", _fontSize, _featureTexts[i]);
  }

  drawEncodingSelectInterface(_canvas, _encodings, 4, _canvas.height-_encodingHeight);
}

function drawEncodingSelectInterface(_canvas, _encodings, _topMargin, _infoHeight){
  var _context = _canvas.getContext("2d");

  var _cWidth = _canvas.width;
  var _cHeight = (_canvas.height-_infoHeight-_topMargin);
  var _margin = 5;
  var _gap = 5;

  var _oneBoxWidth = (_cWidth-_margin*2-_gap*(_encodings.length-1))/_encodings.length;
  var _oneBoxHeight = _cHeight-2;

  var _sum = 0;
  for(var i=0; i<_encodings.length; i++){
    _sum += _encodings[i];
  }

  for(var i=0; i<_encodings.length; i++){
    var _x = _margin + (_oneBoxWidth+_gap)*i;
    var _y = _infoHeight + _topMargin+ _oneBoxHeight/2 -1;
    var _sc = blackTone_4d;
    var _fc = "white";
    var _lw = 1;
    if(_sum == 0){
      _encodings[0] = 1;
    }

    if(_encodings[i] == 1){
      _sc = blackTone_00;
      _fc = blackTone_ba;
      _lw = 2;
    }

    drawRectButton(_context, _x, _y, _oneBoxHeight, _oneBoxWidth, _oneBoxHeight, _lw, _sc, _fc, 1);
    
    var _eText = "";
    if(i==0){
      _eText = "Saccade length || Fixation duration";
    }else if(i==1){
      _eText = "Saccade length";
    }else if(i==2){
      _eText = "Fixation duration";
    }else{
      _eText = "Fixation duration && Saccade length";
    }
    var _fSize = 12;
    drawText(_context, _x+(_oneBoxWidth/2), _y+(_fSize/3), blackTone_25, "center", _fSize, _eText);
  }
}


function getDistance(x1, y1, x2, y2){
  var dis = 0;
  var difx = x2-x1;
  var dify = y2-y1;
  dis = Math.sqrt(difx*difx+dify*dify);
  return dis;
}

function drawScanpathPixelView(_canvas, _fxData, _orderedIndexes, _fixRad, _spDurationType){
  var _context = _canvas.getContext("2d");

  // draw scanpath-pixel-view
  var _spvHeight = _canvas.height;
  var _oneSetHeight = _spvHeight/_fxData.length;
  var _oneGapHeight = _oneSetHeight/10;
  var _oneBoxHeight = 9*_oneSetHeight/10;
  var _w = _canvas.width;

  var _totalFixWidth = _w/25;
  var _scanpathsWidth = 24*_w/25;
  var _scanpathsHeight = 2*_oneBoxHeight/3;
  var _durationBarHeight = _oneBoxHeight/3;

  if(selectedUserDataIdx != -999){
    var _bx = 0;
    var _by = _oneSetHeight*selectedUserDataIdx;
    drawRectFrame(_context, _bx, _by, _w, _oneBoxHeight, 1, blackTone_00, 1);
  }

  // data order array init
  _orderedIndexes = [];
  for(var i=0; i<_fxData.length; i++){
    _orderedIndexes.push(i);
  }

  // init saccades length
  saccadesLength = [];
  var _allMaxLength = 0;
  for(var i=0; i<_fxData.length; i++){
    var _prev_x = 0;
    var _prev_y = 0;
    var _sumLen = 0;
    var _lens = [];
    var _count = 0;
    for(var j=0; j<_fxData[i].length; j++){
      var _x = _fxData[i][j].x;
      var _y = _fxData[i][j].y;
      if(j==0){
        _prev_x = _x;
        _prev_y = _y;
        continue;
      }
      var _dis = getDistance(_prev_x, _prev_y, _x, _y);
      _lens.push(_dis);
      _sumLen += _dis;

      _prev_x = _x;
      _prev_y = _y;
      _count+=1;
    }
    var _t = {
      sumLen: _sumLen,
      lens: _lens
    };
    saccadesLength.push(_t);

    // get max length from all data
    if(_allMaxLength < _sumLen){
      _allMaxLength = _sumLen;
    }
  }
  orderedScanpathsIdx = _orderedIndexes;

  scanpathsPixelData = [];
  var _dataNum = featureModelTexts.length;
  var _oneScanpathBoxHeight = (_scanpathsHeight-2)/_dataNum;
  var _oneScanpathHeight = 9*_oneScanpathBoxHeight/10;
  var _gapBetweenScanpaths = (_oneScanpathBoxHeight/10)/_dataNum;
  var _lenRatio = _scanpathsWidth/_allMaxLength;

  var _oneScanpathBoxWithoutDurationHeight = _oneBoxHeight/_dataNum;
  var _oneScanpathWithoutDurationHeight = (_dataNum-1)*_oneScanpathBoxWithoutDurationHeight/_dataNum;
  var _gapBetweenScanpathsWithoutDuration = _oneScanpathBoxWithoutDurationHeight/_dataNum;
  for(var i=0; i<_fxData.length; i++){
    var _scanpaths = [];
    for(var k=0; k<_dataNum; k++){
      var _scanpath = [];
      var _y = _oneSetHeight*i+(_oneScanpathHeight+_gapBetweenScanpaths)*k;
      var _y2 = _oneSetHeight*i + (_oneScanpathWithoutDurationHeight+_gapBetweenScanpathsWithoutDuration)*k;
      var _spd_p_x = _totalFixWidth+(_totalFixWidth/3);
      for(var j=0; j<saccadesLength[i].lens.length; j++){
        // set color
        var _featureThreshold = getFeatureThreshold(k);

        var _c = blackTone_87;
        
        if(features_values[i][j][k] > _featureThreshold){
          _c = features_color[k];
        }

        if(j==0){
          var _p = {
            x: _spd_p_x,
            y: (_fixRad)*2 + _y,
            y2: (_fixRad)*2 + _y2,
            c: _c
          };
          _scanpath.push(_p);
          continue;
        }

        var _x = _spd_p_x + saccadesLength[i].lens[j-1]*_lenRatio;        
        var _p = {
          x: _x,
          y: (_fixRad)*2+ _y,
          y2: (_fixRad)*2 + _y2,
          c: _c
        };

        _scanpath.push(_p);

        _spd_p_x = _x;
        if(j==saccadesLength[i].lens.length-1){
          var _x = _spd_p_x + saccadesLength[i].lens[j]*_lenRatio;
          var _p = {
            x: _x,
            y: (_fixRad)*2+ _y,
            y2: (_fixRad)*2 + _y2,
            c: _c
          };
          _scanpath.push(_p);
        }
      }
      _scanpaths.push(_scanpath);
    }
    scanpathsPixelData.push(_scanpaths);
  }

  var user_id_font = 10;
  // draw user id text
  for(var i=0; i<_orderedIndexes.length; i++){
    var _order = _orderedIndexes[i];

    var _x = _totalFixWidth/2;
    var _y = user_id_font/4+scanpathsPixelData[i][0][0].y;

    drawText(_context, _x, _y, blackTone_4d, "center", user_id_font, "data_"+_order);
  }

  // temp setting
  // ordering
  // ordering
  // ordering
  // ordering

  // draw total fixation duration
  var leftmargin=5;
  var tDurationChart_h = _oneBoxHeight-(user_id_font*2)-5;
  var tDurationChart_x = leftmargin;
  var tDurationChart_w = _totalFixWidth-(leftmargin*2)-1;
  for(var i=0; i<_orderedIndexes.length; i++){
    var _order = _orderedIndexes[i];
    var tDurationChart_y = user_id_font+scanpathsPixelData[i][0][0].y;
    var userDuration = stimulusSummaryData[_order][2];
    var _udRatio = userDuration/maxPointsInUsr;
    var _ufill_h = tDurationChart_h*_udRatio;
    var _ufill_y = tDurationChart_y + (tDurationChart_h-_ufill_h);
    drawFilledRect(_context, tDurationChart_x, _ufill_y, tDurationChart_w, _ufill_h, blackTone_87, 1);
    drawRectFrame(_context, tDurationChart_x, tDurationChart_y, tDurationChart_w, tDurationChart_h, 1, blackTone_87, 1);
    
    for(var m=0; m<11; m++){
      var dly = tDurationChart_y+(tDurationChart_h/10)*m;
      drawDottedLiine(_context, tDurationChart_x, dly, tDurationChart_x+tDurationChart_w, dly, 1, blackTone_ba);
    }
  }


  // draw ordered scanpath-pixel-vis
  var _eSel = scanpathPixelEncodingSelect;
  if(_eSel[0] == 1 && _eSel[1] == 0 && _eSel[2] == 0 && _eSel[3] == 0){
    // scanpath type: encoding only saccade length
    encodingSaccadeLengthScanpathPixel(_canvas, _orderedIndexes, scanpathsPixelData, _fixRad, _fixRad, 1.0, 1.0, user_id_font, _spDurationType);
  }else if(_eSel[0] == 0 && _eSel[1] == 1 && _eSel[2] == 0 && _eSel[3] == 0){
    // scanpath type: encoding only saccade length + without duration graph
    encodingOnlyScanpathPixel(_canvas, _orderedIndexes, scanpathsPixelData, _fixRad, 1.0, 1.0);
  }else if((_eSel[0] == 0 && _eSel[1] == 0 && _eSel[2] == 1 && _eSel[3] == 0)){
    // scanpath type: encoding only fixation duration
    encodingFixationDurationScanpathPixel(_canvas, _orderedIndexes, scanpathsPixelData, stimulusSummaryData, _fixRad, 1.0, 1.0);
  }else if((_eSel[0] == 0 && _eSel[1] == 0 && _eSel[2] == 0 && _eSel[3] == 1)){
    // scanpath type: encoding saccade length with fixation duration
    encodingFDwithSLScanpathPixel(_canvas, _orderedIndexes, scanpathsPixelData, stimulusSummaryData, saccadesLength, _fixRad, 1.0, 1.0);
  }
}

function encodingSaccadeLengthScanpathPixel(_canvas, _oIdxs, _spData, _w, _h, _slw, _ga, _fontSize, _spDurationType){
  var _context = _canvas.getContext("2d");

  // draw ordered scanpaths type: encoding only saccade length
  for(var i=0; i<_oIdxs.length; i++){
    var _order = _oIdxs[i];
    for(var j=0; j<_spData[_order].length; j++){
      var _prev_x = 0;
      var _prev_y = 0;
      for(var k=0; k<_spData[_order][j].length-1; k++){
        var _x = _spData[_order][j][k].x;
        var _y = _spData[_order][j][k].y;
        //console.log(_x+", "+_y);
        
        if(k==0){
          _prev_x = _x;
          _prev_y = _y;
          continue;
        }

        drawSaccade(_context, _prev_x, _prev_y, _x, _y, 1, blackTone_4d, 1);
        _prev_x = _x;
        _prev_y = _y;
      } 

      for(var k=0; k<_spData[_order][j].length-1; k++){
        var _x = _spData[_order][j][k].x;
        var _y = _spData[_order][j][k].y;
        var _c = _spData[_order][j][k].c;

        drawRectFixation(_context, _x, _y, _w, _w, _h, _slw, blackTone_87, _c, _ga);
      }
    }
  }

  var _canvasWidth = _canvas.width;
  var _totalFixWidth = _canvasWidth/25;
  var _spvHeight = _canvas.height;
  var _oneSetHeight = _spvHeight/_oIdxs.length;
  var _oneGapHeight = _oneSetHeight/10;
  var _oneBoxHeight = 9*_oneSetHeight/10;
  var _durationBarHeight = _oneBoxHeight/3;

  // draw fixation duration
  for(var i=0; i<_oIdxs.length; i++){
    var _order = _oIdxs[i];
    var chart_x = _totalFixWidth+(_totalFixWidth/3);
    var chart_y = (_oneBoxHeight)*(i+1)+ _oneGapHeight*i - _durationBarHeight;
    var chart_w = 23*_canvasWidth/25;
    var chart_h = _durationBarHeight-5;
    var chart_lw = 1;
    var chart_sc = blackTone_4d;
    var chart_ga = 1;
    var fixCount = stimulusSummaryData[_order][3].length;
    var boxWidth = chart_w/fixCount;

    for(var m=0; m<stimulusSummaryData[_order][3].length; m++){
      var bw = boxWidth;
      var bx = chart_x+bw*m;
      var by = chart_y;
      var bh = chart_h;
      var blw = 1;
      var bsc = blackTone_87;
      var bga = chart_ga;
      var pCountInFix = stimulusSummaryData[i][3][m];
      var _mPinF = maxPointsInFix;
      if(_spDurationType == 1){
        _mPinF = stimulusSummaryData[i][1];
      }
      var pRatio = pCountInFix/_mPinF;
      var fill_h = bh*pRatio;
      var fill_y = by + (bh - fill_h);
      drawFilledRect(_context, bx, fill_y, bw, fill_h, bsc, bga);
      drawRectFrame(_context, bx, by, bw, bh, blw, bsc, bga);

    }

    for(var m=0; m<11; m++){
      var dly = chart_y+(chart_h/10)*m;
      drawDottedLiine(_context, chart_x, dly, chart_x+chart_w, dly, 1, blackTone_ba);
    }
  }

}

function encodingOnlyScanpathPixel(_canvas, _oIdxs, _spData, _h, _slw, _ga){
  var _context = _canvas.getContext("2d");

  // draw ordered scanpaths type: encoding only saccade length
  for(var i=0; i<_oIdxs.length; i++){
    var _order = _oIdxs[i];
    for(var j=0; j<_spData[_order].length; j++){
      var _prev_x = 0;
      var _prev_y = 0;
      for(var k=0; k<_spData[_order][j].length-1; k++){
        var _x = _spData[_order][j][k].x;
        var _y = _spData[_order][j][k].y2;
        
        if(k==0){
          _prev_x = _x;
          _prev_y = _y;
          continue;
        }

        drawSaccade(_context, _prev_x, _prev_y, _x, _y, 1, blackTone_4d, 1);
        _prev_x = _x;
        _prev_y = _y;
      } 

      for(var k=0; k<_spData[_order][j].length-1; k++){
        var _x = _spData[_order][j][k].x;
        var _y = _spData[_order][j][k].y2;
        var _c = _spData[_order][j][k].c;

        // adding fixation color select function
        drawRectFixation(_context, _x, _y, _h, _h, _h, _slw, blackTone_87, _c, _ga);
      }
    }
  }
}

function encodingFixationDurationScanpathPixel(_canvas, _oIdxs, _spData, _durationData, _h, _slw, _ga, _spDurationType){
  var _context = _canvas.getContext("2d");

  // scanpath type: encoding only fixation duration
  for(var i=0; i<_oIdxs.length; i++){
    var _order = _oIdxs[i];
    // draw saccade
    for(var j=0; j<_spData[_order].length; j++){
      var _saccadeWidth = 5;
      var _rdRatio = ((20*_canvas.width)/25)/(maxPointsInUsr+_saccadeWidth*(_durationData[_order][3].length-1));
      var _sumWidth = 0;
      for(var k=0; k<_spData[_order][j].length; k++){
        var _x = (_canvas.width/25)+_sumWidth;
        var _y = _spData[_order][j][k].y2;
        if(k != 0){
          drawSaccade(_context, _x, _y, _x+_saccadeWidth, _y, 1, blackTone_4d, _ga);
          _sumWidth+=_saccadeWidth;
        }

        var _pointsInFix = _durationData[_order][3][k];
        if(_spDurationType == 1){
          _rdRatio = ((20*_canvas.width)/25)/(_durationData[_order][2]+_saccadeWidth*(_durationData[_order][3].length-1));
        }
        var _w = _pointsInFix*_rdRatio;
        _sumWidth+=_w;
      }

      // draw fixation with duration
      _sumWidth = 0;
      for(var k=0; k<_spData[_order][j].length; k++){
        //var _x = _spData[_order][j][k].x;
        var _x = (_canvas.width/25)+_sumWidth;
        var _y = _spData[_order][j][k].y2;
        var _c = _spData[_order][j][k].c;
        var _pointsInFix = _durationData[_order][3][k];
        //var _mPinF = maxPointsInFix;
        if(_spDurationType == 1){
          _rdRatio = ((20*_canvas.width)/25)/(_durationData[_order][2]+_saccadeWidth*(_durationData[_order][3].length-1));
        }
        //var pRatio = pCountInFix/_mPinF;
        var _w = _durationData[_order][3][k]*_rdRatio;
        var _m = _h;

        // adding fixation color select function
        drawRectFixation(_context, _x, _y, _m, _w, _h, _slw, blackTone_87, _c, _ga);
        _sumWidth+=(_w+_saccadeWidth);
      }
    }
  }
}

//encodingSaccadeLengthScanpathPixel(_canvas, _oIdxs, _spData, _w, _h, _slw, _ga, _fontSize, _spDurationType){
function encodingFDwithSLScanpathPixel(_canvas, _oIdxs, _spData, _durationData, _sLenData, _h, _slw, _ga, _spDurationType){
  var _context = _canvas.getContext("2d");
  
  // calculate max length values
  var _maxSumLen = 0;
  var _maxLenInUser = [];
  for(var i=0; i<_sLenData.length; i++){
    var _max = _sLenData[i].sumLen;
    if(_maxSumLen < _max){
      _maxSumLen = _max;
    }

    var _m = 0;
    for(var j=0; j<_sLenData[i].lens.length; j++){
      var _v = _sLenData[i].lens[j];
      if(_m < _v){
        _m = _v;
      }
    }
    _maxLenInUser.push(_m);
  }

  // calculate ratios
  var _eachLengthSums = [];
  var _maxSum = 0;
  for(var i=0; i< _sLenData.length; i++){
    var _mSumLen = _sLenData[i].sumLen;
    var _mSumDur = _durationData[i][2];
    var _sumLenDur = _mSumLen + _mSumDur;

    _eachLengthSums.push(_sumLenDur);

    if(_maxSum < _sumLenDur){
      _maxSum = _sumLenDur;
    }
  }

  // draw
  for(var i=0; i<_oIdxs.length; i++){
    var _order = _oIdxs[i];
    // draw saccade
    for(var j=0; j<_spData[_order].length; j++){
      var _rdRatio = (23*_canvas.width/25)/_maxSum;
      var _sumWidth = 0;
      for(var k=0; k<_spData[_order][j].length; k++){
        if(_spDurationType == 1){
          _rdRatio = (23*_canvas.width/25)/_eachLengthSums[_order];
        }
        var _pointsInFix = _durationData[_order][3][k];
        var _w = _pointsInFix*_rdRatio;
        _sumWidth+=_w;

        var _x = (_canvas.width/25)+_sumWidth;
        var _y = _spData[_order][j][k].y2;        
        var _saccadeWidth = _sLenData[_order].lens[k]*_rdRatio;

        
        drawSaccade(_context, _x, _y, _x+_saccadeWidth, _y, 1, blackTone_4d, _ga);
        _sumWidth+=_saccadeWidth;
        
      }

      
      // draw fixation with duration
      _sumWidth = 0;
      for(var k=0; k<_spData[_order][j].length; k++){
        var _x = (_canvas.width/25)+_sumWidth;
        var _y = _spData[_order][j][k].y2;
        var _c = _spData[_order][j][k].c;
        var _pointsInFix = _durationData[_order][3][k];
        if(_spDurationType == 1){
          _rdRatio = (23*_canvas.width/25)/_eachLengthSums[_order];
        }
        var _saccadeWidth = _sLenData[_order].lens[k]*_rdRatio;
        var _w = _pointsInFix*_rdRatio;
        var _m = _h;

        drawRectFixation(_context, _x, _y, _m, _w, _h, _slw, blackTone_87, _c, _ga);
        _sumWidth+=(_w+_saccadeWidth);
      }
    }
  }
}


function calcScore(_canvas){
  //fittingScoreData


  for(var i=0; i<features_in_fix.length; i++){
    var _sti = features_in_fix[i][0]; 
    var _x = features_in_fix[i][1];
    var _y = features_in_fix[i][2];
    var _overThreshold = [];
    for(var j=0; j<features_in_fix[i][3].length; j++){
      var _fs = features_in_fix[i][3][j];
      var _vals = [];
      if(_fs[j] > getFeatureThreshold[k]){
        _vals.push(1);
      }else{
        _vals.push(0);
      }
    }
    _overThreshold.push(_vals);
    var _duration = stimulusSummaryData[selectedUserDataIdx][3][i];
    var _move = 0;
    if(i!=0){
      _move = saccadesLength[selectedUserDataIdx].lens[i];
    }

    var _d = {
      x: _x,
      y: _y,
      v: _overThreshold,
      d: _duration,
      m: _move,
      s: 0
    };
    fittingScoreData.push(_d);
  }

  



}


function getFeatureThreshold(_index){
  return radarChart_left[_index].val * features_weights[_index];
}

function drawScanpathOnStimulus(_canvas, _xdim, _ydim, _fixRad, _sacWidth){
  var _context = _canvas.getContext("2d");

  
  for(var i=0; i<fixationSaccade.length; i++){
    if(i == selectedUserDataIdx){
      var prev_x = 0;
      var prev_y = 0;
      for(var j=0; j<fixationSaccade[i].length; j++){
        var _x = Math.round(fixationSaccade[i][j].x*(_canvas.width/_xdim));
        var _y = Math.round(fixationSaccade[i][j].y*(_canvas.height/_ydim));
        if(j==0){
          prev_x = _x;
          prev_y = _y;
        }else{
          // draw saccade
          drawSaccade(_context, prev_x, prev_y, _x, _y, _sacWidth+2, "white", 1.0);
          drawSaccade(_context, prev_x, prev_y, _x, _y, _sacWidth, blackTone_4d, 1.0);
          if(j==1){
            drawFixation(_context, prev_x, prev_y, _fixRad-2, "#de2d26", 1.0);
          }
        }

        // draw fixation
        drawFixation(_context, _x, _y, _fixRad+2, "white", 1.0);
        drawFixation(_context, _x, _y, _fixRad, blackTone_4d, 1.0);

        prev_x = _x;
        prev_y = _y;
      }
    }
  }
}

function drawFeatureOnStimulus(_canvas, _xdim, _ydim, _fType){
  var _context = _canvas.getContext("2d");
  var _cWidth = _canvas.width;
  var _cHeight = _canvas.height;
  var _wRatio = _cWidth/_xdim;
  var _hRatio = _cHeight/_ydim;
  
  for(var i=0; i<_xdim; i++){
    for(var j=0; j<_ydim; j++){
      if(features_raw_data[_fType][i][j] > getFeatureThreshold(_fType)){
        var _x = i*_wRatio;
        var _y = j*_hRatio;
        var _w = _wRatio;
        var _h = _hRatio;
        drawFilledRect(_context, _x, _y, _w, _h, features_color[_fType], 0.5);
      }
    }
  }
}