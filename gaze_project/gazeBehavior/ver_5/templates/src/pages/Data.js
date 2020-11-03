import React from 'react';
import Select from 'react-select';
import axios from 'axios';

class Data extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      datasetList: [],
      featureTypes: [],
      stimulusTypes: [],
      selectedDataset: null,
    };
  }


  loadDatasetList = () =>{
    axios.get(`http://${window.location.hostname}:5000/static/dataset.csv?`+Math.random())
      .then(response => {
        console.log(response.data);
        let options = [];

        var _val = 0;
        for (let value of response.data.split('\n')){
          if(value.length>0){
            var _d = {
              "value": value.replace('\r', ''),
              "label": value.replace('\r', '')
            };
            options.push(_d);
            _val++;
          }
        }

        // for(var i=0; i<response.data.length; i++){
        //   var _d = {
        //     "value": i,
        //     "label": response.data[i]
        //   };
        //   options.push(_d);
        // }
        console.log(options);
        this.setState({
          datasetList: options
        });
      });
  }

  loadFeatureTypes = dataName => {
    axios.get(`http://${window.location.hostname}:5000/static/data/${dataName}/feature_types.csv`)
      .then(response => {
        const featureTypes = [];
        for (let value of response.data.split('\n')) {
          if (value.length > 0)
            featureTypes.push(value.replace('\r', ''));
        }
        this.setState({
          featureTypes: featureTypes
        });
      });
  }

  loadStimulusTypes = dataName => {
    axios.get(`http://${window.location.hostname}:5000/static/data/${dataName}/stimulus_types.csv`)
      .then(response => {
        const stimulusTypes = [];
        for (let value of response.data.split('\n')) {
          if (value.length > 0)
            stimulusTypes.push(value.replace('\r', ''));
        }
        this.setState({
          stimulusTypes: stimulusTypes
        });
      });
  }

  componentDidMount() {
    this.loadDatasetList();
  }

  onDataChanged = e => {
    const dataName = e.currentTarget.value;
    this.loadFeatureTypes(dataName);
    this.loadStimulusTypes(dataName);
  }

  onSubmit = e => {
    e.preventDefault();
    
    const data = new FormData(e.target);
    const featureTypes = [];
    for (let i = 0; i < this.state.featureTypes.length; i++) {
      if (data.get(`feature-type-${i}`) !== null)
        featureTypes.push(data.get(`feature-type-${i}`));
    }
    const stimulusClasses = [];
    for (let i=0; i<this.state.stimulusTypes.length; i++){
      if (data.get(`stimulus-type-${i}`) !== null)
        stimulusClasses.push(data.get(`stimulus-type-${i}`));
    }

    data.set('feature-types', featureTypes);
    data.set('stimulus-classes', stimulusClasses);

    axios.post(`http://${window.location.hostname}:5000/api/gaze_data/submit`, data)
      .then(response => {
        if (response.data.status === 'success') {
          alert('Data loaded');
        } else if (response.data.status === 'failed') {
          alert(`Failed to load data - ${response.data.reason}`);
        }
      }).catch(error => {
        alert(`Error - ${error.message}`);
      });
  }

  datasetChange = selectedDataset => {
    this.setState({selectedDataset});
    this.loadFeatureTypes(selectedDataset.value);
    this.loadStimulusTypes(selectedDataset.value);
  };

  render() {
    const { datasetList, featureTypes, stimulusTypes, selectedDataset } = this.state;

    
    return (
      <>
        <div className="page-header">
          <h1>Select Data</h1>
        </div>

        <form onSubmit={this.onSubmit}>
          <div className="page-section select-data">
            <h2>Dataset</h2>
            <Select 
              value={selectedDataset}
              onChange = {this.datasetChange}
              options={datasetList}
            />
            {/* <ul>
              <li>
                <input type="radio" id="data-mit300" name="data-origin" value="mit300" onClick={this.onDataChanged} />
                <label htmlFor="data-mit300">
                  <span>MIT300 dataset</span>
                </label>
              </li>
              <li>
                <input type="radio" id="data-database" name="data-origin" value="database" onClick={this.onDataChanged} />
                <label htmlFor="data-database">
                  <span>Database</span>
                </label>
              </li>
            </ul> */}
          </div>

          {featureTypes.length > 0 &&
            <div className="page-section select-feature-type">
              <h2>Feature Type</h2>
              <ul>
                {featureTypes.map((value, index) =>
                  <li key={index}>
                    <input
                      type="checkbox"
                      id={`feature-type-${index}`}
                      name={`feature-type-${index}`}
                      className="feature-type-item"
                      value={value}
                    />
                    <label htmlFor={`feature-type-${index}`}>
                      <span>{value}</span>
                    </label>
                  </li>
                )}
              </ul>
            </div>
          }

          {stimulusTypes.length > 0 &&
            <div className="page-section select-stimulus-type">
              <h2>Stimulus Class</h2>
              <ul>
                {stimulusTypes.map((value, index) =>
                  <li key={index}>
                    <input 
                      type="checkbox" 
                      id={`stimulus-type-${index}`}
                      name={`stimulus-type-${index}`}
                      className="stimulus-type-item"
                      value={value} 
                    />
                    <label htmlFor={`stimulus-type-${index}`}>
                      <span>{value}</span>
                    </label>
                  </li>
                )}
              </ul>
            </div>
          }

          <div className="page-section button-wrapper">
            <button className="submit-button">Load</button>
          </div>
        </form>
      </>
    );
  }
}

export default Data;
