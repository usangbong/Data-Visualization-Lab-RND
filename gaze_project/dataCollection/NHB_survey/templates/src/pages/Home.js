import React, { useState } from 'react';
import axios from 'axios';

import IntroAggrement from '../components/IntroAggrement';
import Aggrement from '../components/Aggrement';

import IntroManual from '../components/IntroManual';
import Manual from '../components/Manual';

import IntroMeaning from '../components/IntroMeaning';
import Meaning from '../components/Meaning';

import IntroSubjectInfo from '../components/IntroSubjectInfo';
import SubjectInfo from '../components/SubjectInfo';

import IntroSurvey from '../components/IntroSurvey';
import StimulusView from '../components/StimulusView';
import LikertScaleQuestion from '../components/LikertScaleQuestion';

import IntroRewardInfo from '../components/IntroRewardInfo';
import RewardInfo from '../components/RewardInfo';
import ModifyCell from '../components/modifyCell';

import IntroEndContent from '../components/IntroEndContent';
import EndContent from '../components/EndContent';

import Footer from '../components/Footer';

const COLORS = [
  "#e31a1c", "#33a02c", "#ff7f00", "#1f78b4", "#6a3d9a",
  "#b15928", "#a6cee3", "#b2df8a", "#fb9a99", "#fdbf6f",
  "#cab2d6", "#ffff99", "#000000", "#FF6347", "#00ff00",
  "#0000ff", "#800000", "#ffffff", "#2F4F2F", "#7393B3"
];

const PORT = 5000;
// const PORT = 36003;

const PAGE_AGRREMENT = 0;
const PAGE_SUBJECT_INFO = 1;
const PAGE_MANUAL = 2;
const PAGE_MEANING = 3;
const PAGE_SURVEY_START = 4;

const M_VIDEO_URL = `http://${window.location.hostname}:${PORT}/static/manual/suvey_manual_720.mp4?`+Math.random();
const M_IMAGE_URL = `http://${window.location.hostname}:${PORT}/static/manual/m_example.png?`+Math.random();
const M_IMAGE_SALIENCY_INTENSITY = `http://${window.location.hostname}:${PORT}/static/manual/saliency_intensity.png?`+Math.random();
const M_IMAGE_SALIENCY_COLOR = `http://${window.location.hostname}:${PORT}/static/manual/saliency_color.png?`+Math.random();
const M_IMAGE_SALIENCY_ORIENTATION = `http://${window.location.hostname}:${PORT}/static/manual/saliency_orientation.png?`+Math.random();
const M_IMAGE_MEANING_INFO = `http://${window.location.hostname}:${PORT}/static/manual/meaning_info.png?`+Math.random();
const M_IMAGE_MEANING_CONTEXT = `http://${window.location.hostname}:${PORT}/static/manual/meaning_context.png?`+Math.random();
const M_IMAGE_MEANING_NO_SALIENCY = `http://${window.location.hostname}:${PORT}/static/manual/meaning_nosaliency.png?`+Math.random();
const M_IMAGE_MEANING_SALIENCY = `http://${window.location.hostname}:${PORT}/static/manual/meaning_saliency.png?`+Math.random();

const Home =()=> {
  // Main
  const [PAGE_NUMBER, setPageNumber] = useState(0);
  const [TOTAL_PAGE, setTotalPageNumber] = useState(0);
  const [PAGE_NEXT_BUTTON_DRAWABLE, setNextBtnDrawFlag] = useState(true);
  const [BROWSER, setWebBrowser] = useState("");
  const [USE_ENV, setUseEnvironment] = useState("");
  const [DATA_SAVE_LOG, setDataSaveLog] = useState(false);
  const [DATA_SURVEY_STEP, setSurveyStep] = useState(0);
  const [MODIFY_CELL, setModifyCellFlag] = useState(true);

  // // Manual
  // const [VIDEO_URL, setVideoUrl] = useState("");

  // LOG
  // {user} | {event} | {subEvent} | {stimulus} | {colorIdx} | {timeStamp}
  // {event} = 1) mouse: down; drag; up, 2) likert: add; reset; scoring, 3) paging: start; end, 4) error: firstSelect, addSelect, countSelect.
  const [USER_ID, setUserId] = useState("");
  const [EVENT_LOG, setEventLog] = useState([]);
  
  // PAGE_NUMBER = 1
  const [SUBJECT_BIRTH, setSubjectBirth] = useState("");
  const [SUBJECT_ED_LEVEL, setSubjectEducationLevel] = useState({value: 'opt_ed_level3', label: '학사학위 취득'});
  const [SUBJECT_EYE_COLOR_W, setSubjectColorWeak] = useState({value: 'opt_color_w1', label: '없음'});
  const [SUBJECT_CELL, setSubjectCell] = useState("");

  // PAGE_NUMBER = 3 to 52
  // public variable
  const [COLOR_BOX_ARRAY, setColorBoxArray] = useState(["#e31a1c"]);
  const [SELECTED_COLOR_IDX, setSelectedColorIdx] = useState(0);
  const [STIMULUS_IMAGE_URL, setStiImgUrl] = useState([]);
  const [STIMULUS_INDEX, setStiIndex] = useState(0);
  // stack data
  const [STACK_SELECTED_AREA, setStackSelectedArea] = useState([]);
  const [STACK_LIKERT_QUESTION_ARRAY, setStackLikertQuestionArray] = useState([]);
  // each page
  const [SELECTED_AREA, setSelectedArea] = useState([]);
  const [LIKERT_QUESTION_ARRAY, setLikertQuestionArray] = useState([]);

  // PAGE_NUMBER = 53
  
  const [SLECTED_REWARD, setSelectedReward] = useState({value:"reward1", label: "문화상품권"});
  
  const getTimestamp=()=>{
    let timestamp="";
    timestamp =+ new Date();
    return timestamp;
  }

  const pushEventLog=(log)=>{
    let elog = EVENT_LOG;
    if(EVENT_LOG.length == 0){
      elog = [];
    }
    elog.push(log);
    setEventLog(elog);
    // console.log(elog);
  }

  const updateChangedCell=(changedCell)=>{
    setSubjectCell(changedCell);
    let userid = USER_ID.split("_")[0]+"_"+USER_ID.split("_")[1]+"_"+changedCell.split("-")[1]+changedCell.split("-")[2];
    setUserId(userid);
    // console.log(userid);
    let updatedLog = [];
    for(let i=0; i<EVENT_LOG.length; i++){
      let _log = EVENT_LOG[i];
      _log.user = userid;
      updatedLog.push(_log);
    }
    // console.log(updatedLog);
    setEventLog(updatedLog);
  }

  const updateStackSelectedArea=(arr)=>{
    // console.log("updateStackSelectedArea");
    let stackedArr = STACK_SELECTED_AREA;
    stackedArr.push(arr)
    // console.log(stackedArr);
    setStackSelectedArea(stackedArr);
  }

  const updateStackLikertQuestionArray=(arr)=>{
    // console.log("updateStackLikertQuestionArray");
    let stackedArr = STACK_LIKERT_QUESTION_ARRAY;
    stackedArr.push(arr);
    // console.log(stackedArr);
    setStackLikertQuestionArray(stackedArr);
  }

  const selectedColorIndexUpdate =(index)=>{
    setSelectedColorIdx(index);
  }

  const selectedAreaUpdate =(areaArr)=>{
    // console.log(areaArr);
    setSelectedArea(areaArr);
    let selectedAreaSize = areaArr.length;
    if(selectedAreaSize!=0){
      for(let i=0; i<areaArr.length; i++){
        if(areaArr[i].length == 0){
          selectedAreaSize--;
        }
      }
      if(selectedAreaSize > 0){
        selectedColorIndexUpdate(selectedAreaSize-1);
        let lqarr = [];
        for(let i=0; i<selectedAreaSize; i++){
          let _a={
            value: 'lp0', label: '얼마나 의미 있나요?'
          };
          if(i<LIKERT_QUESTION_ARRAY.length){
            _a = LIKERT_QUESTION_ARRAY[i];
          }
          lqarr.push(_a);
        }
        likertQuestionArrayUpdate(lqarr);
      }
    }
  }

  const likertQuestionArrayUpdate =(arr)=>{
    setLikertQuestionArray(arr);
  }

  const browserType=(agt)=>{
    if (agt.indexOf("chrome") != -1) return 'Chrome'; 
    if (agt.indexOf("mozilla/5.0") != -1) return 'Mozilla'; 
    if (agt.indexOf("opera") != -1) return 'unavailable'; 
    if (agt.indexOf("staroffice") != -1) return 'unavailable'; 
    if (agt.indexOf("webtv") != -1) return 'unavailable'; 
    if (agt.indexOf("beonex") != -1) return 'unavailable'; 
    if (agt.indexOf("chimera") != -1) return 'unavailable'; 
    if (agt.indexOf("netpositive") != -1) return 'unavailable'; 
    if (agt.indexOf("phoenix") != -1) return 'unavailable'; 
    if (agt.indexOf("firefox") != -1) return 'unavailable'; 
    if (agt.indexOf("safari") != -1) return 'unavailable'; 
    if (agt.indexOf("skipstone") != -1) return 'unavailable'; 
    if (agt.indexOf("msie") != -1) return 'unavailable'; 
    if (agt.indexOf("netscape") != -1) return 'unavailable'; 
    // if (agt.indexOf("opera") != -1) return 'Opera'; 
    // if (agt.indexOf("staroffice") != -1) return 'Star Office'; 
    // if (agt.indexOf("webtv") != -1) return 'WebTV'; 
    // if (agt.indexOf("beonex") != -1) return 'Beonex'; 
    // if (agt.indexOf("chimera") != -1) return 'Chimera'; 
    // if (agt.indexOf("netpositive") != -1) return 'NetPositive'; 
    // if (agt.indexOf("phoenix") != -1) return 'Phoenix'; 
    // if (agt.indexOf("firefox") != -1) return 'Firefox'; 
    // if (agt.indexOf("safari") != -1) return 'Safari'; 
    // if (agt.indexOf("skipstone") != -1) return 'SkipStone'; 
    // if (agt.indexOf("msie") != -1) return 'Internet Explorer'; 
    // if (agt.indexOf("netscape") != -1) return 'Netscape';
  }

  function onClick_pageNumberAdd_button(){
    // console.log(PAGE_NUMBER);
    // console.log(TOTAL_PAGE);
    if(PAGE_NUMBER == PAGE_AGRREMENT){
      // PAGE_AGGREMENT = 0
      // set video url setting
      // setVideoUrl((): void=> manualVideo);
      // user env check
      // PC-Mobile
      let envFilter="win16|win32|win64|macintel|mac|";
      if(navigator.platform){
        if(envFilter.indexOf(navigator.platform.toLocaleLowerCase())<0){
          // mobile
          setUseEnvironment("mobile");
          alert("모바일 환경에서 접속했습니다. PC로 접속해주세요.")
        }else{
          // pc
          setUseEnvironment("pc");
          if(navigator.platform.toLocaleLowerCase()=="mac"){
            alert("...Mac CHECKING...");
          }
          if(navigator.platform.toLocaleLowerCase()=="macintel"){
            alert("...Macintel CHECKING...");
          }
        }
      }
      // Web browser
      let _browser = browserType(navigator.userAgent.toLocaleLowerCase());
      setWebBrowser(_browser);
      if(_browser == "unavailable"){
        alert("크롬(Chrome), 엣지(Microsoft Edge), 웨일 브라우저를 사용해주세요.")
      }

      alert("개인정보 수집 및 이용에 동의했습니다.");
      axios.get(`http://${window.location.hostname}:${PORT}/static/stimuli_test.json?`+Math.random())
      .then(response => {
        // console.log(Object.keys(response.data['name']).length);
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
        setStiIndex(0);

        // PAGE_SURVEY_START = 4
        setTotalPageNumber(PAGE_SURVEY_START+_stiInfo.length);
        setPageNumber(PAGE_NUMBER+1);
      })
      .catch(error =>{
        alert(`ERROR - ${error.message}`);
      });
    }else if(PAGE_NUMBER == PAGE_SUBJECT_INFO){
      // PAGE_SUBJECT_INFO = 1
      if(SUBJECT_CELL == "" || SUBJECT_BIRTH == ""){
        alert("모든 항목을 입력해주세요.");
      }else{
        setPageNumber(PAGE_NUMBER+1);
        let _date = new Date().toISOString().split("T")[0];
        let _time = new Date().toTimeString().split(" ")[0].split(":");
        let dateForm = _date+"-"+_time[0]+_time[1];
        let userid = dateForm+"_"+SUBJECT_BIRTH+"_"+SUBJECT_CELL.split("-")[1]+SUBJECT_CELL.split("-")[2];
        setUserId(userid);
        // console.log(userid);
      }
    }else if(PAGE_NUMBER == PAGE_MANUAL){
      // PAGE_MANUAL = 2
      setPageNumber(PAGE_NUMBER+1);
    }else if(PAGE_NUMBER == PAGE_MEANING){
      // PAGE_MEANING = 3
      setPageNumber(PAGE_NUMBER+1);
      // loging
      pushEventLog({
        user: USER_ID, 
        event: "paging",
        subEvent: "start",
        stimulus: STIMULUS_IMAGE_URL[STIMULUS_INDEX].url.split("/static/stimuli/")[1],
        colorIdx: 0,
        timeStamp: getTimestamp()
      });
    }else if(PAGE_NUMBER >= PAGE_SURVEY_START && PAGE_NUMBER<TOTAL_PAGE){
      // PAGE_SURVEY_START = 4
      let trueDataFlag = true;
      let likertCountFlag = true;
      if(LIKERT_QUESTION_ARRAY.length<5){
        likertCountFlag = false;
      }
      for(let i=0; i<LIKERT_QUESTION_ARRAY.length; i++){
        if(LIKERT_QUESTION_ARRAY[i].value=='lp0'){
          trueDataFlag = false;
          break;
        }
      }
      
      if(trueDataFlag==true){
        if(likertCountFlag == true){
          // loging
          pushEventLog({
            user: USER_ID, 
            event: "paging",
            subEvent: "end",
            stimulus: STIMULUS_IMAGE_URL[STIMULUS_INDEX].url.split("/static/stimuli/")[1],
            colorIdx: 0,
            timeStamp: getTimestamp()
          });
          if(PAGE_NUMBER != TOTAL_PAGE-1){
            // loging
            pushEventLog({
              user: USER_ID, 
              event: "paging",
              subEvent: "start",
              stimulus: STIMULUS_IMAGE_URL[STIMULUS_INDEX+1].url.split("/static/stimuli/")[1],
              colorIdx: SELECTED_COLOR_IDX,
              timeStamp: getTimestamp()
            });
          }
          setPageNumber(PAGE_NUMBER+1);
          // console.log(PAGE_NUMBER-2);
          setStiIndex(PAGE_NUMBER-(PAGE_SURVEY_START-1));
          // stack selected area and init
          updateStackSelectedArea(SELECTED_AREA);
          setSelectedArea([]);
          // stack likert question array and init
          updateStackLikertQuestionArray(LIKERT_QUESTION_ARRAY);
          setLikertQuestionArray([]);
          // init color box array
          setColorBoxArray(["#e31a1c"]);
          // init selected color index
          setSelectedColorIdx(0);
          if(PAGE_NUMBER==TOTAL_PAGE-1){
            setNextBtnDrawFlag(false);
          }
          // init survey step
          setSurveyStep(0);
        }else{
          alert("이미지에서 최소 5개 영역을 선택하고 평가해주세요.");
          // loging
          pushEventLog({
            user: USER_ID, 
            event: "error",
            subEvent: "countSelect",
            stimulus: STIMULUS_IMAGE_URL[STIMULUS_INDEX].url.split("/static/stimuli/")[1],
            colorIdx: SELECTED_COLOR_IDX,
            timeStamp: getTimestamp()
          });
        }
      }else{
        alert("선택한 영역들의 의미를 평가해주세요.");
      }
    }
  }

  function onClick_dataSave_button(){
    let cellConfirm = window.confirm("입력된 연락처는 '"+SUBJECT_CELL+"'입니다. 저장하겠습니까?");
    setModifyCellFlag(cellConfirm);
    if(cellConfirm==true){
      // stacked selected area
      let stackedAreaArr = "";
      let areaArr = "";
      for(let i=0; i<STACK_SELECTED_AREA.length; i++){
        areaArr = "";
        for(let j=0; j<STACK_SELECTED_AREA[i].length; j++){
          let _strArr = "";
          for(let k=0; k<STACK_SELECTED_AREA[i][j].length; k++){
            let _ix = STACK_SELECTED_AREA[i][j][k].ix;
            let _iy = STACK_SELECTED_AREA[i][j][k].iy;
            let _ic = STACK_SELECTED_AREA[i][j][k].ic;
            let _c = STACK_SELECTED_AREA[i][j][k].c;
            _strArr = _strArr+_ix + "," + _iy + "," + _ic + "," + _c+"/";
          }
          if(j!=STACK_SELECTED_AREA[i].length-1){
            _strArr = _strArr+"|";
          }
          areaArr = areaArr+_strArr;
        }
        areaArr = areaArr+";";
        stackedAreaArr = stackedAreaArr+areaArr;
      }
      // console.log(stackedAreaArr);

      // stacked likert scale data form change
      let siqArr = "";
      for(let i=0; i<STACK_LIKERT_QUESTION_ARRAY.length; i++){
        let _strArr = "";
        if(STACK_LIKERT_QUESTION_ARRAY[i] == []){
          _strArr = _strArr+";";
        }else{
          for(let j=0; j<STACK_LIKERT_QUESTION_ARRAY[i].length; j++){
            _strArr = _strArr+STACK_LIKERT_QUESTION_ARRAY[i][j].value;
            if(j!=STACK_LIKERT_QUESTION_ARRAY[i].length-1){
              _strArr = _strArr+"|";
            }
          }
          _strArr = _strArr+";";
        }
        siqArr = siqArr+_strArr;
      }
      // event log data form change
      // console.log(EVENT_LOG);
      let eLog = "";
      for(let i=0; i<EVENT_LOG.length; i++){
        let _user = EVENT_LOG[i].user;
        let _event = EVENT_LOG[i].event;
        let _subEvent = EVENT_LOG[i].subEvent;
        let _stimulus = EVENT_LOG[i].stimulus;
        let _colorIdx = EVENT_LOG[i].colorIdx;
        let _t = EVENT_LOG[i].timeStamp;
        eLog = eLog + _user+"|"+_event+"|"+_subEvent+"|"+_stimulus+"|"+_colorIdx+"|"+_t;
        if(i != EVENT_LOG.length-1){
          eLog = eLog+ ";"
        }
        // console.log(eLog);
      }
      // console.log("stacked likert scale data: ");
      // console.log(siqArr);
      const postData = new FormData();
      postData.set('SUBJECT_ID', USER_ID);
      postData.set('SUBJECT_CELL', SUBJECT_CELL);
      postData.set('SUBJECT_BIRTH', SUBJECT_BIRTH);
      postData.set('SUBJECT_ED_LEVEL', SUBJECT_ED_LEVEL.value);
      postData.set('SUBJECT_EYE_WEAK', SUBJECT_EYE_COLOR_W.value);
      // postData.set('SELECTED_AREA_ARR', JSON.stringify(STACK_SELECTED_AREA));
      postData.set('SELECTED_AREA_ARR', stackedAreaArr);
      postData.set('LIKERT_SCORE_ARR', siqArr);
      postData.set('SELECTED_REWARD', SLECTED_REWARD.value);
      postData.set('EVENT_LOG', eLog);
      axios.post(`http://${window.location.hostname}:${PORT}/api/savedata`, postData)
      .then(response => {
        setDataSaveLog(true);
      })
      .catch(error =>{
        alert(`ERROR - ${error.message}`);
      });
    }
    // console.log("SUBJECT_BIRTH: "+SUBJECT_BIRTH);
    // console.log("SUBJECT_ED_LEVEL: ");
    // console.log(SUBJECT_ED_LEVEL);
    // console.log("SUBJECT_EYE_COLOR_W: ");
    // console.log(SUBJECT_EYE_COLOR_W);
    // console.log("STACK_SELECTED_AREA: ");
    // console.log(STACK_SELECTED_AREA);
    // console.log("STACK_LIKERT_QUESTION_ARRAY: ");
    // console.log(STACK_LIKERT_QUESTION_ARRAY);
    // console.log("SUBJECT_CELL: "+SUBJECT_CELL);
    // console.log("SLECTED_REWARD.value: "+SLECTED_REWARD.value);
    // console.log("SLECTED_REWARD.label: "+SLECTED_REWARD.label);
  }

  const colorAddingFunction =()=>{
    var colorArrLength = COLOR_BOX_ARRAY.length;
    if(colorArrLength >= COLORS.length){
      alert("더 이상 색상(영역)을 추가할 수 없습니다.");
    }else{
      let color_arr = [];
      for(let i=0; i<colorArrLength+1; i++){
        color_arr.push(COLORS[i]);
      }
      setColorBoxArray(color_arr);
      selectedColorIndexUpdate(SELECTED_COLOR_IDX+1);
    }
  }

  const resetButtonClickFunction=()=>{
    setSurveyStep(0);
    setSelectedColorIdx(0);
    setColorBoxArray(["#e31a1c"]);
    setSelectedArea([]);
    setLikertQuestionArray([]);
  }

  return (
    <div className="bodyDiv">
      {/* PAGE_NUMBER = 0: private information aggrement */}
      { PAGE_NUMBER == PAGE_AGRREMENT &&
        <div className="topDiv">
          <IntroAggrement />
        </div>
      }
      { PAGE_NUMBER == PAGE_AGRREMENT &&
        <Aggrement />
      }

      {/* PAGE_NUMBER = 1: subject information A */}
      { BROWSER != "unavailable" && USE_ENV == "pc" && PAGE_NUMBER == PAGE_SUBJECT_INFO &&
        <div className="topDiv">
          <IntroSubjectInfo />
        </div>
      }
      { BROWSER != "unavailable" && USE_ENV == "pc" && PAGE_NUMBER == PAGE_SUBJECT_INFO &&
        <SubjectInfo 
          SUBJECT_ED_LEVEL={SUBJECT_ED_LEVEL}
          SUBJECT_EYE_COLOR_W={SUBJECT_EYE_COLOR_W}
          updateSubjectCell={setSubjectCell}
          updateSubjectBirth={setSubjectBirth}
          updateSubjectED={setSubjectEducationLevel}
          updateSubjectEye={setSubjectColorWeak}
        />
      }

      {/* PAGE_NUMBER = 2: manual */}
      { BROWSER != "unavailable" && USE_ENV == "pc" && PAGE_NUMBER == PAGE_MANUAL &&
        <div className="topDiv">
          <IntroManual />
        </div>
      }
      { BROWSER != "unavailable" && USE_ENV == "pc" && PAGE_NUMBER == PAGE_MANUAL &&
        <Manual 
          VIDEO_URL={M_VIDEO_URL}
          IMAGE_URL={M_IMAGE_URL}
        />
      }

      {/* PAGE_NUMBER == 3: meaning */}
      { BROWSER != "unavailable" && USE_ENV == "pc" && PAGE_NUMBER == PAGE_MEANING &&
        <IntroMeaning />
      }
      { BROWSER != "unavailable" && USE_ENV == "pc" && PAGE_NUMBER == PAGE_MEANING &&
        <Meaning 
          IMG_URL_INTENSITY={M_IMAGE_SALIENCY_INTENSITY}
          IMG_URL_COLOR={M_IMAGE_SALIENCY_COLOR}
          IMG_URL_ORIENTATION={M_IMAGE_SALIENCY_ORIENTATION}
          IMG_URL_MEAN_INFO={M_IMAGE_MEANING_INFO}
          IMG_URL_MEAN_CONTEXT={M_IMAGE_MEANING_CONTEXT}
          IMG_URL_MEAN_NOSALIENCY={M_IMAGE_MEANING_NO_SALIENCY}
          IMG_URL_MEAN_SALIENCY={M_IMAGE_MEANING_SALIENCY}
      />
      }

      {/* PAGE_NUMBER >= 4 to end-1: survey */}
      { BROWSER != "unavailable" && USE_ENV == "pc" && PAGE_NUMBER >= PAGE_SURVEY_START && PAGE_NUMBER < TOTAL_PAGE &&
        <div className="topDiv">
          <IntroSurvey
            surveyStep={DATA_SURVEY_STEP}
            colorArray={COLOR_BOX_ARRAY}
          />
        </div>
      }
      
      { BROWSER != "unavailable" && USE_ENV == "pc" && PAGE_NUMBER >= PAGE_SURVEY_START && PAGE_NUMBER < TOTAL_PAGE &&
        <div className="bodyStiDiv">
          <div className="stimulusViewDiv">
            <StimulusView
              USER_ID={USER_ID}
              pushEventLogFunc={pushEventLog}
              imgURL={STIMULUS_IMAGE_URL[STIMULUS_INDEX]}
              gridWidthCellNumber={50}
              gridHeightCellNumber={50}
              gridVisableFlag={false}W
              colorArray={COLOR_BOX_ARRAY}
              selectedArea={SELECTED_AREA}
              selectedColorIdx={SELECTED_COLOR_IDX}
              selectedAreaUpdate={selectedAreaUpdate}
              surveyStep={DATA_SURVEY_STEP}
              updateSurveyStep={setSurveyStep}
            />
          </div>
          <div className="likertDiv">
            <LikertScaleQuestion
              USER_ID={USER_ID}
              STIMULUS={STIMULUS_IMAGE_URL[STIMULUS_INDEX].url.split("/static/stimuli/")[1]}
              pushEventLogFunc={pushEventLog}
              colorArray={COLOR_BOX_ARRAY}
              colorAddFunction={colorAddingFunction}
              selectedColorIdx={SELECTED_COLOR_IDX}
              selectedArea={SELECTED_AREA}
              likertScaleArr={LIKERT_QUESTION_ARRAY}
              likertScaleArrUpdate={likertQuestionArrayUpdate}
              restBtnFunction={resetButtonClickFunction}
              surveyStep={DATA_SURVEY_STEP}
              updateSurveyStep={setSurveyStep}
            />
          </div>
        </div>
      }

      { BROWSER != "unavailable" && USE_ENV == "pc" && PAGE_NUMBER == TOTAL_PAGE && DATA_SAVE_LOG == false &&
        <div className="topDiv">
          <IntroRewardInfo />
        </div>
      }
      { BROWSER != "unavailable" && USE_ENV == "pc" && PAGE_NUMBER == TOTAL_PAGE && DATA_SAVE_LOG == false &&
        <RewardInfo
          // updateSubjectCell={setSubjectCell}
          SLECTED_REWARD={SLECTED_REWARD}
          updateSelcetdReward={setSelectedReward}
        />
      }
      { MODIFY_CELL == false &&
        <ModifyCell
          MODIFY_CELL_FLAG={MODIFY_CELL}
          CELL_BEFORE={SUBJECT_CELL}
          updateSubjectCellandApply={updateChangedCell}
        />
      }

      <div className="footDiv">
        { PAGE_NUMBER > 0 && DATA_SAVE_LOG == false &&
          <h3>{PAGE_NUMBER}/{TOTAL_PAGE}&nbsp;</h3>
        }
        <h3>&nbsp;</h3>
        { PAGE_NEXT_BUTTON_DRAWABLE == true &&
          <button onClick={onClick_pageNumberAdd_button}>다음</button>
        }
        { PAGE_NEXT_BUTTON_DRAWABLE == false && DATA_SAVE_LOG == false &&
          <button onClick={onClick_dataSave_button}>저장</button>
        }
      </div>

      { DATA_SAVE_LOG == true &&
        <div className="topDiv">
          <IntroEndContent />
        </div>
      }
      { DATA_SAVE_LOG == true &&
        <EndContent />
      }
      <div className="footer">
        <Footer />
      </div>
    </div>
  );
  
}

export default Home;
