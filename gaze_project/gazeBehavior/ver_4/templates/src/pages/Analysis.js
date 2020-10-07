import React from 'react';
import VisImage from 'components/VisImage';
import LineChart from 'components/LineChart';
// import SurfacePlot from 'components/SurfacePlot';
import axios from 'axios';

class Analysis extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      stimulusPath: "",
      // powerSpectra: {},
      rawGazeData: [],
      fixationData: [],
      rawRndData: [],
      lineChartData: []
    };
  }
  
  // dataFromFormular = func => {
  //   const output = [];
  //   for (let x = -20; x < 20; x++) {
  //     const f0 = [];
  //     output.push(f0);
  //     for (let y = -20; y < 20; y++)
  //       f0.push(func(x, y));
  //   }
  //   return output;
  // }

  componentDidMount() {
    axios.get(`http://${window.location.hostname}:5000/static/output/selected_stimulus_path.json`)
      .then(response => {
        this.setState({
          stimulusPath: 
            response.data
        });
      });
    // axios.get(`http://${window.location.hostname}:5000/static/output/power_gaze.json`)
    //   .then(response => {
    //     this.setState({
    //       powerSpectra: [
    //         /*this.dataFromFormular((x, y) =>
    //           Math.sin(Math.sqrt(x * x + y * y) / 5 * Math.PI) * 50),*/
    //         this.dataFromFormular((x, y) =>
    //           response.data[(x + 20) * 40 + (y + 20)] * 1000),
    //         this.dataFromFormular((x, y) =>
    //           Math.cos(x / 15 * Math.PI) * Math.cos(y / 15 * Math.PI) * 60 + Math.cos(x / 8 * Math.PI) * Math.cos(y / 10 * Math.PI) * 40),
    //         this.dataFromFormular((x, y) =>
    //           -(Math.cos(Math.sqrt(x * x + y * y) / 6 * Math.PI) + 1) * 300 / (Math.pow(x * x + y * y + 1, 0.3) + 1) + 50)
    //       ]
    //     });
    //   });
    axios.get(`http://${window.location.hostname}:5000/static/output/selected_fixation.json`)
      .then(response => {
        // var _data = response.data;
        // var processedData = [];
        // for(var i=0; i<_data.length; i++){
        //   processedData.push([parseFloat(_data[i][1]), parseFloat(_data[i][2])]);
        // }
        //console.log(processedData);
        this.setState({
          rawGazeData: 
            //processedData
            response.data
        });
      });
    axios.get(`http://${window.location.hostname}:5000/static/output/selected_raw_random.json`)
      .then(response => {
        this.setState({
          rawRndData:
            response.data
        });
      });
    // axios.get('https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_IC.csv')
    axios.get(`http://${window.location.hostname}:5000/static/output/selected_raw_gaze.json`)
      .then(response => {
        // CSV to object
        // const data = [];
        // const rows = response.data.split('\n');
        // rows[0] = rows[0].split(',');
        // for (let i = 1; i < rows.length-1; i++) {
        //   const row = {};
        //   rows[i].split(',').forEach((value, index) => {
        //     row[rows[0][index]] = value;
        //   });
        //   data.push(row);
        // }
        console.log(response.data);
        const pData = [];
        const data = response.data;
        var tVal = [];
        var pre_t = -1;
        var tCount = 0;
        for (let i=0; i<data.length; i++){
          var cur_t = data[i][0];
          if(pre_t === -1){
            pre_t = cur_t;
          }
          if(pre_t !== cur_t){
            tVal.push(tCount);
            tCount = 0;
          }
          pre_t = cur_t;
          tCount++;
        }
        tVal.push(tCount);
        console.log(tVal);
        var velocity = [];
        var tValIdx = 0;
        var tValCount = tVal[tValIdx];
        for (let i=0; i<data.length; i++){
          var _ft = 1/40;
          var _vel = _ft;
          if(tValCount === 0){
            tValIdx++;
            tValCount = tVal[tValIdx];
          }
          _vel = _ft/tVal[tValIdx];
          velocity.push(_vel);
          tValCount--;
        }
        
        for (let i=0; i<data.length; i++) {
          var row = {
            x: i+1,
            y: data[i][1],
            v: velocity[i]
          }
          pData.push(row);
        }
        console.log(pData);
        this.setState({
          lineChartData:
            pData
        });
      });
  }

  render() {
    // const { stimulusPath, powerSpectra, rawGazeData, rawRndData } = this.state;
    const { stimulusPath, rawGazeData, rawRndData, lineChartData } = this.state;
    console.log(rawGazeData);
    return (
      <>
        <div className="page-header">
          <h1>Analysis</h1>
        </div>

        <div className="page-section feature-type">
          <h2>Feature type-stimulus-eye_movement_data</h2>
          <div className="stimulus-wrapper">
            <VisImage
              width="960" height="auto"
              image={`http://${window.location.hostname}:5000${stimulusPath}`}
              circles={rawGazeData}
            />
          </div>
          <br></br>
          <div className="stimulus-wrapper">
            <VisImage
              width="960" height="auto"
              image={`http://${window.location.hostname}:5000${stimulusPath}`}
              circles={rawRndData}
            />
          </div>
        </div>

        <div className="page-section feature-type">
          <div>
            <LineChart
              width="500" height="300"
              data={lineChartData}
            />
          </div>
        </div>

        {/* <div className="page-section feature-type">
          <h2>Power specta</h2>
          <div className="power-spectra-left">
            <div className="power-spectra-wrapper">
              <SurfacePlot width="300" height="200" data={powerSpectra[0]} />
            </div>
            <div className="power-spectra-wrapper">
              <SurfacePlot width="300" height="200" data={powerSpectra[1]} />
            </div>
          </div>
          <div className="power-spectra-right">
            <SurfacePlot width="300" height="410" data={powerSpectra[2]} />
          </div>
        </div> */}

        <div className="page-section feature-type">
          <h2>Bispectra</h2>
          <div className="bispectra-wrapper"></div>
          <div className="bispectra-wrapper"></div>
          <div className="bispectra-wrapper"></div>
        </div>
        
      </>
    );
  }
}

export default Analysis;
