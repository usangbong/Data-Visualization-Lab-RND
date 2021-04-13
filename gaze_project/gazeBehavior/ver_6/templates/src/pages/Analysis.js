import React from 'react';
import axios from 'axios';
import Select from 'react-select';
// https://react-select.com/home
import { AlphaPicker, SketchPicker } from 'react-color';
// https://casesandberg.github.io/react-color/#api

import Heatmap from 'components/Heatmap';
import PatchVisualization from 'components/PatchVisualization';
import ScanpathVisualization from 'components/ScanpathVisualization';
import BoxPlot from 'components/BoxPlot';

// import { AgGridColumn, AgGridReact } from 'ag-grid-react';

// import '../../node_modules/ag-grid-enterprise';
// import '../../node_modules/ag-grid-community/dist/styles/ag-grid.css';
// import '../../node_modules/ag-grid-community/dist/styles/ag-theme-alpine.css';
// import { stringToArray } from 'ag-grid-community';

const select_option_dataset = [
  { value:'all', label: 'All Stimulus Dataset' },
  { value:'CAT2000', label: 'CAT2000' },
  { value:'FIGRIM', label: 'FIGRIM' },
  { value:'MIT1003', label: 'MIT1003' }
];

const select_option_scanpathSimilarity = [
  { value:'jd', label: 'Jaccard Coefficient' },
  { value:'dtw', label: 'Dynamic Time Warping' },
  { value:'lcs', label: 'Longest Common Subsequence' },
  { value:'fd', label: 'Frechet Distance' },
  { value:'ed', label: 'Edit (Levenshtein) Distance' }
];

const select_option_useCache = [
  { value:'use', label: 'Use cache file' },
  { value:'not', label: 'Do not use cache file' }
];

const select_option_dataTransformation = [
  { value:'raw', label: 'Raw data' },
  { value:'min_max', label: 'Min-max' },
  { value:'z_score', label: 'z-score' },
  { value:'yeo_johonson', label: 'Yeo-Johonson' },
  { value:'yeo_johonson_min_max', label: 'Yeo-Johonson + Min-max' }
];

const select_option_dimensionReduction = [
  { value:'MDS', label: 'MDS (Multi Dimensional Scaling)' },
  { value:'PCA', label: 'PCA (Principal Component Analysis)' },
  { value:'ICA', label: 'ICA (Independent Component Aanalysis)' },
  { value:'t_SNE', label: 't-SNE (t-Stochastic Neighbor Embedding)' },
  { value:'PLS', label: 'PLS (Partial Least Squares)' }
];

// const select_option_dataClustering = [
//   { value:'random_forest', label: 'RandomForest' },
//   { value:'dbscan', label: 'DBSCAN' },
//   { value:'hdbscan', label: 'hDBSCAN' },
//   { value:'k_means', label: 'k-Means' }
// ];

const select_option_patchImageFlag = [
  { value:'image', label: 'Draw fixated patch images' },
  { value:'box', label: 'Draw only label box' }
];

class Analysis extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      select_stiDataset: [],
      select_semanticClass: [],
      select_stiName: [],
      select_participant: [],
      select_useCache: null,
      select_cacheFile: null,
      select_scanpathSimilarityMetohd: null,
      select_main_scanpath: null,
      select_dataTransformation: null,
      // select_dataClustering: null,
      select_dimensionReduction: null,
      select_patchImageFlag: null,
      select_isDisabled_participant: true,
      select_isDisabled_semanticClass: true,
      select_isDisabled_stiName: true,
      select_isDisabled_scanpathSimilarity: true,
      select_isDisabled_mainScanpath: true,
      select_isDisabled_dataTransformation: true,
      // select_isDisabled_dataClustering: true,
      select_isDisabled_dimensionReduction: true,
      select_isDisabled_useCache: true,
      select_isDisabled_cacheFile: true,
      select_option_participant: [],
      select_option_stiClass: [],
      select_option_stiName: [],
      select_option_mainScanpath: [],
      select_option_cacheFile: [],
      STI_CLASS_LIST: [],
      FEATURE_LIST: [],
      spDataURL: "",
      stiURL: [],
      scanpathList: [],
      alphaPicker_stimulusAlpha: 1,
      alphaPicker_stimulusColor: {},
      tempColor: {r: '255', g: '255', b: '255', a:'1'},
      processingDataColumns: [],
      processingDataList: [],
      rawDataList: [],
      patchDataList: [],
      patchesOnHumanFixationMap: [],
      patchesOutsideHumanFixationMap: [],
    };
  }

  select_onChanged_stiDataset = select_stiDataset =>{
    this.setState({select_stiDataset})
    if(select_stiDataset !== null && select_stiDataset !== undefined){
      // console.log(select_stiDataset);
      var stiDatasetList_str = "";
      for(let i=0; i<select_stiDataset.length; i++){
        if(i==0){
          stiDatasetList_str = stiDatasetList_str+select_stiDataset[i].value
        }else{
          stiDatasetList_str = stiDatasetList_str+"/"+select_stiDataset[i].value
        }
      }
      // console.log(stiDatasetList_str);
      const data = new FormData();
      data.set('stiDataset', stiDatasetList_str);
      axios.post(`http://${window.location.hostname}:5000/api/processing/stiDataset`, data)
      .then(response => {
        // console.log(response);
        let getClassList = response.data.classList;
        let stiClassList = [];
        let optionClassList = [
          { value: 'all', label: 'All semantic class' }
        ];
        for(let i=0; i<getClassList.length; i++){
          var _r = {
            'datasetName': getClassList[i][0],
            'classList': getClassList[i][1]
          }
          for(let j=0; j<_r.classList.length; j++){
            var j_str = j.toString();
            if(j<10){
              j_str = "0"+j.toString();
            }
            var _sc = {
              value: _r.datasetName+"/"+_r.classList[j],
              label: "("+_r.datasetName.charAt(0)+j_str+") "+_r.datasetName+": "+_r.classList[j]
            }
            optionClassList.push(_sc);
          }
          stiClassList.push(_r);
        }
        // console.log(stiClassList);
        // console.log(optionClassList);

        this.setState({
          STI_CLASS_LIST:stiClassList
        });
        

        let getFeatureList = response.data.featureList;
        // console.log(getFeatureList);
        this.setState({
          FEATURE_LIST: getFeatureList
        });
        
        this.setState({
          select_option_stiClass: optionClassList
        });
        this.setState({
          select_isDisabled_semanticClass: false
        })
        
        this.setState({
          spDataURL: `http://${window.location.hostname}:5000/static/__cache__/sp_cvt.csv?`+Math.random()
        });
      }).catch(error => {
        alert(`Error - ${error.message}`);
      });
    }
  }

  select_onChanged_semanticClass = select_semanticClass =>{
    console.log("select_onChanged_semanticClass");
    this.setState({select_semanticClass});
    if(select_semanticClass !== null && select_semanticClass !== undefined){
      let select_semanticClass_str = "";
      for(let i=0; i<select_semanticClass.length; i++){
        // console.log(select_semanticClass);
        if(i==0){
          select_semanticClass_str = select_semanticClass[i].value;
        }else{
          select_semanticClass_str = select_semanticClass_str+"-"+select_semanticClass[i].value;
        }
      }

      const data = new FormData();
      data.set('stiClass', select_semanticClass_str);
      axios.post(`http://${window.location.hostname}:5000/api/processing/loadStimulusNames`, data)
      .then(response => {
        // console.log(response.data.stimulusNames);
        let getStimulusNames = response.data.stimulusNames;
        let stiNamesList = [];
        for(let i=0; i<getStimulusNames.length; i++){
          let splitData = getStimulusNames[i][0].split("/");
          let datasetName = splitData[0];
          let stiClassName = splitData[1];
          let stiFileName = splitData[2];
          let classShortName = "";
          for(let j=0; j<this.state.select_option_stiClass.length; j++){
            let splitSelectOptionClass = this.state.select_option_stiClass[j].value.split("/");
            let _dn = splitSelectOptionClass[0];
            let _cn = "";
            if(splitSelectOptionClass.length == 2){
              _cn = splitSelectOptionClass[1];
            }else if(splitSelectOptionClass.length == 3){
              _cn = splitSelectOptionClass[1]+"/"+splitSelectOptionClass[2];
            }else{
              for(let k=1; k<splitSelectOptionClass.length; k++){
                if(k==1){
                  _cn = _cn + splitSelectOptionClass[k];
                }else{
                  _cn = _cn +"/"+ splitSelectOptionClass[k]
                }
              }
            }
            if(_dn == datasetName && _cn == stiClassName){
              classShortName = this.state.select_option_stiClass[j].label.split(" ")[0];
              break;
            }
          }
          let stiNameOption = {
            value: datasetName+"/"+stiClassName+"/"+stiFileName+"/"+getStimulusNames[i][1]+"_"+getStimulusNames[i][2],
            label: classShortName+" "+stiFileName+ " ("+getStimulusNames[i][1] +"x"+ getStimulusNames[i][2]+")"
          }; 
          stiNamesList.push(stiNameOption);
        }
        this.setState({
          select_option_stiName: stiNamesList
        });
        this.setState({
          select_isDisabled_stiName: false
        });
      }).catch(error => {
        alert(`Error - ${error.message}`);
      });
      
    }
  }

  select_onChanged_stiName = select_stiName =>{
    console.log("select_onChanged_stiName");
    this.setState({select_stiName});
    if(select_stiName !== null && select_stiName !== undefined){
      let stiURLList = [];
      let stiList_str = "";
      for(let i=0; i<select_stiName.length; i++){
        // console.log(select_stiName[i].value);
        let splitValue = select_stiName[i].value.split("/");
        let pathString = splitValue[0] +"/"+ splitValue[1] +"/"+ splitValue[2];
        let stiWidth = parseInt(splitValue[3].split("_")[0]);
        let stiHeight = parseInt(splitValue[3].split("_")[1]);
        let _sURL = {
          url: `http://${window.location.hostname}:5000/static/stimulus/`+pathString,
          width: stiWidth,
          height: stiHeight
        };
        stiURLList.push(_sURL);
        if(i==0){
          stiList_str = pathString;
        }else{
          stiList_str = stiList_str +"-"+ pathString;
        }
      }
      this.setState({
        stiURL: stiURLList
      });
      // console.log(stiURLList);
      // console.log(stiList_str);

      const data = new FormData();
      data.set('stiList', stiList_str);
      axios.post(`http://${window.location.hostname}:5000/api/processing/loadFixationDataList`, data)
      .then(response => {
        // console.log(response.data.participantList);
        let getParticipantList = response.data.participantList;
        // console.log(getParticipantList);
        let participantList = [
          { value:'all', label: 'All Participant data' }
        ];
        for(let i=0; i<getParticipantList.length; i++){
          let _splitdata = getParticipantList[i].split("/")
          var _dataset = _splitdata[0];
          var _class = _splitdata[1];
          var _name = _splitdata[2];
          let pLabel = "";
          for(let j=0; j<this.state.select_option_stiName.length; j++){
            let _split = this.state.select_option_stiName[j].value.split("/");
            let _sd = _split[0];
            let _sc = _split[1];
            let _sn = _split[2].split(".")[0]+"_"+_split[2].split(".")[1];
            if(_sd == _dataset && _class == _sc && _name == _sn){
              pLabel = this.state.select_option_stiName[j].label.split(" ")[0]+" "+_split[2]+": "+_splitdata[3];
              break;
            }
          }
          var _p = {
            value: getParticipantList[i],
            label: pLabel
          };
          participantList.push(_p);
        }
        this.setState({
          select_option_participant: participantList
        });
        this.setState({
          select_isDisabled_participant: false
        });
        
      }).catch(error => {
        alert(`Error - ${error.message}`);
      });
    }
  }

  select_onChanged_participant = select_participant =>{
    console.log("select_onChanged_participant");
    this.setState({select_participant});
    if(select_participant !== null && select_participant !== undefined){
      let allParticipantSelectFlag = false;
      for(let i=0; i<select_participant.length; i++){
        if(select_participant[i].value == "all"){
          allParticipantSelectFlag = true;
          break;
        }
      }
      let selectedParticipant_str = "";
      let strIdx = 0;
      let loadData = select_participant;
      let _select_option_mainScanpath = [];
      if(allParticipantSelectFlag == true){
        strIdx = 1;
        loadData = this.state.select_option_participant;
      }
      for(let i=strIdx; i<loadData.length; i++){
        if(i == strIdx){
          selectedParticipant_str = loadData[i].value;
        }else{
          selectedParticipant_str = selectedParticipant_str +"-"+ loadData[i].value;
        }
        var _opt_mScanpath = {
          value: loadData[i].value,
          label: loadData[i].label
        };
        _select_option_mainScanpath.push(_opt_mScanpath);
      }
      // console.log('_select_option_mainScanpath');
      // console.log(_select_option_mainScanpath);
      this.setState({
        select_option_mainScanpath: _select_option_mainScanpath
      });
      let _mainScanpath_flag = true;
      if(_select_option_mainScanpath !== null && _select_option_mainScanpath !== undefined){
        _mainScanpath_flag = false;
      }else{
        _mainScanpath_flag = true;
      }
      this.setState({
        select_isDisabled_mainScanpath: _mainScanpath_flag
      });
      
      const data = new FormData();
      data.set('participantList', selectedParticipant_str);
      axios.post(`http://${window.location.hostname}:5000/api/processing/genFixationDataList`, data)
      .then(response => {
        // console.log('response.data.fixDataList');
        // console.log(response.data.fixDataList);
        let getFixDataList = response.data.fixDataList;
        let scanpathDataList = [];
        for(let i=0; i<getFixDataList.length; i++){
          let _fixs = getFixDataList[i][1];
          let _id = getFixDataList[i][0][0]+"/"+getFixDataList[i][0][1]+"/"+getFixDataList[i][0][2]+"/"+getFixDataList[i][0][3];
          let _cFixs = [];
          for(let j=0; j<_fixs.length; j++){
            var _f = {
              id: _id+"/"+j,
              clu: 0,
              x: _fixs[j][0],
              y: _fixs[j][1]
            };
            _cFixs.push(_f);
          }
          let _fixData = {
            rId: _id,
            rClu: 0,
            scanpath: _cFixs
          };
          scanpathDataList.push(_fixData);
        }
        // console.log('scanpathDataList');
        // console.log(scanpathDataList);
        this.setState({
          scanpathList: scanpathDataList
        });
        this.setState({
          select_isDisabled_useCache: false
        });
      }).catch(error => {
        alert(`Error - ${error.message}`);
      });

    }
  }

  select_onChanged_mainScanpath = select_main_scanpath =>{
    console.log("select_onChanged_mainScanpath");
    this.setState({select_main_scanpath});
    if(select_main_scanpath !== null && select_main_scanpath !== undefined){
      let select_isDisabled_scanpathSimilarity_flag = true;
      if(this.state.select_participant.length >= 5 || this.state.select_participant[0].value == "all"){
        select_isDisabled_scanpathSimilarity_flag = false;
      }else{
        select_isDisabled_scanpathSimilarity_flag = true;
      }
      this.setState({
        select_isDisabled_scanpathSimilarity: select_isDisabled_scanpathSimilarity_flag
      });

      // console.log(select_main_scanpath);
      let displayedScanpath = this.state.scanpathList;
      let copyScanpathList = [];
      for(let i=0; i<displayedScanpath.length; i++){
        let _fixs = [];
        let _rid = displayedScanpath[i].rId;
        let _rclu = 0;
        for(let j=0; j<displayedScanpath[i].scanpath.length; j++){
          let _clu = 0;
          let _id = displayedScanpath[i].scanpath[j].id;
          let _idWithoutIndex = _id.split("/")[0]+"/"+_id.split("/")[1]+"/"+_id.split("/")[2]+"/"+_id.split("/")[3];
          if(_idWithoutIndex == select_main_scanpath.value){
            _clu = 1;
            _rclu = 1;
          }
          let _f = {
            id: _id,
            clu: _clu,
            x: displayedScanpath[i].scanpath[j].x,
            y: displayedScanpath[i].scanpath[j].y
          };
          _fixs.push(_f);
        }
        let _fixData = {
          rId: _rid,
          rClu: _rclu,
          scanpath: _fixs
        };
        copyScanpathList.push(_fixData);
      }
      // console.log('copyScanpathList');
      // console.log(copyScanpathList);
      this.setState({
        scanpathList: copyScanpathList
      });
    }
  }

  select_onChanged_scanpathSimilarity = select_scanpathSimilarityMetohd =>{
    console.log("select_onChanged_scanpathSimilarity");
    this.setState({select_scanpathSimilarityMetohd});
    if(select_scanpathSimilarityMetohd !== null && select_scanpathSimilarityMetohd !== undefined){
      let selectedScanpathFileList_str = "";
      let _selectedParticipant = this.state.select_participant;
      let _strIdx = 0;
      let _getData = _selectedParticipant;
      for(let i=0; i<_selectedParticipant.length; i++){
        if(_selectedParticipant[i].value == "all"){
          _strIdx = 1;
          _getData = this.state.select_option_participant;
          break;
        }
      }
      for(let i=_strIdx; i<_getData.length; i++){
        if(i==_strIdx){
          selectedScanpathFileList_str = _getData[i].value;
        }else{
          selectedScanpathFileList_str = selectedScanpathFileList_str +"-"+ _getData[i].value;
        }
      }
      // console.log(selectedScanpathFileList_str);
      
      const data = new FormData();
      data.set('scanpathSimilarityMethod', select_scanpathSimilarityMetohd.value);
      data.set('selectedScanpaths', selectedScanpathFileList_str);
      data.set('mainScanpath', this.state.select_main_scanpath.value);
      axios.post(`http://${window.location.hostname}:5000/api/scanpath/calcSimilarity`, data)
      .then(response => {
        let getSSVdata = response.data.scanpathSimilarityValues;
        // console.log('response.data.scanpathSimilarityValues');
        // console.log(getSSVdata);
        // console.log('this.state.scanpathList');
        // console.log(this.state.scanpathList);
        let displayedScanpath = this.state.scanpathList;
        let changedScanpathList = [];
        for(let i=0; i<displayedScanpath.length; i++){
          let _rid = displayedScanpath[i].rId;
          let mainFlag = false;
          let _rclu = displayedScanpath[i].rClue;
          let _tempClu = 0;
          for(let j=0; j<getSSVdata.length; j++){
            if(_rid == getSSVdata[j].main){
              mainFlag = true;
              break;
            }
            if(_rid == getSSVdata[j].target){
              _tempClu = getSSVdata[j].sclu;
              break;
            }
          }
          if(mainFlag == false){
            _rclu = _tempClu;
          }else{
            _rclu = 1;
          }
          let _fixs = [];
          for(let j=0; j<displayedScanpath[i].scanpath.length; j++){
            let _f = {
              id: displayedScanpath[i].scanpath[j].id,
              clu: _rclu,
              x: displayedScanpath[i].scanpath[j].x,
              y: displayedScanpath[i].scanpath[j].y
            };
            _fixs.push(_f);
          }
          let _fixsData = {
            rId: _rid,
            rClu: _rclu,
            scanpath: _fixs
          };
          changedScanpathList.push(_fixsData);
        }
        // console.log('changedScanpathList');
        // console.log(changedScanpathList);
        this.setState({
          scanpathList: changedScanpathList
        });

      }).catch(error => {
        alert(`Error - ${error.message}`);
      });
    }
  }

  select_onChange_useCache = select_useCache =>{
    console.log("select_onChange_useCache");
    this.setState({select_useCache});
    if(select_useCache !== null && select_useCache !== undefined){
      let _cacheFlag = true;
      if(select_useCache.value == 'use'){
        _cacheFlag = true;
        axios.post(`http://${window.location.hostname}:5000/api/clustering/loadCacheList`)
        .then(response => {
          // console.log(response.data);
          let getCacheFileList = response.data.caches;
          let loadedCacheList = [];
          for(let i=0; i<getCacheFileList.length; i++){
            let _c ={
              value: getCacheFileList[i],
              label: getCacheFileList[i]
            };
            loadedCacheList.push(_c);
          }
          this.setState({
            select_option_cacheFile: loadedCacheList
          });
          this.setState({
            select_isDisabled_cacheFile: false
          });
          
        }).catch(error => {
          alert(`Error - ${error.message}`);
        });
      }else{
        _cacheFlag = false;
      }
      this.setState({
        select_isDisabled_dataTransformation: _cacheFlag
      });
      this.setState({
        select_isDisabled_dimensionReduction: _cacheFlag
      });
      this.setState({
        select_isDisabled_cacheFile: true
      });
    }
  }

  select_onChange_cacheFile = select_cacheFile =>{
    console.log("select_onChange_cacheFile");
    this.setState({select_cacheFile});
  }

  run_transformation_clustering = (tMethod, drMethod) =>{
    const data = new FormData();
    data.set('transformationMethod', tMethod);
    data.set('dimensionReductionMethod', drMethod);
    axios.post(`http://${window.location.hostname}:5000/api/clustering/processing`, data)
    .then(response => {
      // console.log(response.data);
      console.log(response.data.dataColumns);
      this.setState({
        processingDataColumns: response.data.dataColumns
      });
      this.setState({
        processingDataList: response.data.processingData
      });
      this.setState({
        rawDataList: response.data.rawData
      });
      
      let getPorcessedDataList = response.data.processingData;
      let unprocessedDataList = this.state.scanpathList;
      
      this.setState({
        patchDataList: getPorcessedDataList
      });

      let onHFMPatches = [];
      let outsideHFMPatches = [];
      for(let i=0; i<getPorcessedDataList.length; i++){
        let _label = getPorcessedDataList[i][3];
        if(_label == 0){
          // label 0: outside
          outsideHFMPatches.push(getPorcessedDataList[i]);
        }else{
          // label 1: on
          onHFMPatches.push(getPorcessedDataList[i]);
        }
      }
      console.log("onHFMPatches");
      console.log(onHFMPatches);
      console.log("outsideHFMPatches");
      console.log(outsideHFMPatches);
      this.setState({
        patchesOnHumanFixationMap: onHFMPatches
      });
      this.setState({
        patchesOutsideHumanFixationMap: outsideHFMPatches
      });
      
    }).catch(error => {
      alert(`Error - ${error.message}`);
    });
  }

  select_onChanged_dataTransformation = select_dataTransformation =>{
    console.log("select_onChanged_dataTransformation");
    this.setState({select_dataTransformation});
    if(select_dataTransformation !== null && select_dataTransformation !== undefined && this.state.select_dimensionReduction !== null && this.state.select_dimensionReduction !== undefined){
      this.run_transformation_clustering(select_dataTransformation.value, this.state.select_dimensionReduction.value);
    }
  }

  select_onChanged_dimensionReduction = select_dimensionReduction =>{
    console.log("select_onChanged_dimensionReduction");
    this.setState({select_dimensionReduction});
    if(select_dimensionReduction !== null && select_dimensionReduction !== undefined && this.state.select_dataTransformation !== null && this.state.select_dataTransformation !== undefined){
      this.run_transformation_clustering(this.state.select_dataTransformation.value, select_dimensionReduction.value);
    }
  }

  // select_onChanged_dataClustering = select_dataClustering =>{
  //   this.setState({select_dataClustering});
  //   if(select_dataClustering !== null && select_dataClustering !== undefined && this.state.select_dataTransformation !== null && this.state.select_dataTransformation !== undefined){
  //     console.log("select_onChanged_dataClustering");
  //     this.run_transformation_clustering(this.state.select_dataTransformation.value, select_dataClustering.value);
  //   }
  // }

  select_onChanged_patchImageFlag = select_patchImageFlag =>{
    console.log("select_onChanged_patchImageFlag");
    this.setState({select_patchImageFlag});
  }

  alphaPicker_onChange_stimulusAlpha = (color) =>{
    this.setState({alphaPicker_stimulusColor: color.rgb});
    this.setState({
      alphaPicker_stimulusAlpha: color.rgb.a
    });
  }

  tempFunction = (color) =>{
    this.setState({tempColor:color.rgb});
  }

  render() {
    // data filter select
    const { select_stiDataset, select_participant, select_semanticClass, select_stiName } = this.state;
    const { select_option_participant, select_option_stiClass, select_option_stiName } = this.state;
    const { select_isDisabled_participant, select_isDisabled_semanticClass, select_isDisabled_stiName } = this.state;
    // sp heatmap
    const { spDataURL, FEATURE_LIST, STI_CLASS_LIST} = this.state;
    // scanpath visualization
    const { stiURL, scanpathList } = this.state;
    const { alphaPicker_stimulusColor, alphaPicker_stimulusAlpha, tempColor } = this.state;
    // scanpath similarity
    const { select_main_scanpath, select_isDisabled_mainScanpath, select_option_mainScanpath, select_scanpathSimilarityMetohd, select_isDisabled_scanpathSimilarity } = this.state;
    // patch clustering
    const { select_useCache, select_cacheFile, select_option_cacheFile, select_dataTransformation, select_dimensionReduction } = this.state;
    // const { select_dataClustering, select_isDisabled_dataClustering } = this.state;
    const { select_isDisabled_useCache, select_isDisabled_cacheFile, select_isDisabled_dataTransformation, select_isDisabled_dimensionReduction } = this.state;
    const { patchDataList, select_patchImageFlag } = this.state;
    // saliency features visualization
    const { patchesOnHumanFixationMap, patchesOutsideHumanFixationMap } = this.state;

    return (
    <>
      {/* data filter */}
      <div className="inputBoxWrap">
        <div className="page-header">
          <div id="logo"></div><div><h3>Visual Attention Analysis System</h3></div>
        </div>
        <div className="section-header">
          <h4> Analysis of Spatial Variance </h4>
        </div>
        <Select 
          value={select_stiDataset}
          isMulti
          options={select_option_dataset}
          onChange={this.select_onChanged_stiDataset}
          className="basic-multi-select"
          classNamePrefix="select"
          placeholder="Select stimulus dataset"
        />
        { spDataURL.length != 0 &&
        <div id="heat" className="page-section heatmap">
          <Heatmap 
            width={400}
            height={650}
            dataURL={spDataURL}
            FEATURE_DEFINE={FEATURE_LIST}
            STI_CLASS_DEFINE={STI_CLASS_LIST}
          />
        </div>
        }
        <div className="section-header">
          <h4> Data Filter </h4>
        </div>
        <Select 
          value={select_semanticClass}
          isDisabled={select_isDisabled_semanticClass}
          isMulti
          options={select_option_stiClass}
          onChange={this.select_onChanged_semanticClass}
          className="basic-multi-select"
          classNamePrefix="select"
          placeholder="Select semantic class"
        />
        <Select 
          value={select_stiName}
          isDisabled={select_isDisabled_stiName}
          isMulti
          options={select_option_stiName}
          onChange={this.select_onChanged_stiName}
          className="basic-multi-select"
          classNamePrefix="select"
          placeholder="Select visual stimulus"
        />
        <Select 
          value={select_participant}
          isDisabled={select_isDisabled_participant}
          isMulti
          options={select_option_participant}
          onChange={this.select_onChanged_participant}
          className="basic-multi-select"
          classNamePrefix="select"
          placeholder="Select observer ID"
        />
        
        <div className="section-header">
          <h4> Analysis Settings </h4>
        </div>
        <Select
          value={select_main_scanpath}
          isDisabled={select_isDisabled_mainScanpath}
          options={select_option_mainScanpath}
          onChange={this.select_onChanged_mainScanpath}
          placeholder="Select scanpath for calculation similarity"
        />
        <Select
          value={select_scanpathSimilarityMetohd}
          isDisabled={select_isDisabled_scanpathSimilarity}
          options={select_option_scanpathSimilarity}
          onChange={this.select_onChanged_scanpathSimilarity}
          placeholder="Select scanpath similarity calculation method"
        />
        <Select
          value={select_useCache}
          isDisabled={select_isDisabled_useCache}
          options={select_option_useCache}
          onChange={this.select_onChange_useCache}
          placeholder="Use cache file or not"
        />
        { select_option_cacheFile.length > 0 && select_useCache.value == "use" &&
        <div>
          <Select
            value={select_cacheFile}
            isDisabled={select_isDisabled_cacheFile}
            options={select_option_cacheFile}
            onChange={this.select_onChange_cacheFile}
            placeholder="Select cache file"
          />
        </div>
        }
        { select_useCache !== null && select_useCache !== undefined && select_useCache.value == "not" &&
        <div>
        <Select
          value={select_dataTransformation}
          isDisabled={select_isDisabled_dataTransformation}
          options={select_option_dataTransformation}
          onChange={this.select_onChanged_dataTransformation}
          placeholder="Select transformation method"
        />
        <Select
          value={select_dimensionReduction}
          isDisabled={select_isDisabled_dimensionReduction}
          options={select_option_dimensionReduction}
          onChange={this.select_onChanged_dimensionReduction}
          placeholder="Select dimension reduction method"
        />
        </div>
        }
      </div>

      {/* col 2 */}
      <div className="dataVisualizationWrap">
        <div className="section-header">
          <h4> Scanpath Visualization </h4>
        </div>
        <div className="visualizationViewWrap">
          { select_stiName !== null && select_stiName !== undefined &&  
          <div className="visViewDiv">
            <ScanpathVisualization 
              width={900}
              height={600}
              stimulusURL={stiURL}
              scanpathList={scanpathList}
              imageOpacity={alphaPicker_stimulusAlpha}
            />
          </div>
          }
          { select_stiName !== null && select_stiName !== undefined &&  
          <div className="viewControlDiv">
            <SketchPicker 
              width={260}
              color={tempColor}
              onChange={this.tempFunction}
            />
            <br></br>
            <AlphaPicker
              width={280}
              color={alphaPicker_stimulusColor}
              onChange={this.alphaPicker_onChange_stimulusAlpha}
            />
          </div>
          }
        </div>

        <div className="section-header">
          <h4> Patch Visualization View </h4>
        </div>
        <div className="patchVisualizationViewWrap">
          { patchDataList.length != 0 && select_patchImageFlag !== null && select_patchImageFlag !== undefined &&
          <div className="patchView">
            <PatchVisualization 
              width={900}
              height={535}
              patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
              patchList={patchDataList}
              patchDrawFlag={select_patchImageFlag.value}
            />
          </div>
          }
          { patchDataList.length != 0 &&
          <div className="patchViewControl">
            <Select
              value={select_patchImageFlag}
              options={select_option_patchImageFlag}
              onChange={this.select_onChanged_patchImageFlag}
              placeholder="Select fixated patch style"
            />
          </div>
          }
        </div>
      </div>

      {/* col 3 */}
      <div className="featureVisualizationViewWrap">
        <div className="colorEncodeLabelDescriptionBox">
          Salinecy feature color encode description
        </div>
        <div className="section-header">
          <h4> All patches: {patchDataList.length} </h4>
        </div>
        { patchDataList.length != 0 && select_patchImageFlag !== null && select_patchImageFlag !== undefined &&
        <div className="saliencyView_boxplot">
          <BoxPlot
            width={390}
            height={150}
            patchDataList={patchDataList}
          />
        </div>
        }
        <div className="section-header">
          <h4> Patches on fixation map: {patchesOnHumanFixationMap.length} </h4>
        </div>
        { patchDataList.length != 0 && select_patchImageFlag !== null && select_patchImageFlag !== undefined &&
        <div className="saliencyView_boxplot">
          <BoxPlot
            width={390}
            height={150}
            patchDataList={patchesOnHumanFixationMap}
          />
        </div>
        }
        <div className="section-header">
          <h4> Patches outside on fixation map: {patchesOutsideHumanFixationMap.length} </h4>
        </div>
        { patchDataList.length != 0 && select_patchImageFlag !== null && select_patchImageFlag !== undefined &&
        <div className="saliencyView_boxplot">
          <BoxPlot
            width={390}
            height={150}
            patchDataList={patchesOutsideHumanFixationMap}
          />
        </div>
        }
        <div className="saliencyView_linechart">

        </div>
      </div>
    </>
    );
  }
}

export default Analysis;
