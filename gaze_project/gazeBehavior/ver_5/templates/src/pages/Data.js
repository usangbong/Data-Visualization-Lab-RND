import React from 'react';
import Select from 'react-select';
import axios from 'axios';

class Data extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      datasetList: [],
      fixationFilters: [],
      participants: [],
      featureTypes: [],
      stimulusTypes: [],
      selectedDataset: null,
      selectedParticipant: null,
      selectedFilter: null
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
    data.set('dataset', this.state.selectedDataset);
    data.set('participant', this.state.selectedParticipant);
    data.set('filter', this.state.selectedFilter);

    axios.post(`http://${window.location.hostname}:5000/api/gaze_data/submit`, data)
      .then(response => {
        if (response.data.status === 'success') {
          alert('Data loaded');
          console.log(response.data);
        } else if (response.data.status === 'failed') {
          alert(`Failed to load data - ${response.data.reason}`);
        }
      }).catch(error => {
        alert(`Error - ${error.message}`);
      });
  }

  datasetChange = d => {
    const selected = d.value;
    this.setState({selectedDataset: selected});
    console.log(this.state.selectedDataset);
    this.loadParticipantsList(selected);
  };

  participantChange = p => {
    const selected = p.value;
    this.setState({selectedParticipant: selected});
    console.log(this.state.selectedParticipant);
  }

  filterChange = f => {
    const selected = f.value;
    this.setState({selectedFilter: selected});
    console.log(this.state.selectedFilter);

  };

  render() {
    const { datasetList, participants, fixationFilters, selectedDataset, selectedParticipant, selectedFilter } = this.state;

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
      </>
    );
  }
}

export default Data;
