import React, {useState, useEffect,useRef } from 'react';
import Chart from 'react-apexcharts'
import './LineCharts.scoped.scss';

function LineCharts(props) {
  const [chart_data, chart_data_on] = useState([]);
  const [chart_options, chart_options_on] = useState({});
  const [preMins, MINS_on] = useState(0);
  const nameInput = useRef();
  const {NAME,VALUES,MINS} = props;

  useEffect(()=>{
    
    if(Math.abs(MINS-preMins)>1||chart_data.length===0)
    {
      let count = MINS>5?5:MINS;
      if(props.TYPE==='DG')
      {
        count = MINS>15?15:MINS
      }
    
      let i = MINS-count;
      let tempArray = [];
      while (i <= MINS) {
        let x = i;
        let y = VALUES[i];
        tempArray.push({x:x, y:y});
        i++;
      }
      
      chart_data_on([{data: tempArray}])
      MINS_on(MINS)
    }
    else if(preMins!==MINS)
    {
      let x = MINS;
      let y = VALUES[MINS];
      let tempArray = chart_data[0].data;
      tempArray.push({x:x, y:y})
      chart_data_on([{data: tempArray}])
      MINS_on(MINS)
    }
},[MINS])

  useEffect(()=>{
    if(chart_data.length>0)
    {

        nameInput.current.chart.updateSeries([{
          data: chart_data[0].data
        }])
      
      
      
      let tmpYs= nameInput.current.chart.data.twoDSeries;
      tmpYs.sort();
      nameInput.current.chart.removeAnnotation('my-annotation'+NAME.split(' ')[0]);
      nameInput.current.chart.addYaxisAnnotation({
        id: 'my-annotation'+NAME.split(' ')[0],
        y: tmpYs[parseInt(tmpYs.length*0.3)],
        y2: tmpYs[parseInt(tmpYs.length*0.7)],
        borderColor: '#000',
        fillColor: '#FEB019',
        opacity: 0.2,
        label: {
          borderColor: '#333',
          style: {
            fontSize: '8px',
            color: '#333',
            background: '#FEB019',
          },
          text: 'Normal Boundary',
        }
      });
      if(props.TYPE==='DG')
      {
        if(chart_data[0].data.length>15){
          chart_data_on([{data: chart_data[0].data.slice(-15,-1)}]);
          nameInput.current.chart.updateSeries([{
            chart_data
          }], false, true);
        }
      }
      else{
        if(chart_data[0].data.length>6){
          chart_data_on([{data: chart_data[0].data.slice(-6,-1)}]);
          nameInput.current.chart.updateSeries([{
            chart_data
          }], false, true);
        }
      }
      
    }
    

  },[chart_data])
  

  useEffect(()=>{
    chart_options_on({
      chart: {
        id: NAME,
        height: '150px',
        type: 'line',
        animations: {
          enabled: false,
          easing: 'linear',
          dynamicAnimation: {
            speed: 1000
          }
        },
        toolbar: {
          show: false
        },
        zoom: {
          enabled: false
        }
      },
      annotations: {
        yaxis: []
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        curve: 'smooth'
      },
      title: props.TYPE==='DG'?{}:{
        text: NAME,
        align: 'center',
        margin: 0,
        offsetX: 0,
        offsetY: 12,
        floating: false,
        style: {
          fontSize:  '14px',
          fontWeight:  'bold',
          fontFamily:  undefined,
          color:  '#263238'
        },
      }, 
      grid: {
        padding: {
            top: 4,
            right: 10,
            bottom: 4,
            left: 4
        },
      }, 
      markers: {
        size: 0
      },
      xaxis: {
        type: 'datetime',
        labels: {
          show: true,
          rotate: -45,
          rotateAlways: false,
          hideOverlappingLabels: true,
          showDuplicates: false,
          trim: false,
          minHeight: undefined,
          maxHeight: 40,
          style: {
              colors: [],
              fontSize: '10px',
              fontFamily: 'Helvetica, Arial, sans-serif',
              fontWeight: 400,
              cssClass: 'apexcharts-xaxis-label',
          },
          offsetX: 0,
          offsetY: 0,
          formatter: (value) => { 
            let tmpS = 'test'
            if(value)
            {
              if(props.TYPE==='DG')
                tmpS = (new Date(value * 1000).toISOString().substr(11, 8));
              else
                tmpS = (value<720?'AM ':'PM ')+(new Date(value * 60000).toISOString().substr(11, 5));
            }
              
            return tmpS;
          },
        },
      },
      yaxis: {
        labels: {
          show: true,
          align: 'right',
          minWidth: 0,
          maxWidth: 30,
          style: {
              colors: [],
              fontSize: '10px',
              fontFamily: 'Helvetica, Arial, sans-serif',
              fontWeight: 400,
              cssClass: 'apexcharts-yaxis-label',
          },
          offsetX: 0,
          offsetY: 0,
          rotate: 0,
          formatter: (value) => { 
            let tmpS = (value % 1 === 0)?value:value.toFixed(2) ;
            return tmpS
          },
        }
      },
      
      legend: {
        show: false
      },
    });
  },[])

      
  

  return (
    <div id={NAME}>
      <Chart className="StaticChartCard" ref={nameInput} options={chart_options} series={chart_data} type="line" width={300} height={150} />
    </div>
  );
}

export default LineCharts;
