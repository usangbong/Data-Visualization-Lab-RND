import React, { useState } from 'react';
import axios from 'axios';


import StimulusView from '../components/StimulusView';
import ColorBox from '../components/ColorBox';

let COLORS = [
  "#e31a1c", "#33a02c", "#ff7f00", "#1f78b4", "#6a3d9a",
  "#b15928", "#a6cee3", "#b2df8a", "#fb9a99", "#fdbf6f",
  "#cab2d6", "#ffff99", "#000000", "#FF6347", "#00ff00",
  "#0000ff", "#800000", "#ffffff", "#2F4F2F", "#7393B3"
];

const PORT = 5000;
const DIV_VALUE = 10;

const Home =()=> {
  // public variable
  const [COLOR_BOX_ARRAY, setColorBoxArray] = useState(["#e31a1c"]);
  const [SELECTED_COLOR_IDX, setSelectedColorIdx] = useState(0);
  const [STIMULUS_IMAGE_URL, setStiImgUrl] = useState([]);
  const [STIMULUS_INDEX, setStiIndex] = useState(-999);
  const [GRID_COLOR, setGridColor] = useState("black");
  const [GRID_DRAW_FLAG, setGridDrawFlag] = useState(true);
  
  // each page
  const [SELECTED_AREA, setSelectedArea] = useState([]);
  
  init();

  // init process
  function init(){
    // console.log('run init functions');
    if(STIMULUS_IMAGE_URL.length == 0){
      axios.get(`http://${window.location.hostname}:${PORT}/static/stimuli.json?`+Math.random())
      .then(response => {
        let _stiInfo = [];
        for(let i=0; i<Object.keys(response.data['name']).length; i++){
          let _url = `http://${window.location.hostname}:${PORT}/static/stimuli/`+response.data.name[i];
          let _width = response.data.width[i];
          let _height = response.data.height[i];
          _stiInfo.push({
            url: _url,
            width: _width,
            height: _height
          });
        }
        setStiImgUrl(_stiInfo);
        // console.log("setStiImgUrl");
        setStiIndex(0);
        // console.log("setStiIndex");
      })
      .catch(error =>{
        alert(`ERROR - ${error.message}`);
      });
    }
  }

  // functions for d3View
  const selectedAreaUpdate =(areaArr)=>{
    setSelectedArea(areaArr);
    // console.log(areaArr);
  }
  const selectedAreaChage=(chaneInfo)=>{
    // console.log(chaneInfo);
    let _ix = chaneInfo[0];
    let _iy = chaneInfo[1];
    // let _label = chaneInfo[3];
    let changedArr = []
    for(let i=0; i<SELECTED_AREA.length; i++){
      let _arr = [];
      for(let j=0; j<SELECTED_AREA[i].length; j++){
        if(SELECTED_AREA[i][j].ix == _ix && SELECTED_AREA[i][j].iy == _iy){
          // console.log(SELECTED_AREA[i][j]);
          continue;
        }
        _arr.push(SELECTED_AREA[i][j]);
      }
      changedArr.push(_arr);
    }
    setSelectedArea(changedArr);
    // console.log(changedArr);
    // console.log('duplicated area is removed');
  }
  const updateColorIndex=(changedColorIdx)=>{
    setSelectedColorIdx(changedColorIdx);
  }

  // functions for button click event
  function onClick_gridColor_button(){
    if(GRID_COLOR == "black"){
      setGridColor("white");
    }else{
      setGridColor("black");
    }
  }
  function onClick_nextStimulus_button(){
    // data save
    const postData = new FormData();
    let segArrString = "";
    for(let i=0; i<SELECTED_AREA.length; i++){
      let _rowStr = "";
      for(let j=0; j<SELECTED_AREA[i].length; j++){
        let _ix = SELECTED_AREA[i][j].ix;
        let _iy = SELECTED_AREA[i][j].iy;
        let _label = SELECTED_AREA[i][j].label;
        if(j != SELECTED_AREA[i].length-1){
          _rowStr = _rowStr+String(_ix)+","+String(_iy)+","+String(_label)+"|";
        }else{
          _rowStr = _rowStr+String(_ix)+","+String(_iy)+","+String(_label)+"/";
        }
        segArrString = segArrString+_rowStr;
      }
    }
    // console.log(segArrString);
    let imageURL = STIMULUS_IMAGE_URL[STIMULUS_INDEX].url;
    let imageWidth = STIMULUS_IMAGE_URL[STIMULUS_INDEX].width;
    let imageHeight = STIMULUS_IMAGE_URL[STIMULUS_INDEX].height;
    postData.set('seg_arr', segArrString);
    postData.set('img_url', imageURL);
    postData.set('img_width', imageWidth);
    postData.set('img_height', imageHeight);
    axios.post(`http://${window.location.hostname}:${PORT}/api/savedata`, postData)
    .then(response => {
      console.log("save data")
    })
    .catch(error =>{
      alert(`ERROR - ${error.message}`);
    });

    // change stimulus index (+1)
    setStiIndex(STIMULUS_INDEX+1);
    // init variables
    setSelectedColorIdx(0);
    setColorBoxArray(["#e31a1c"]);
    setSelectedArea([]);
  }
  function onClick_gridDrawFlag_button(){
    setGridDrawFlag(!GRID_DRAW_FLAG);
  }
  const colorAddingFunction =()=>{
    if(SELECTED_AREA[SELECTED_COLOR_IDX].length != 0){
      var colorArrLength = COLOR_BOX_ARRAY.length;
      if(colorArrLength >= COLORS.length){
        for(;;){
          const randomColor = Math.floor(Math.random()*16777215).toString(16);
          let _rc = "#" + randomColor;
          let dupColorFlag = false;
          for(let i=0; i<COLORS.length; i++){
            if(_rc==COLORS[i]){
              dupColorFlag = true;
              break;
            }
          }
          if(dupColorFlag != true){
            COLORS.push(_rc);
            break;
          }
        }
      }
      
      let color_arr = [];
      for(let i=0; i<colorArrLength+1; i++){
        color_arr.push(COLORS[i]);
      }
      setColorBoxArray(color_arr);
      console.log(color_arr.length)
      setSelectedColorIdx(SELECTED_COLOR_IDX+1);
      // console.log(color_arr);
    }else{
      alert("Press this btn after selecting area");
    }
    
  }
  const resetButtonClickFunction=()=>{
    setSelectedColorIdx(0);
    setColorBoxArray(["#e31a1c"]);
    setSelectedArea([]);
  }


  return (
    <div className="bodyDiv">
      <div className="colorViewer">
        <ColorBox 
          colorArray={COLOR_BOX_ARRAY}
          selectedColorIdx={SELECTED_COLOR_IDX}
          selectedArea={SELECTED_AREA}
          colorAddFunction={colorAddingFunction}
          restBtnFunction={resetButtonClickFunction}
          updateColorIndex={updateColorIndex}
        />
      </div>
      { STIMULUS_INDEX >= 0 &&
        <div className="imageViewer">
          <StimulusView
            imgURL={STIMULUS_IMAGE_URL[STIMULUS_INDEX]}
            gridWidthCellNumber={STIMULUS_IMAGE_URL[STIMULUS_INDEX].width/DIV_VALUE}
            gridHeightCellNumber={STIMULUS_IMAGE_URL[STIMULUS_INDEX].height/DIV_VALUE}
            gridColor={GRID_COLOR}
            gridVisableFlag={GRID_DRAW_FLAG}
            colorArray={COLOR_BOX_ARRAY}
            selectedArea={SELECTED_AREA}
            selectedColorIdx={SELECTED_COLOR_IDX}
            selectedAreaUpdate={selectedAreaUpdate}
            selectedAreaChage={selectedAreaChage}
          />
        </div>
      }
      <div className="interface">
        {STIMULUS_INDEX+1}/{STIMULUS_IMAGE_URL.length}&nbsp;
        <button onClick={onClick_nextStimulus_button}>Next</button>
        <button onClick={onClick_gridColor_button}>Grid color: {GRID_COLOR}</button>
        <button onClick={onClick_gridDrawFlag_button}>Grid draw: {String(GRID_DRAW_FLAG)}</button>
      </div>
    </div>
  );
}

export default Home;
