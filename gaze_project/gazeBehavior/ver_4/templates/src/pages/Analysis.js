import React from 'react';
import VisImage from 'components/VisImage';
import SurfacePlot from 'components/SurfacePlot';
import axios from 'axios';

class Analysis extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      stimulusPath: "",
      powerSpectra: {},
      rawGazeData: [],
      rawRndData: []
    };
  }
  
  dataFromFormular = func => {
    const output = [];
    for (let x = -20; x < 20; x++) {
      const f0 = [];
      output.push(f0);
      for (let y = -20; y < 20; y++)
        f0.push(func(x, y));
    }
    return output;
  }

  componentDidMount() {
    axios.get(`http://${window.location.hostname}:5000/static/output/stimulus_path.json`)
      .then(response => {
        this.setState({
          stimulusPath: 
            response.data
        });
      });
    axios.get(`http://${window.location.hostname}:5000/static/output/power_gaze.json`)
      .then(response => {
        this.setState({
          powerSpectra: [
            /*this.dataFromFormular((x, y) =>
              Math.sin(Math.sqrt(x * x + y * y) / 5 * Math.PI) * 50),*/
            this.dataFromFormular((x, y) =>
              response.data[(x + 20) * 40 + (y + 20)] * 1000),
            this.dataFromFormular((x, y) =>
              Math.cos(x / 15 * Math.PI) * Math.cos(y / 15 * Math.PI) * 60 + Math.cos(x / 8 * Math.PI) * Math.cos(y / 10 * Math.PI) * 40),
            this.dataFromFormular((x, y) =>
              -(Math.cos(Math.sqrt(x * x + y * y) / 6 * Math.PI) + 1) * 300 / (Math.pow(x * x + y * y + 1, 0.3) + 1) + 50)
          ]
        });
      });
    axios.get(`http://${window.location.hostname}:5000/static/output/fixation.json`)
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
    axios.get(`http://${window.location.hostname}:5000/static/output/raw_random.json`)
      .then(response => {
        this.setState({
          rawRndData:
            response.data
        });
      });
  }

  render() {
    const { stimulusPath, powerSpectra, rawGazeData, rawRndData } = this.state;
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
        </div>

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
