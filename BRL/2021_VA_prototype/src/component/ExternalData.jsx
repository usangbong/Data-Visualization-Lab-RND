import React, {useState, useEffect,useRef } from 'react';
import axios from 'axios';

import './ExternalData.scoped.scss';


function ExternalData(props) {

  const [value, onValue] = useState([]);
  const [checkList, checkList_on] = useState([]);
  const nameInput = useRef();

  useEffect(()=>{
    axios.get('http://localhost:3000/api/static/').then((res)=>{
      
      onValue(Object.keys(res.data))
    })
  },[])
  
  useEffect(()=>{
    console.log(value)
  },[value])

  useEffect(()=>{
    props.static_check_update(checkList)
  },[checkList])
  

  return (
    <div className="ExternalData">
      <div className="Title">ExternalData</div>
      <div className="Enviroment">
      <div className="THBOX">
        <div>Enviroment</div>
        <div>Values</div>
      </div>
      <div className="TBODYBOX">
      <div className="SelectBox_code" ref={nameInput}>
      {
        value.map((val,i) =>{
          return (
            <div key={i}>
              <input type="checkbox" id={val} onChange={(e)=>{
                let tmp = nameInput.current.childNodes;
                let tmp_res =[];
                for(let i = 0;i<tmp.length;i++)
                {
                  if(tmp[i].childNodes[0].checked)
                  {
                    tmp_res.push(tmp[i].childNodes[0].id);
                  }
                }
                checkList_on(tmp_res);
              }} />
              <label htmlFor={val}>{val}</label>
            </div>
          )
        }
        )
      }
          </div>
          <div className="ValueBox_code">
  
          </div>
      </div>
      </div>
      <div className="Traffic">
        <div className="THBOX">
          <div>Traffic</div>
          <div>Values</div>
        </div>
        <div className="TBODYBOX">
        <div className="SelectBox_code">
            
            </div>
            <div className="ValueBox_code">
    
            </div>
        </div>
        </div>
    </div>
  );
}

export default ExternalData;
