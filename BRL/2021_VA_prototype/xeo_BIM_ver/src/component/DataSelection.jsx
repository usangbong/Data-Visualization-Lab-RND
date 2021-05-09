import React, {useState, useEffect, useRef } from 'react';
import axios from 'axios';

import './DataSelection.scoped.scss';

function DataSelection(props) {

  const [value, onValue] = useState([]);
  const [checkList, checkList_on] = useState([]);
  const nameInput = useRef();

  useEffect(()=>{
    axios.get('http://localhost:3000/api/dynamic/').then((res)=>{
      onValue(Object.keys(res.data))
    })
  },[])
  
  useEffect(()=>{
  },[value])

  useEffect(()=>{
    let tmpS = checkList.join(';');
    props.SpawnEnemies(tmpS);
  },[checkList])
  
  return (
    <div className="DataSelection">
      <div className="Title">DataSelection</div>
      <div className="SensorData">
      SensorData
        <div className="SelectBox" ref={nameInput}>
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
      </div>
      <div className="StateAnalysis">
      StateAnalysis
        <div className="SelectBox_2">
        <div>
            <input type="radio" id="CrossSectionalAreaofCables" name="d2" defaultChecked={true}/>
            <label htmlFor="CrossSectionalAreaofCables">Cross-Sectional Area of Cables</label>
          </div>
          <div>
            <input type="radio" id="Deteriorationcurve" name="d2" />
            <label htmlFor="Deteriorationcurve">Deterioration curve</label>
          </div>
          <div>
            <input type="radio" id="AnomalyScore" name="d2" />
            <label htmlFor="AnomalyScore">Anomaly Score</label>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DataSelection;
