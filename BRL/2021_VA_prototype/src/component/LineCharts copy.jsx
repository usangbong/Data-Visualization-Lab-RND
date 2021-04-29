import React, {useState, useEffect } from 'react';
import {Line}  from 'react-chartjs-2'
import 'chartjs-plugin-streaming';
import './LineCharts.scoped.scss';

function LineCharts(props) {

  //props.HOOK
  const [DATAS, DATASO_on] = useState([]);

  const [DATA, DATA_on] = useState({});
  const [COUNTER, COUNTER_on] = useState(0);

  
  useEffect(()=>{
    let temp = props.VALUES.slice((props.SECONDS-6)>-1?(props.SECONDS-6):0,props.SECONDS+1)
    let resArray = [];
    for(let i=props.SECONDS;i<props.SECONDS+temp.length;i++)
    {
      resArray.push({x:i,y:props.VALUES[i]})
    }
    DATASO_on(resArray)
  },[])
  
  useEffect(()=>{
    DATA_on({
      datasets: [
        {
          label: props.NAME,
          borderColor: "rgb(255, 99, 132)",
          backgroundColor: "rgba(255, 99, 132, 0.5)",
          lineTension: 0,
          borderDash: [8, 4],
          data: DATAS
        }
      ]
    });
    console.log(DATAS)
  },[DATAS])
  
  let options = {
    type: "line",
    scales: {
      xAxes: [
        {
          type: 'realtime',
        }
      ]
    },
    plugins:{
      streaming: {            // enabled by default
        duration: 20000,    // data in the past 20000 ms will be displayed
        refresh: 1000,      // onRefresh callback will be called every 1000 ms
        delay: 2000,        // delay of 1000 ms, so upcoming values are known before plotting a line
        frameRate: 30,      // chart is drawn 30 times every second
        pause: !props.HOOK,      // chart is not paused
        onRefresh: function() {
          if(props.HOOK)
            {
              DATASO_on([...DATAS,{
                x: COUNTER,
                y: props.VALUES[COUNTER]
              }]);
              console.log(COUNTER)
              COUNTER_on(COUNTER+1)
            }
        }
      }
    }
  };

  return (
    <div>
      <Line data={DATA} options={options} />
    </div>
  );
}

export default LineCharts;
