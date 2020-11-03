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
      rawGazeData: [],
      fixations: [],
      rndFixations: [],
      rawRndData: [],
      lineChartData: []
    };
  }
  
  dataLoad = () => {
    axios.get(`http://${window.location.hostname}:5000/static/output/selected_stimulus_path.json?`+Math.random())
      .then(response => {
        // console.log(response.data);
        this.setState({
          stimulusPath: 
            response.data
        });
      });
    axios.get(`http://${window.location.hostname}:5000/static/output/selected_fixation.json?`+Math.random())
      .then(response => {
        var _data = response.data;
        var _fixs = [];
        for(var i=0; i<_data.length; i++){
          _fixs.push([_data[i][0], _data[i][1]]);
        }
        // console.log(response.data);
        // console.log(_fixs);
        this.setState({
          fixations: 
            _fixs
            // response.data
        });
      });
    axios.get(`http://${window.location.hostname}:5000/static/output/selected_raw_random.json?`+Math.random())
      .then(response => {
        var _data = response.data;
        var _rndFixs = [];
        for(var i=0; i<_data.length; i++){
          _rndFixs.push([_data[i][0], _data[i][1]]);
        }
        // console.log(response.data);
        // console.log(_rndFixs);
        this.setState({
          rndFixations:
            // response.data
            _rndFixs
        });
      });
    axios.get(`http://${window.location.hostname}:5000/static/output/selected_raw_gaze.json?`+Math.random())
      .then(response => {
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
        // console.log(tVal);
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
        // console.log(pData);
        this.setState({
          lineChartData:
            pData
        });
      });
      this.forceUpdate();
  }

  componentDidMount() {
    this.dataLoad();
  }


  render() {
    const { stimulusPath, fixations, rndFixations, lineChartData } = this.state;
    console.log(fixations);
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
              circles={fixations}
            />
          </div>
          <br></br>
          <div className="stimulus-wrapper">
            <VisImage
              width="960" height="auto"
              image={`http://${window.location.hostname}:5000${stimulusPath}`}
              circles={rndFixations}
            />
          </div>
        </div>

        <div className="page-section feature-type">
          <div>
            <LineChart
              width="500" height="300"
              data={lineChartData}
              onVelocityChanged={this.dataLoad}
            />
          </div>
        </div>

        {/* <div className="page-section feature-type">
          <h2>Bispectra</h2>
          <div className="bispectra-wrapper"></div>
          <div className="bispectra-wrapper"></div>
          <div className="bispectra-wrapper"></div>
        </div> */}
        
      </>
    );
  }
}

export default Analysis;
