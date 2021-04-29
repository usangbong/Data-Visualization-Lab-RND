import './DynamicGraphs.scoped.scss';
import LineCharts from './LineCharts';
import WindGraph from '../box/WindGraph';
import Draggable from 'react-draggable';
import React, {useState} from 'react';


function DynamicGraphs(props) {
    const {PlayHook,Seconds,dynamic_graphs,dynamic_value } = props;
    const [Toggle, Toggle_on] = useState(true);

    return (
      <div className="DynamicWrap">
      {
        dynamic_graphs.map((val, i)=>{
          if(val==='풍향풍속계')
          {
            return (
              <Draggable handle=".Title">
              <div className={"DynamicGraphs " + (Toggle ? 'MAXMODE' : 'MINMODE') + ' BORDERLAND'} >
                <div className="Title">{val}</div>
                <div className="Minimizer" onClick={()=>{Toggle_on(!Toggle)}}>{Toggle?'_':'M'}</div>
                      <WindGraph 
                      key={val}
                      TYPE={'DG'} 
                      NAME={val} 
                      VALUES={dynamic_value[val]}
                      MINS={parseInt(Seconds)}
                      HOOK={PlayHook}
                      />
              </div>
              </Draggable>
          )
          }
          else{
            return (
              <Draggable handle=".Title">
                
              <div className={"DynamicGraphs " + (Toggle ? 'MAXMODE' : 'MINMODE') + ' BORDERLAND'} >
                <div className="Title">{val}</div>
                <div className="Minimizer" onClick={()=>{Toggle_on(!Toggle)}}>{Toggle?'_':'M'}</div>
                      <LineCharts 
                      key={val}
                      TYPE={'DG'} 
                      NAME={val} 
                      VALUES={dynamic_value[val]}
                      MINS={parseInt(Seconds)}
                      HOOK={PlayHook}
                      />
              </div>
              </Draggable>
          )
          }
        })
      }
      {props.check_yeol?
              <Draggable handle=".Title">
                
              <div className={"DynamicGraphs " + (Toggle ? 'MAXMODE' : 'MINMODE') + ' BORDERLAND'} >
                <div className="Title">열화곡선</div>
                <div className="Minimizer" onClick={()=>{Toggle_on(!Toggle)}}>{Toggle?'_':'M'}</div>
                  <img alt='' className="YeolImg" src={'images/열화곡선.png'}></img>
              </div>
              </Draggable>
          :''}
      </div>
      
    );
  
}

export default DynamicGraphs;
