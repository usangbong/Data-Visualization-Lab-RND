import React from 'react';
import Select from 'react-select';
import axios from 'axios';

import Heatmap from 'components/Heatmap';
import CorrelationMatrix from 'components/CorrelationMatrix';

const dataProcessingMethods = [
  { value:'min_max', label: 'min-max' },
  { value: 'z_score', label: 'z-score'}
];

class Data extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      datasetList: [],
      fixationFilters: [],
      participants: [],
      featureTypes: [],
      stimulusTypes: [],
      spHeatmapDataURL: "",
      corrMatDataURL: "",
      selectedDataset: null,
      selectedParticipant: null,
      selectedFilter: null,
      selectedProcessMethod: null,
    };
  }

  loadDatasetList = () =>{
    axios.get(`http://${window.location.hostname}:5000/static/dataset.csv?`+Math.random())
      .then(response => {
        // console.log(response.data);
        let dataset_options = [];

        var _val = 0;
        for (let value of response.data.split('\n')){
          if(value.length>0){
            var _d = {
              "value": value.replace('\r', ''),
              "label": value.replace('\r', '')
            };
            dataset_options.push(_d);
            _val++;
          }
        }

        console.log(dataset_options);
        this.setState({
          datasetList: dataset_options
        });
      });
  }

  loadParticipantsList = dataName => {
    axios.get(`http://${window.location.hostname}:5000/static/data/${dataName}/participants.csv?`+Math.random())
      .then(response => {
        // console.log(response.data);
        let participants_options = [];

        for (let value of response.data.split('\n')){
          if(value.length>0){
            var _d = {
              "value": value.replace('\r', ''),
              "label": value.replace('\r', '')
            };
            participants_options.push(_d);
          }
        }

        console.log(participants_options);
        this.setState({
          participants: participants_options
        });
      });
  }

  loadSPMeanPath = () =>{
    axios.get(`http://${window.location.hostname}:5000/static/access/sp_heatmap_path.json?`+Math.random())
      .then(response => {
        // console.log(response);
        let _path = "http://"+window.location.hostname+":5000"+response.data;
        console.log("sp heatmap data access path: "+_path);
        this.setState({
          spHeatmapDataURL: _path
        });
      });
  }
  
  loadCorrMatrixPath = () =>{
    axios.get(`http://${window.location.hostname}:5000/static/access/corr_matrix_short_path.json?`+Math.random())
      .then(response => {
        // console.log(response);
        let _path = "http://"+window.location.hostname+":5000"+response.data;
        console.log("correlation data access path: "+_path);
        this.setState({
          corrMatDataURL: _path
        });
      });
  }

  loadFixationFilters = () =>{
    axios.get(`http://${window.location.hostname}:5000/static/fixation_filters.csv?`+Math.random())
      .then(response => {
        // console.log(response.data);
        let filter_options = [];

        for (let value of response.data.split('\n')){
          if(value.length>0){
            var _d = {
              "value": value.replace('\r', ''),
              "label": value.replace('\r', '')
            };
            filter_options.push(_d);
          }
        }

        console.log(filter_options);
        this.setState({
          fixationFilters: filter_options
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
    this.loadFixationFilters();
  }

  onDataChanged = e => {
    const dataName = e.currentTarget.value;
    this.loadFeatureTypes(dataName);
    this.loadStimulusTypes(dataName);
  }

  

  onSubmit = e => {
    e.preventDefault();
    
    const data = new FormData(e.target);
    data.set('dataset', this.state.selectedDataset.value);
    data.set('participant', this.state.selectedParticipant.value);
    data.set('filter', this.state.selectedFilter.value);

    axios.post(`http://${window.location.hostname}:5000/api/gaze_data/submit`, data)
      .then(response => {
        if (response.data.status === 'success') {
          this.loadSPMeanPath();
          alert('Data loaded');
          console.log(response.data);
          this.loadCorrMatrixPath();
        } else if (response.data.status === 'failed') {
          alert(`Failed to load data - ${response.data.reason}`);
        }
      }).catch(error => {
        alert(`Error - ${error.message}`);
      });
  }

  datasetChange = selectedDataset => {
    this.setState({selectedDataset});
    // console.log(selectedDataset.value);
    this.loadParticipantsList(selectedDataset.value);
  };

  participantChange = selectedParticipant => {
    this.setState({selectedParticipant});
    // console.log(selectedParticipant.value);
  }

  filterChange = selectedFilter => {
    this.setState({selectedFilter});
    // console.log(selectedFilter.value);
  };

  pMethodChange = selectedProcessMethod => {
    this.setState({selectedProcessMethod});
    
    const data = new FormData();
    data.set('processing', selectedProcessMethod.value);
    axios.post(`http://${window.location.hostname}:5000/api/corr/process`, data)
    .then(response => {
      if (response.data.status === 'success') {
        alert('Data pre-processing aplied');
        this.loadCorrMatrixPath();
      } else if (response.data.status === 'failed') {
        alert(`Failed data pre-processing - ${response.data.reason}`);
      }
    }).catch(error => {
      alert(`Error - ${error.message}`);
    });
  }

  render() {
    const { datasetList, participants, fixationFilters, selectedDataset, spHeatmapDataURL, corrMatDataURL, selectedParticipant, selectedFilter, selectedProcessMethod } = this.state;

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
              onChange={this.datasetChange}
              options={datasetList}
              placeholder="Select dataset"
            />
          </div>
          
          {participants.length > 0 &&
            <div className="page-section select-participant">
              <Select 
                value={selectedParticipant}
                onChange={this.participantChange}
                options={participants}
                placeholder="Select participant data"
              />
            </div>
          }

          <div className="page-section select-filter">
            <Select 
              value={selectedFilter}
              onChange={this.filterChange}
              options={fixationFilters}
              placeholder="Select eye movement event filter"
            />
          </div>

          <div className="page-section button-wrapper">
            <button className="submit-button">Load</button>
          </div>
        </form>

        {spHeatmapDataURL.length > 0 &&
          <div id="heat">
            <Heatmap 
              dataURL={spHeatmapDataURL}
            />
          </div>
        }

        <div className="page-section select-process">
          <Select
            value={selectedProcessMethod}
            onChange={this.pMethodChange}
            options={dataProcessingMethods}
            placeholder="Select data pre-processing method"
          />
        </div>


        {corrMatDataURL.length > 0 &&
          <div id="corr">
            <CorrelationMatrix 
              dataURL={corrMatDataURL}
            />
          </div>  
        }
      </>
    );
  }
}

export default Data;
