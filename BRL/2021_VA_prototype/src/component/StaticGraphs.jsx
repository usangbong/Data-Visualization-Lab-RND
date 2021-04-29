import './StaticGraphs.scoped.scss';
import LineCharts from './LineCharts';
import Draggable from 'react-draggable';
import React, {useState} from 'react';

function StaticGraphs(props) {
    const {Seconds,static_value,PlayHook, static_checks} = props;
    const [Toggle, Toggle_on] = useState(true);
    
    return (
      <Draggable handle="#DRAGGTitle" >
      <div className={"StaticGraphs " + (Toggle ? 'MAXMODE' : 'MINMODE') + (static_checks.length>0 ? ' BORDERLAND' : '')} >
        {static_checks.length>0?<div id="DRAGGTitle" className="Title">Environment</div>:''}
        {static_checks.length>0?<div className="Minimizer" onClick={()=>{Toggle_on(!Toggle)}}>{Toggle?'_':'M'}</div>:''}
        {
          static_checks.map((val, i)=>{
            return (
                <LineCharts key={val}
                TYPE={'SG'} 
                NAME={val} 
                VALUES={static_value[val]}
                MINS={parseInt(Seconds/60)}
                HOOK={PlayHook}
                />
            )
          })
        }
      </div>
      </Draggable>
    );
  
}

export default StaticGraphs;
