import React, {useState, useEffect,useRef ,useImperativeHandle } from 'react';
import axios from 'axios';
import PageHeader from './PageHeader';

import './History.scoped.scss';



//TODO: Onclick 이벤트와 param APP에 넘기기

const History = React.forwardRef( (props,ref) =>{
  const [value, onValue] = useState([]);
  const historyRef = useRef(null);


  useEffect(()=>{
    axios.get('http://localhost:3000/api/history/').then((res)=>{
      onValue(res.data)
    })
  },[])
  
  useEffect(()=>{
    console.log(value)
  },[value])

  function addHistory(ctx){
    let tempAraay = value;
    console.log(tempAraay);
    //tempAraay.push({'datetime':new Date().toISOString().substr(0, 19),'img_path':value[2]['img_path']})
    onValue([{'datetime':new Date().toISOString().substr(0, 19),'img_path':value[2]['img_path']},...tempAraay])
  };
  
  useImperativeHandle(ref, () => ({
    addHistory(ctx)
    {
      return addHistory(ctx); 
    }
  }) , [historyRef]); // deps도 추가가능하다.

  
  return (
    <div className="History" >
      <div className="History_H">
      <PageHeader msg={'History'} ></PageHeader>
      </div>
      <div className="HID_SAVE" onClick={()=>{
        addHistory()
        //props.SaveHistory()
        }}>&#128249;</div>
      
      {
        value.map((val,i) =>{
          return (
            <div key={i} className="HistoryCard">
              <div>{val['datetime']}</div>
              <img alt='' className="HistoryImg" src={val['img_path']}></img>
            </div>
          )
        }
        )
      }
    </div>
  );
});

export default History;
