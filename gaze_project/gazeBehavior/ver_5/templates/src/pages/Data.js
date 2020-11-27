import React from 'react';
import Select from 'react-select';
import axios from 'axios';

import Heatmap from 'components/Heatmap';
import CorrelationMatrix from 'components/CorrelationMatrix';
import ScatterPlot from 'components/ScatterPlot';
import PatchTable from 'components/PatchTable';

const dataProcessingMethods = [
  { value: 'min_max', label: 'min-max' },
  { value: 'z_score', label: 'z-score'}
];

const correlationMethods = [
  { value:'pearson', label: 'Pearson linear' },
  { value:'spearman', label: 'Spearman rank-order' },
  { value:'kendall', label: 'Kendall rank-order' }
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
      selectedCorrelationMethod: null,
      feature_define: [],
      corr_feature_define: [],
      sti_class_define: [],
      scatter_axis: []
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

        // console.log(dataset_options);
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

        // console.log(participants_options);
        this.setState({
          participants: participants_options
        });
      });
  }

  loadFeatureDefine = () =>{
    axios.get(`http://${window.location.hostname}:5000/static/access/feature_define.json?`+Math.random())
      .then(response => {
        let features = [];
        for(let i=0; i<response.data.length; i++){
          features.push(response.data[i]);
        }
        this.setState({
          feature_define: features
        });
    });
  }

  loadSelectedFeatureDefine = () =>{
    // console.log(this.state.corr_feature_define);
    if(this.state.corr_feature_define.length === 0){
      this.setState({
        corr_feature_define: this.state.feature_define
      });

    }else{
      axios.get(`http://${window.location.hostname}:5000/static/access/selected_feature_define.json?`+Math.random())
        .then(response => {
          // console.log(response);
          let selected_feature_define = response.data;
          
          this.setState({
            corr_feature_define: selected_feature_define
          });
      });
    }
    
  }


  loadSPMeanPath = () =>{
    axios.get(`http://${window.location.hostname}:5000/static/access/sp_heatmap_path.json?`+Math.random())
      .then(response => {
        // console.log(response);
        let _path = "http://"+window.location.hostname+":5000"+response.data+"?"+Math.random();
        // console.log("sp heatmap data access path: "+_path);
        this.setState({
          spHeatmapDataURL: _path
        });
      });

    this.loadFeatureDefine();
    this.loadSelectedFeatureDefine();

    axios.get(`http://${window.location.hostname}:5000/static/access/sti_class_define.json?`+Math.random())
      .then(response => {
        let sti_class = [];
        for(let i=0; i<response.data.length; i++){
          sti_class.push(response.data[i]);
        }
        this.setState({
          sti_class_define: sti_class
        });
    });
  }
  
  loadCorrMatrixPath = () =>{
    axios.get(`http://${window.location.hostname}:5000/static/access/corr_matrix_short_path.json?`+Math.random())
      .then(response => {
        // console.log(response);
        let _path = "http://"+window.location.hostname+":5000"+response.data+"?"+Math.random();
        // console.log("correlation data access path: "+_path);
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

        // console.log(filter_options);
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

  loadScatterAxis = () =>{
    axios.get(`http://${window.location.hostname}:5000/static/access/scatter_axis.json?`+Math.random())
      .then(response => {
        // console.log(response);
        let _axis = response.data;
        
        this.setState({
          scatter_axis: _axis
        });
    });
  }

  // generateScatterData = () =>{
  //   axios.post(`http://${window.location.hostname}:5000/api/scatter/generatedata`, _data)
  //     .then(response => {
  //       if (response.data.status === 'success') {
  //           // alert('data columns changed');
  //           console.log('data columns changed');
  //       } else if (response.data.status === 'failed') {
  //           alert(`Failed change data columns - ${response.data.reason}`);
  //       }
  //     }).catch(error => {
  //       alert(`Error - ${error.message}`);
  //   });
  // }

  

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
          // console.log(response.data);
          this.loadCorrMatrixPath();
        } else if (response.data.status === 'failed') {
          alert(`Failed to load data - ${response.data.reason}`);
        }
      }).catch(error => {
        alert(`Error - ${error.message}`);
      });

    this.loadFeatureDefine();

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
  }

  cMethodChange = selectedCorrelationMethod => {
    this.setState({selectedCorrelationMethod});
    
    const data = new FormData();
    data.set('processing', this.state.selectedProcessMethod.value);
    data.set('correlation', selectedCorrelationMethod.value);
    axios.post(`http://${window.location.hostname}:5000/api/corr/process`, data)
    .then(response => {
      if (response.data.status === 'success') {
        alert('Data pre-processing and correlation methods aplied');
        this.loadCorrMatrixPath();
      } else if (response.data.status === 'failed') {
        alert(`Failed apply data pre-processing and correlation methods - ${response.data.reason}`);
      }
    }).catch(error => {
      alert(`Error - ${error.message}`);
    });

    // load selected features define
    this.loadSelectedFeatureDefine();
  }

  render() {
    const { datasetList, participants, fixationFilters, selectedDataset, spHeatmapDataURL, corrMatDataURL, selectedParticipant, selectedFilter, selectedProcessMethod, selectedCorrelationMethod, feature_define, sti_class_define, scatter_axis, corr_feature_define } = this.state;

    return (
      <>
        <div className="page-header">
          <h2>Temp Title</h2>
        </div>

        <form onSubmit={this.onSubmit}>
          <div className="page-section select-data">
            <Select 
              value={selectedDataset}
              onChange={this.datasetChange}
              options={datasetList}
              placeholder="Stimulus Dataset"
            />
          </div>
          
          {participants.length > 0 &&
            <div className="page-section select-participant">
              <Select 
                value={selectedParticipant}
                onChange={this.participantChange}
                options={participants}
                placeholder="Participant data"
              />
            </div>
          }

          <div className="page-section select-filter">
            <Select 
              value={selectedFilter}
              onChange={this.filterChange}
              options={fixationFilters}
              placeholder="Eye movement event filter"
            />
          </div>

          <div className="page-section button-wrapper">
            <button className="submit-button">Load</button>
          </div>
        </form>

        {spHeatmapDataURL.length > 0 &&
          <div id="heat" className="page-section heatmap">
            <Heatmap 
              width={400}
              height={400}
              dataURL={spHeatmapDataURL}
              FEATURE_DEFINE={feature_define}
              STI_CLASS_DEFINE={sti_class_define}
            />
          </div>
        }

        {spHeatmapDataURL.length > 0 &&
          <div className="page-section select-process">
            <Select
              value={selectedProcessMethod}
              onChange={this.pMethodChange}
              options={dataProcessingMethods}
              placeholder="Data processing"
            />
          </div>
        }

        {spHeatmapDataURL.length > 0 &&
          <div className="page-section select-correlation">
            <Select
              value={selectedCorrelationMethod}
              onChange={this.cMethodChange}
              options={correlationMethods}
              placeholder="Correlation method"
            />
          </div>
        }

        {corrMatDataURL.length > 0 &&
          <div id="corr" className="page-section correlation">
            <CorrelationMatrix 
              width={400}
              height={400}
              dataURL={corrMatDataURL}
              features={corr_feature_define}
              onAxisChanged={this.loadScatterAxis}
            />
          </div>  
        }

        
        <div className="page-section">
          <ScatterPlot
            width={450}
            height={400}
            axis={scatter_axis}
            dataURL={`http://${window.location.hostname}:5000/static/access/scatter_data.csv?`+Math.random()}
          />
        </div>
        

        <div className="page-section">
          <PatchTable />
        </div>
        
      </>
    );
  }
}

export default Data;
