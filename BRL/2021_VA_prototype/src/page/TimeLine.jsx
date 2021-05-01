import React, { useState , useEffect} from 'react';
import DatePicker from 'react-date-picker';
import Slider from 'rc-slider';
import ReactInterval from 'react-interval';

import 'rc-slider/assets/index.css';

import './TimeLine.scoped.scss';
import axios from 'axios';
//TODO: HOOK으로 데이터 변동 이벤트 APP에 보내기
const DELTA_TIME = 0.013564814814815;
const WINDOW_SIZE = 1172;
const DAT_SEC = 86400;

function TimeLine(props) {
  const [dates, datesonChange] = useState();
  const [slider_value, slider_valueChange] = useState(0);
  const [A_Time, A_TimeonChange] = useState(0);
  const [play_hook, play_hookChange] = useState(false);

  useEffect(() => {
    axios.get('http://localhost:3000/api/data/').then((res)=>{
      datesonChange(new Date(res.data[0]['data_dates']))
  })
  },[]);
  useEffect(() => {
    console.log(dates);
  },[dates]);

  useEffect(() => {
    A_TimeonChange(parseInt(slider_value/WINDOW_SIZE*DAT_SEC));
  },[slider_value]);

  useEffect(() => {
    props.secondUpdate(A_Time);
    //console.log(A_Time)
  },[A_Time]);
  useEffect(() => {
    props.PlayHookUpdate(play_hook);
  },[play_hook]);
  
  
  let marks = {};

  for(let i=0;i<25;i++)
  {
    marks[i] = {
      style: {
        marginTop: '5px',
        fontSize:'14px',
      },
      label: <strong>{i.toString()+':00'}</strong>,
    };
  }
  

  return (
    
    <div className="TimeLine">
          <ReactInterval {...{timeout:100, enabled:play_hook}}
          callback={() => {
            let tmp = slider_value+DELTA_TIME;
            if(tmp<WINDOW_SIZE)
            {
              slider_valueChange(tmp)
            }
            else{
              play_hookChange(false)
            }
            }} />

      <div className="DatePickerWrap">
        <div className="CompTitle"> Date </div>
      <DatePicker
        className="DatePickerS"
        onChange={datesonChange}
        value={dates}
      />
      </div>
      <div className="SilderWrap">
      <div className="CompTitle"> Time </div>
      <div className="SilderRobot" > 
        <div className="SilderRobotBtn" onMouseUp={()=>{play_hookChange(!play_hook)}}>
          {
            play_hook?'Pause':'Play'
          }
        </div>
        <div className="SilderRobotRail"  onMouseUp={(e)=>{
          
          if(e.target.className==='SilderRobotRail'){
            let temp = WINDOW_SIZE*(e.nativeEvent.layerX/WINDOW_SIZE)
            slider_valueChange(temp);
          }
          }}> 
          <div className="SilderRobotHandle" style={{
            left:slider_value
          }}> 
            <div className="SilderRobotHHMMSS"> 
            {
              (A_Time<(DAT_SEC/2)?'AM ':'PM ')+(new Date(A_Time * 1000).toISOString().substr(11, 8))
            }
            </div>
          </div>
        </div>
      </div>
        <Slider 
        onChange={value => {
          slider_valueChange(value);
        }}
        min={0}
        max={24}
        step={1}
        marks={marks}
        included={false} dots={true} 
        handleStyle={{
          display:'none'
        }}
        railStyle={{
          position: 'absolute',
          bottom: '-3px',
          marginLeft: '2.5px',
          height: '20px',
          border: '0.75px solid #767171',
          backgroundColor: 'rgba(51, 63, 80, 0.70)',
          borderRadius: '0%',
          verticalAlign: 'middle',
        }}
        dotStyle={{
          position: 'absolute',
          bottom: '-10px',
          marginLeft: '-5px',
          width: '10px',
          height: '26px',
          border: '0.75px solid #767171',
          backgroundColor: 'rgba(51, 63, 80, 0.70)',
          borderRadius: '0%',
          verticalAlign: 'middle',
        }} />
      </div>
    </div>
  );
}

export default TimeLine;
