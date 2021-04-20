import React from 'react';
import reactCSS from 'reactcss';
import axios from 'axios';
import Select from 'react-select';

// https://react-select.com/home
import { AlphaPicker, SketchPicker } from 'react-color';
// https://casesandberg.github.io/react-color/#api

import Heatmap from 'components/Heatmap';
import PatchVisualization from 'components/PatchVisualization';
import MultiPatchVisualization from 'components/MultiPatchVisualization';
import ScanpathVisualization from 'components/ScanpathVisualization';
import BoxPlot from 'components/BoxPlot';
// import LineChart from 'components/LineChart';
import HumanFixationMap from '../components/HumanFixationMap';
import ParallelCoordinateChart from '../components/ParallelCoordinateChart';
import BarChart from '../components/BarChart';

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

const select_option_overview = [
  { value:'asv', label: 'Analysis of Spatial Variance' },
  { value:'scanpath', label: '#Scanpaths' },
  { value:'patch_total', label: '#Patches' },
  { value:'patch_on', label: '#On Patches' },
  { value:'patch_out', label: '#Outside Patches' }
];

const select_option_scanpathSimilarity = [
  { value:'jd', label: 'Jaccard Coefficient' },
  { value:'dtw', label: 'Dynamic Time Warping' },
  { value:'lcs', label: 'Longest Common Subsequence' },
  { value:'fd', label: 'Frechet Distance' },
  { value:'ed', label: 'Edit (Levenshtein) Distance' }
];

const select_option_analysisStyle = [
  { value:'scanpath', label: 'Scanpath Analysis' },
  { value:'patch', label: 'Patch Analysis' }
];

const select_option_patchView = [
  { value:'multi', label: 'Multi View' },
  { value:'single', label: 'Single View' }
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

const select_option_patchImageFlag = [
  { value:'image', label: 'Draw fixated patch images' },
  { value:'box', label: 'Draw only label box' }
];

const select_option_humanFixationMapStyle = [
  { value:'original', label: 'Use original' },
  { value:'discrete', label: 'Use discrete' }
];

class Analysis extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      select_overview: [],
      select_stiDataset: [],
      select_semanticClass: [],
      select_stiName: [],
      select_participant: [],
      select_patchView: null,
      select_useCache: null,
      // select_cacheFile: null,
      select_scanpathSimilarityMetohd: null,
      select_main_scanpath: null,
      select_dataTransformation: null,
      select_dimensionReduction: null,
      select_patchImageFlag: {value:'box', label: 'Draw only label box' },
      select_humanFixationMapStyle : { value:'original', label: 'Use original' },
      select_analysisStyle: null,
      select_isDisabled_participant: true,
      select_isDisabled_semanticClass: true,
      select_isDisabled_stiName: true,
      select_isDisabled_scanpathSimilarity: true,
      select_isDisabled_mainScanpath: true,
      select_isDisabled_dataTransformation: true,
      select_isDisabled_dimensionReduction: true,
      select_isDisabled_useCache: true,
      // select_isDisabled_cacheFile: true,
      select_option_participant: [],
      select_option_stiClass: [],
      select_option_stiName: [],
      select_option_mainScanpath: [],
      // select_option_cacheFile: [],
      onFlag_overview_asv: false,
      onFlag_overview_scanpath: false,
      onFlag_overview_patch_total: false,
      onFlag_overview_patch_on: false,
      onFlag_overview_patch_out: false,
      STI_CLASS_LIST: [],
      FEATURE_LIST: [],
      spDataURL: "",
      stiURL: [],
      humanFixationMapURL: [],
      scanpathList: [],
      alphaPicker_stimulusAlpha: 1,
      alphaPicker_stimulusColor: {},
      alphapicker_patchBoxAlpha: 1,
      alphapicker_patchBoxColor: {},
      displayColorPicker_0: false,
      displayColorPicker_1: false,
      displayColorPicker_2: false,
      displayColorPicker_3: false,
      displayColorPicker_4: false,
      displayColorPicker_5: false,
      displayColorPicker_6: false,
      displayColorPicker_7: false,
      colorEncodings: [],
      colorEncoding_0: {r: '228', g: '26', b: '28', a:'1'},
      colorEncoding_1: {r: '55', g: '126', b: '184', a:'1'},
      colorEncoding_2: {r: '77', g: '175', b: '74', a:'1'},
      colorEncoding_3: {r: '255', g: '127', b: '0', a:'1'},
      colorEncoding_4: {r: '166', g: '86', b: '40', a:'1'},
      colorEncoding_5: {r: '153', g: '153', b: '153', a:'1'},
      colorEncoding_6: {r: '152', g: '78', b: '163', a:'1'},
      colorEncoding_7: {r: '247', g: '129', b: '191', a:'1'},
      processingDataColumns: [],
      processingDataList: [],
      rawDataList: [],
      patchDataList: [],
      patchDataList_multi: [],
      patchesOnHumanFixationMap: [],
      patchesOutsideHumanFixationMap: [],
      cacheFilePath: "",
      overviewCountDataList: [],
    };
  }

  select_onChange_overview = select_overview =>{
    console.log("select_onChange_overview");
    this.setState({select_overview});
    if(select_overview !== null && select_overview !== undefined){
      let flag_asv = false;
      let flag_scanpath = false;
      let flag_patch_total = false;
      let flag_patch_on = false;
      let flag_patch_out = false;
      for(let i=0; i<select_overview.length; i++){
        let _value = select_overview[i].value;
        if(_value == "asv"){
          flag_asv = true;
        }else if(_value == "scanpath"){
          flag_scanpath = true;
        }else if(_value == "patch_total"){
          flag_patch_total = true;
        }else if(_value == "patch_on"){
          flag_patch_on = true;
        }else if(_value == "patch_out"){
          flag_patch_out = true;
        }else{
          console.log("Unavailable flag selected");
        }
        if(this.state.select_semanticClass !== null && this.state.select_semanticClass !== undefined && this.state.select_semanticClass.length == 1){
          let selectedSemanticClass = this.state.select_semanticClass[0].value;
          const data = new FormData();
          data.set("semanticClass", selectedSemanticClass);
          axios.post(`http://${window.location.hostname}:5000/api/overview`, data)
          .then(response => {
            console.log(response.data.overview);
            this.setState({
              overviewCountDataList: response.data.overview
            });
          }).catch(error => {
            alert(`Error - ${error.message}`);
          });

        }
      }
      this.setState({
        onFlag_overview_asv: flag_asv
      });
      this.setState({
        onFlag_overview_scanpath: flag_scanpath
      });
      this.setState({
        onFlag_overview_patch_total: flag_patch_total
      });
      this.setState({
        onFlag_overview_patch_on: flag_patch_on
      });
      this.setState({
        onFlag_overview_patch_out: flag_patch_out
      });
    }else{
      this.setState({
        onFlag_overview_asv: false
      });
      this.setState({
        onFlag_overview_scanpath: false
      });
      this.setState({
        onFlag_overview_patch_total: false
      });
      this.setState({
        onFlag_overview_patch_on: false
      });
      this.setState({
        onFlag_overview_patch_out: false
      });
    }
  }

  select_onChanged_stiDataset = select_stiDataset =>{
    this.colorEncodingStateInitFunction();
    this.setState({select_stiDataset});
    // console.log("select_stiDataset");
    // console.log(select_stiDataset);
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
          let stiShortName = "(S";
          if(i<10){
            stiShortName = stiShortName+"0"+String(i)+")";
          }else{
            stiShortName = stiShortName+String(i)+")";
          }
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
            label: classShortName+" "+stiShortName+" "+stiFileName+ " ("+getStimulusNames[i][1] +"x"+ getStimulusNames[i][2]+")"
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
      let hfmURLList = [];
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
        let _hfmURL = {
          url: `http://${window.location.hostname}:5000/static/ground_truth/`+pathString.replace(".jpeg", ".jpg"),
          width: stiWidth,
          height: stiHeight
        }
        console.log(_hfmURL);
        stiURLList.push(_sURL);
        hfmURLList.push(_hfmURL);
        if(i==0){
          stiList_str = pathString;
        }else{
          stiList_str = stiList_str +"-"+ pathString;
        }
      }
      this.setState({
        stiURL: stiURLList
      });
      this.setState({
        humanFixationMapURL: hfmURLList
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
          { value:'all', label: 'All observers data: #'+getParticipantList.length }
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
        console.log('response.data.scanpathSimilarityValues');
        console.log(getSSVdata);
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
      // let _cacheFlag = true;
      // if(select_useCache.value == 'use'){
      //   _cacheFlag = true;
      //   axios.post(`http://${window.location.hostname}:5000/api/clustering/loadCacheList`)
      //   .then(response => {
      //     // console.log(response.data);
      //     let getCacheFileList = response.data.caches;
      //     let loadedCacheList = [];
      //     for(let i=0; i<getCacheFileList.length; i++){
      //       let _c ={
      //         value: getCacheFileList[i],
      //         label: getCacheFileList[i]
      //       };
      //       loadedCacheList.push(_c);
      //     }
      //     this.setState({
      //       select_option_cacheFile: loadedCacheList
      //     });
      //     this.setState({
      //       select_isDisabled_cacheFile: false
      //     });
          
      //   }).catch(error => {
      //     alert(`Error - ${error.message}`);
      //   });
      // }else{
      //   _cacheFlag = false;
      // }
      // _cacheFlag = false;
      this.setState({
        select_isDisabled_dataTransformation: false
      });
      this.setState({
        select_isDisabled_dimensionReduction: false
      });
      // this.setState({
      //   select_isDisabled_cacheFile: true
      // });
    }
  }

  select_onChange_patchView = select_patchView =>{
    console.log("select_onChange_patchView");
    this.setState({select_patchView});
    this.run_transformation_clustering(select_patchView, "", "");
  }

  // select_onChange_cacheFile = select_cacheFile =>{
  //   console.log("select_onChange_cacheFile");
  //   this.setState({select_cacheFile});
  //   let _cacheFilePath = `http://${window.location.hostname}:5000`+"/static/__cache__/pcache/"+select_cacheFile.value+"?"+Math.random();
  //   this.setState({
  //     cacheFilePath: _cacheFilePath
  //   });
  //   axios.post(_cacheFilePath)
  //   .then(response => {
  //     console.log(response.data);
  //   }).catch(error => {
  //     alert(`Error - ${error.message}`);
  //   });
  // }

  run_transformation_clustering = (pView, tMethod, drMethod) =>{
    let getStiNames = this.state.select_stiName;
    let selectedStisStr = "";
    for(let i=0; i<getStiNames.length; i++){
      let stiValue = getStiNames[i].value;
      if(i==0){
        selectedStisStr = selectedStisStr + stiValue;
      }else{
        selectedStisStr = selectedStisStr +"-"+ stiValue;
      }
    }
    if(pView == "single"){
      let cacheUseFlag = this.state.select_useCache.value;
      const data = new FormData();
      data.set('cacheUseFlag', cacheUseFlag)
      data.set('transformationMethod', tMethod);
      data.set('dimensionReductionMethod', drMethod);
      data.set('selectedStimulus', selectedStisStr);
      axios.post(`http://${window.location.hostname}:5000/api/clustering/processing`, data)
      .then(response => {
        // console.log(response.data);
        // console.log(response.data.dataColumns);
        this.setState({
          processingDataColumns: response.data.dataColumns
        });
        this.setState({
          processingDataList: response.data.processingData
        });
        this.setState({
          rawDataList: response.data.rawData
        });
        // console.log("generated cachefile path");
        // console.log(response.data.cacheFilePath);
        // console.log(`http://${window.location.hostname}:5000`+response.data.cacheFilePath+"?"+Math.random());
        this.setState({
          cacheFilePath: `http://${window.location.hostname}:5000`+response.data.cacheFilePath+"?"+Math.random()
        });
        
        let getPorcessedDataList = response.data.processingData;
        
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
        this.setState({
          patchesOnHumanFixationMap: onHFMPatches
        });
        this.setState({
          patchesOutsideHumanFixationMap: outsideHFMPatches
        });
        
      }).catch(error => {
        alert(`Error - ${error.message}`);
      });
    }else{
      let tMethods_str = "";
      for(let i=0; i<select_option_dataTransformation.length; i++){
        if(i==0){
          tMethods_str = select_option_dataTransformation[i].value;
        }else{
          tMethods_str = tMethods_str +"/"+ select_option_dataTransformation[i].value;
        }
      }
      let drMethods_str = "";
      for(let i=0; i<select_option_dimensionReduction.length; i++){
        if(i==0){
          drMethods_str = select_option_dimensionReduction[i].value;
        }else{
          drMethods_str = drMethods_str +"/"+ select_option_dimensionReduction[i].value;
        }
      }
      const data = new FormData();
      data.set('transformationMethod', tMethods_str);
      data.set('dimensionReductionMethod', drMethods_str);
      data.set('selectedStimulus', selectedStisStr);
      axios.post(`http://${window.location.hostname}:5000/api/clustering/processingMulti`, data)
      .then(response => {
        console.log(response.data);
        let getProcessedDataLists = response.data.processingData;
        this.setState({
          patchDataList_multi: getProcessedDataLists
        });
        
        console.log(response.data.cacheFilePath);
        let cacheFilePathList = response.data.cacheFilePath;
        let cPath = cacheFilePathList[0][0].split(".")[1] + ".csv";
        console.log("cPath");
        console.log(cPath);
        this.setState({
          cacheFilePath: `http://${window.location.hostname}:5000`+cPath+"?"+Math.random()
        });

        let onHFMPatches = [];
        let outsideHFMPatches = [];
        let getProcessedDataList = getProcessedDataLists[0];
        for(let i=0; i<getProcessedDataList.length; i++){
          let _label = getProcessedDataList[i][3];
          if(_label == 0){
            // label 0: outside
            outsideHFMPatches.push(getProcessedDataList[i]);
          }else{
            // label 1: on
            onHFMPatches.push(getProcessedDataList[i]);
          }
        }
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
  }

  select_onChanged_dataTransformation = select_dataTransformation =>{
    console.log("select_onChanged_dataTransformation");
    this.setState({select_dataTransformation});
    if(select_dataTransformation !== null && select_dataTransformation !== undefined && this.state.select_dimensionReduction !== null && this.state.select_dimensionReduction !== undefined){
      this.run_transformation_clustering(this.state.select_patchView ,select_dataTransformation.value, this.state.select_dimensionReduction.value);
    }
  }

  select_onChanged_dimensionReduction = select_dimensionReduction =>{
    console.log("select_onChanged_dimensionReduction");
    this.setState({select_dimensionReduction});
    if(select_dimensionReduction !== null && select_dimensionReduction !== undefined && this.state.select_dataTransformation !== null && this.state.select_dataTransformation !== undefined){
      this.run_transformation_clustering(this.state.select_patchView, this.state.select_dataTransformation.value, select_dimensionReduction.value);
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

  select_onChanged_analysisStyle = select_analysisStyle =>{
    console.log("select_onChanged_analysisStyle");
    this.setState({select_analysisStyle});
  }

  select_onChanged_humanFixationMapStyle = select_humanFixationMapStyle =>{
    console.log("select_onChanged_humanFixationMapStyle");
    this.setState({select_humanFixationMapStyle});
    let hfmURL = [];
    let getStiURL = this.state.stiURL[0];
    if(select_humanFixationMapStyle.value == "original"){
      let _url = getStiURL.url.replace("/stimulus/", "/ground_truth/");
      _url = _url.replace(".jpeg", ".jpg")
      hfmURL.push({
        url: getStiURL.url.replace("/stimulus/", "/ground_truth/"),
        width: getStiURL.width,
        height: getStiURL.height
      });
    }else{
      console.log(`http://${window.location.hostname}:5000/static/__cache__/discrete_ground_truth_fixation_map.png`,);
      hfmURL.push({
        url: `http://${window.location.hostname}:5000/static/__cache__/discrete_ground_truth_fixation_map.png`,
        width: getStiURL.width,
        height: getStiURL.height
      });
    }
    this.setState({
      humanFixationMapURL: hfmURL
    });
  }

  
  alphaPicker_onChange_stimulusAlpha = (color) =>{
    this.setState({alphaPicker_stimulusColor: color.rgb});
    this.setState({
      alphaPicker_stimulusAlpha: color.rgb.a
    });
  }

  alphaPicker_onChange_patchBoxAlpha = (color) =>{
    this.setState({alphapicker_patchBoxColor: color.rgb});
    this.setState({
      alphapicker_patchBoxAlpha: color.rgb.a
    });
  }

  // tempFunction = (color) =>{
  //   this.setState({tempColor:color.rgb});
  // }

  rgbToHex = (red, green, blue) =>{
    const rgb = (red << 16) | (green << 8) | (blue << 0);
    return '#' + (0x1000000 + rgb).toString(16).slice(1);
  }

  // color encoding handle events
  colorEncodingStateInitFunction =()=>{
    console.log("colorEncodingStateInitFunction");
    let colorEncoding = [
      this.rgbToHex(this.state.colorEncoding_0.r, this.state.colorEncoding_0.g, this.state.colorEncoding_0.b ), 
      this.rgbToHex(this.state.colorEncoding_1.r, this.state.colorEncoding_1.g, this.state.colorEncoding_1.b ), 
      this.rgbToHex(this.state.colorEncoding_2.r, this.state.colorEncoding_2.g, this.state.colorEncoding_2.b ), 
      this.rgbToHex(this.state.colorEncoding_3.r, this.state.colorEncoding_3.g, this.state.colorEncoding_3.b ), 
      this.rgbToHex(this.state.colorEncoding_4.r, this.state.colorEncoding_4.g, this.state.colorEncoding_4.b ), 
      this.rgbToHex(this.state.colorEncoding_5.r, this.state.colorEncoding_5.g, this.state.colorEncoding_5.b ), 
      this.rgbToHex(this.state.colorEncoding_6.r, this.state.colorEncoding_6.g, this.state.colorEncoding_6.b ), 
      this.rgbToHex(this.state.colorEncoding_7.r, this.state.colorEncoding_7.g, this.state.colorEncoding_7.b )
    ];
    
    this.setState({
      colorEncodings: colorEncoding
    });
  }

  // colorEncodingFlagChange = (_flag, _idx) =>{
  //   let _dcp = this.state.displayColorPickers;
  //   _dcp[_idx] = _flag;
  //   this.setState({
  //     displayColorPickers: _dcp
  //   });
  // }

  colorEncodingRGBChange = (_rgb, _idx) =>{
    let _ce = [];
    for(let i=0; i<this.state.colorEncodings.length; i++){
      if(i!=_idx){
        _ce.push(this.state.colorEncodings[i]);
      }else{
        _ce.push(this.rgbToHex(_rgb.r, _rgb.g, _rgb.b));
      }
    }
    this.setState({
      colorEncodings: _ce
    });
  }
  // 0
  handleClick_0 = () => {
    this.setState({ displayColorPicker_0: !this.state.displayColorPicker_0 });
  };
  handleClose_0 = () => {
    this.setState({ displayColorPicker_0: false });
  };
  handleChange_0 = (color) => {
    this.setState({ colorEncoding_0: color.rgb });
    this.colorEncodingRGBChange(color.rgb, 0);
  };
  // 1
  handleClick_1 = () => {
    this.setState({ displayColorPicker_1: !this.state.displayColorPicker_1 });
  };
  handleClose_1 = () => {
    this.setState({ displayColorPicker_1: false });
  };
  handleChange_1 = (color) => {
    this.setState({ colorEncoding_1: color.rgb });
    this.colorEncodingRGBChange(color.rgb, 1);
  };
  // 2
  handleClick_2 = () => {
    this.setState({ displayColorPicker_2: !this.state.displayColorPicker_2 });
  };
  handleClose_2 = () => {
    this.setState({ displayColorPicker_2: false });
  };
  handleChange_2 = (color) => {
    this.setState({ colorEncoding_2: color.rgb });
    this.colorEncodingRGBChange(color.rgb, 2);
  };
  // 3
  handleClick_3 = () => {
    this.setState({ displayColorPicker_3: !this.state.displayColorPicker_3 });
  };
  handleClose_3 = () => {
    this.setState({ displayColorPicker_3: false });
  };
  handleChange_3 = (color) => {
    this.setState({ colorEncoding_3: color.rgb });
    this.colorEncodingRGBChange(color.rgb, 3);
  };
  // 4
  handleClick_4 = () => {
    this.setState({ displayColorPicker_4: !this.state.displayColorPicker_4 });
  };
  handleClose_4 = () => {
    this.setState({ displayColorPicker_4: false });
  };
  handleChange_4 = (color) => {
    this.setState({ colorEncoding_4: color.rgb });
    this.colorEncodingRGBChange(color.rgb, 4);
  };
  // 5
  handleClick_5 = () => {
    this.setState({ displayColorPicker_5: !this.state.displayColorPicker_5 });
  };
  handleClose_5 = () => {
    this.setState({ displayColorPicker_5: false });
  };
  handleChange_5 = (color) => {
    this.setState({ colorEncoding_5: color.rgb });
    this.colorEncodingRGBChange(color.rgb, 5);
  };
  // 6
  handleClick_6 = () => {
    this.setState({ displayColorPicker_6: !this.state.displayColorPicker_6 });
  };
  handleClose_6 = () => {
    this.setState({ displayColorPicker_6: false });
  };
  handleChange_6 = (color) => {
    this.setState({ colorEncoding_6: color.rgb });
    this.colorEncodingRGBChange(color.rgb, 6);
  };
  // 7
  handleClick_7 = () => {
    this.setState({ displayColorPicker_7: !this.state.displayColorPicker_7 });
  };
  handleClose_7 = () => {
    this.setState({ displayColorPicker_7: false });
  };
  handleChange_7 = (color) => {
    this.setState({ colorEncoding_7: color.rgb });
    this.colorEncodingRGBChange(color.rgb, 7);
  };



  render() {
    // overview
    const { select_overview, overviewCountDataList, onFlag_overview_asv, onFlag_overview_scanpath, onFlag_overview_patch_total, onFlag_overview_patch_on, onFlag_overview_patch_out } = this.state;
    // data filter select
    const { select_stiDataset, select_participant, select_semanticClass, select_stiName } = this.state;
    const { select_option_participant, select_option_stiClass, select_option_stiName } = this.state;
    const { select_isDisabled_participant, select_isDisabled_semanticClass, select_isDisabled_stiName } = this.state;
    // sp heatmap
    const { spDataURL, FEATURE_LIST, STI_CLASS_LIST} = this.state;
    // analysis style setting
    const { select_analysisStyle } = this.state;
    const { colorEncodings, alphaPicker_stimulusColor, alphaPicker_stimulusAlpha, alphapicker_patchBoxAlpha, alphapicker_patchBoxColor } = this.state;
    const { displayColorPicker_0, displayColorPicker_1, displayColorPicker_2, displayColorPicker_3, displayColorPicker_4, displayColorPicker_5, displayColorPicker_6, displayColorPicker_7 } = this.state;
    const { colorEncoding_0, colorEncoding_1, colorEncoding_2, colorEncoding_3, colorEncoding_4, colorEncoding_5, colorEncoding_6, colorEncoding_7 } = this.state;
    // scanpath visualization
    const { stiURL, scanpathList } = this.state;
    // scanpath similarity
    const { select_main_scanpath, select_isDisabled_mainScanpath, select_option_mainScanpath, select_scanpathSimilarityMetohd, select_isDisabled_scanpathSimilarity } = this.state;
    // patch clustering
    const { select_patchView, patchDataList_multi, select_useCache, select_dataTransformation, select_dimensionReduction } = this.state;
    // const { select_cacheFile, select_option_cacheFile, select_isDisabled_cacheFile } = this.state;
    const { select_humanFixationMapStyle } = this.state;
    // const { select_dataClustering, select_isDisabled_dataClustering } = this.state;
    const { select_isDisabled_useCache, select_isDisabled_dataTransformation, select_isDisabled_dimensionReduction } = this.state;
    const { patchDataList, select_patchImageFlag, humanFixationMapURL, rawDataList } = this.state;
    // saliency features visualization
    const { patchesOnHumanFixationMap, patchesOutsideHumanFixationMap, cacheFilePath } = this.state;

    // color encoding reactCSS styles
    let colorEncodingStyles = [];
    // colorEncoding_0
    colorEncodingStyles.push(
      reactCSS({
        'default': {
          color: {
            width: '36px',
            height: '14px',
            borderRadius: '2px',
            background: `rgba(${ colorEncoding_0.r }, ${ colorEncoding_0.g }, ${ colorEncoding_0.b }, ${ colorEncoding_0.a })`,
          },
          swatch: {
            padding: '5px',
            background: '#fff',
            borderRadius: '1px',
            boxShadow: '0 0 0 1px rgba(0,0,0,.1)',
            display: 'inline-block',
            cursor: 'pointer',
          },
          popover: {
            position: 'absolute',
            zIndex: '2',
          },
          cover: {
            position: 'fixed',
            top: '0px',
            right: '0px',
            bottom: '0px',
            left: '0px',
          },
        },
      })
    );
    // colorEncoding_1
    colorEncodingStyles.push(
      reactCSS({
        'default': {
          color: {
            width: '36px',
            height: '14px',
            borderRadius: '2px',
            background: `rgba(${ colorEncoding_1.r }, ${ colorEncoding_1.g }, ${ colorEncoding_1.b }, ${ colorEncoding_1.a })`,
          },
          swatch: {
            padding: '5px',
            background: '#fff',
            borderRadius: '1px',
            boxShadow: '0 0 0 1px rgba(0,0,0,.1)',
            display: 'inline-block',
            cursor: 'pointer',
          },
          popover: {
            position: 'absolute',
            zIndex: '2',
          },
          cover: {
            position: 'fixed',
            top: '0px',
            right: '0px',
            bottom: '0px',
            left: '0px',
          },
        },
      })
    );
    // colorEncoding_2
    colorEncodingStyles.push(
      reactCSS({
        'default': {
          color: {
            width: '36px',
            height: '14px',
            borderRadius: '2px',
            background: `rgba(${ colorEncoding_2.r }, ${ colorEncoding_2.g }, ${ colorEncoding_2.b }, ${ colorEncoding_2.a })`,
          },
          swatch: {
            padding: '5px',
            background: '#fff',
            borderRadius: '1px',
            boxShadow: '0 0 0 1px rgba(0,0,0,.1)',
            display: 'inline-block',
            cursor: 'pointer',
          },
          popover: {
            position: 'absolute',
            zIndex: '2',
          },
          cover: {
            position: 'fixed',
            top: '0px',
            right: '0px',
            bottom: '0px',
            left: '0px',
          },
        },
      })
    );
    // colorEncoding_3
    colorEncodingStyles.push(
      reactCSS({
        'default': {
          color: {
            width: '36px',
            height: '14px',
            borderRadius: '2px',
            background: `rgba(${ colorEncoding_3.r }, ${ colorEncoding_3.g }, ${ colorEncoding_3.b }, ${ colorEncoding_3.a })`,
          },
          swatch: {
            padding: '5px',
            background: '#fff',
            borderRadius: '1px',
            boxShadow: '0 0 0 1px rgba(0,0,0,.1)',
            display: 'inline-block',
            cursor: 'pointer',
          },
          popover: {
            position: 'absolute',
            zIndex: '2',
          },
          cover: {
            position: 'fixed',
            top: '0px',
            right: '0px',
            bottom: '0px',
            left: '0px',
          },
        },
      })
    );
    // colorEncoding_4
    colorEncodingStyles.push(
      reactCSS({
        'default': {
          color: {
            width: '36px',
            height: '14px',
            borderRadius: '2px',
            background: `rgba(${ colorEncoding_4.r }, ${ colorEncoding_4.g }, ${ colorEncoding_4.b }, ${ colorEncoding_4.a })`,
          },
          swatch: {
            padding: '5px',
            background: '#fff',
            borderRadius: '1px',
            boxShadow: '0 0 0 1px rgba(0,0,0,.1)',
            display: 'inline-block',
            cursor: 'pointer',
          },
          popover: {
            position: 'absolute',
            zIndex: '2',
          },
          cover: {
            position: 'fixed',
            top: '0px',
            right: '0px',
            bottom: '0px',
            left: '0px',
          },
        },
      })
    );
    // colorEncoding_5
    colorEncodingStyles.push(
      reactCSS({
        'default': {
          color: {
            width: '36px',
            height: '14px',
            borderRadius: '2px',
            background: `rgba(${ colorEncoding_5.r }, ${ colorEncoding_5.g }, ${ colorEncoding_5.b }, ${ colorEncoding_5.a })`,
          },
          swatch: {
            padding: '5px',
            background: '#fff',
            borderRadius: '1px',
            boxShadow: '0 0 0 1px rgba(0,0,0,.1)',
            display: 'inline-block',
            cursor: 'pointer',
          },
          popover: {
            position: 'absolute',
            zIndex: '2',
          },
          cover: {
            position: 'fixed',
            top: '0px',
            right: '0px',
            bottom: '0px',
            left: '0px',
          },
        },
      })
    );
    // colorEncoding_6
    colorEncodingStyles.push(
      reactCSS({
        'default': {
          color: {
            width: '36px',
            height: '14px',
            borderRadius: '2px',
            background: `rgba(${ colorEncoding_6.r }, ${ colorEncoding_6.g }, ${ colorEncoding_6.b }, ${ colorEncoding_6.a })`,
          },
          swatch: {
            padding: '5px',
            background: '#fff',
            borderRadius: '1px',
            boxShadow: '0 0 0 1px rgba(0,0,0,.1)',
            display: 'inline-block',
            cursor: 'pointer',
          },
          popover: {
            position: 'absolute',
            zIndex: '2',
          },
          cover: {
            position: 'fixed',
            top: '0px',
            right: '0px',
            bottom: '0px',
            left: '0px',
          },
        },
      })
    );
    // colorEncoding_7
    colorEncodingStyles.push(
      reactCSS({
        'default': {
          color: {
            width: '36px',
            height: '14px',
            borderRadius: '2px',
            background: `rgba(${ colorEncoding_7.r }, ${ colorEncoding_7.g }, ${ colorEncoding_7.b }, ${ colorEncoding_7.a })`,
          },
          swatch: {
            padding: '5px',
            background: '#fff',
            borderRadius: '1px',
            boxShadow: '0 0 0 1px rgba(0,0,0,.1)',
            display: 'inline-block',
            cursor: 'pointer',
          },
          popover: {
            position: 'absolute',
            zIndex: '2',
          },
          cover: {
            position: 'fixed',
            top: '0px',
            right: '0px',
            bottom: '0px',
            left: '0px',
          },
        },
      })
    );

    return (
    <>
      {/* data filter */}
      <div className="inputBoxWrap">
        <div className="page-header">
          <div id="logo"></div><div><h3>Visual Attention Analysis System</h3></div>
        </div>
        <div className="section-header">
          <h4> Data Filter </h4>
        </div>
        <Select 
          value={select_stiDataset}
          isMulti
          options={select_option_dataset}
          onChange={this.select_onChanged_stiDataset}
          className="basic-multi-select"
          classNamePrefix="select"
          placeholder="Stimulus dataset"
        />
        <Select 
          value={select_semanticClass}
          isDisabled={select_isDisabled_semanticClass}
          isMulti
          options={select_option_stiClass}
          onChange={this.select_onChanged_semanticClass}
          className="basic-multi-select"
          classNamePrefix="select"
          placeholder="Semantic class"
        />
        <Select
          value={select_overview}
          isMulti
          options={select_option_overview}
          onChange={this.select_onChange_overview}
          className="basic-multi-select"
          classNamePrefix="select"
          placeholder="Overview switch"
        />
        <Select 
          value={select_stiName}
          isDisabled={select_isDisabled_stiName}
          isMulti
          options={select_option_stiName}
          onChange={this.select_onChanged_stiName}
          className="basic-multi-select"
          classNamePrefix="select"
          placeholder="Visual stimulus"
        />
        <Select 
          value={select_participant}
          isDisabled={select_isDisabled_participant}
          isMulti
          options={select_option_participant}
          onChange={this.select_onChanged_participant}
          className="basic-multi-select"
          classNamePrefix="select"
          placeholder="Observer ID"
        />
        <Select
          value={select_analysisStyle}
          options={select_option_analysisStyle}
          onChange={this.select_onChanged_analysisStyle}
          placeholder="Analysis mode"
        />
        { onFlag_overview_asv == true && select_stiDataset !== null && select_stiDataset !== undefined && select_stiDataset.length !=0 && 
        <div className="section-header">
          <h4> Analysis of Spatial Variance </h4>
        </div>
        }
        { onFlag_overview_asv == true && select_stiDataset !== null && select_stiDataset !== undefined && spDataURL.length != 0 &&
        <div id="heat" className="page-section heatmap">
          <Heatmap 
            width={400}
            height={400}
            dataURL={spDataURL}
            FEATURE_DEFINE={FEATURE_LIST}
            STI_CLASS_DEFINE={STI_CLASS_LIST}
          />
        </div>
        }
        { onFlag_overview_scanpath == true &&
        <div className="section-header">
          <h4> Overview: #Scanpaths  </h4>
        </div>
        }
        { onFlag_overview_scanpath == true &&
        <div>
          <BarChart
            width={400}
            height={400}
            overviewSytle={"scanpath"}
            countDataList={overviewCountDataList}
            colorEncoding={colorEncodings}
          />
        </div>
        }
        { onFlag_overview_patch_total == true &&
        <div className="section-header">
          <h4> Overview: #Total Patches  </h4>
        </div>
        }
        { onFlag_overview_patch_total == true &&
        <div>
          <BarChart
            width={400}
            height={400}
            overviewSytle={"patch_total"}
            countDataList={overviewCountDataList}
            colorEncoding={colorEncodings}
          />
        </div>
        }
        { onFlag_overview_patch_on == true &&
        <div className="section-header">
          <h4> Overview: #Patches on HFM  </h4>
        </div>
        }
        { onFlag_overview_patch_on == true &&
        <div>
          <BarChart
            width={400}
            height={400}
            overviewSytle={"patch_on"}
            countDataList={overviewCountDataList}
            colorEncoding={colorEncodings}
          />
        </div>
        }
        { onFlag_overview_patch_out == true &&
        <div className="section-header">
          <h4> Overview: #Patches outside on HFM  </h4>
        </div>
        }
        { onFlag_overview_patch_out == true &&
        <div>
          <BarChart
            width={400}
            height={400}
            overviewSytle={"patch_out"}
            countDataList={overviewCountDataList}
            colorEncoding={colorEncodings}
          />
        </div>
        }
        
        <br></br>
        { colorEncodings.length != 0 &&
        <div className="colorSelectBox">
          <div className="colorBox">
            <div style={ colorEncodingStyles[0].swatch } onClick={ this.handleClick_0 }>
              <div style={ colorEncodingStyles[0].color } />
            </div>
            { displayColorPicker_0 ? <div style={ colorEncodingStyles[0].popover }>
              <div style={ colorEncodingStyles[0].cover } onClick={ this.handleClose_0 }/>
              <SketchPicker color={ colorEncoding_0 } onChange={ this.handleChange_0 } />
            </div> : null }
          </div>
          <div className="colorBox">
            <div style={ colorEncodingStyles[1].swatch } onClick={ this.handleClick_1 }>
              <div style={ colorEncodingStyles[1].color } />
            </div>
            { displayColorPicker_1 ? <div style={ colorEncodingStyles[1].popover }>
              <div style={ colorEncodingStyles[1].cover } onClick={ this.handleClose_1 }/>
              <SketchPicker color={ colorEncoding_1 } onChange={ this.handleChange_1 } />
            </div> : null }
          </div>
          <div className="colorBox">
            <div style={ colorEncodingStyles[2].swatch } onClick={ this.handleClick_2 }>
              <div style={ colorEncodingStyles[2].color } />
            </div>
            { displayColorPicker_2 ? <div style={ colorEncodingStyles[2].popover }>
              <div style={ colorEncodingStyles[2].cover } onClick={ this.handleClose_2 }/>
              <SketchPicker color={ colorEncoding_2 } onChange={ this.handleChange_2 } />
            </div> : null }
          </div>
          <div className="colorBox">
            <div style={ colorEncodingStyles[3].swatch } onClick={ this.handleClick_3 }>
              <div style={ colorEncodingStyles[3].color } />
            </div>
            { displayColorPicker_3 ? <div style={ colorEncodingStyles[3].popover }>
              <div style={ colorEncodingStyles[3].cover } onClick={ this.handleClose_3 }/>
              <SketchPicker color={ colorEncoding_3 } onChange={ this.handleChange_3 } />
            </div> : null }
          </div>
          <div className="colorBox">
            <div style={ colorEncodingStyles[4].swatch } onClick={ this.handleClick_4 }>
              <div style={ colorEncodingStyles[4].color } />
            </div>
            { displayColorPicker_4 ? <div style={ colorEncodingStyles[4].popover }>
              <div style={ colorEncodingStyles[4].cover } onClick={ this.handleClose_4 }/>
              <SketchPicker color={ colorEncoding_4 } onChange={ this.handleChange_4 } />
            </div> : null }
          </div>
          <div className="colorBox">
            <div style={ colorEncodingStyles[5].swatch } onClick={ this.handleClick_5 }>
              <div style={ colorEncodingStyles[5].color } />
            </div>
            { displayColorPicker_5 ? <div style={ colorEncodingStyles[5].popover }>
              <div style={ colorEncodingStyles[5].cover } onClick={ this.handleClose_5 }/>
              <SketchPicker color={ colorEncoding_5 } onChange={ this.handleChange_5 } />
            </div> : null }
          </div>
          <div className="colorBox">
            <div style={ colorEncodingStyles[6].swatch } onClick={ this.handleClick_6 }>
              <div style={ colorEncodingStyles[6].color } />
            </div>
            { displayColorPicker_6 ? <div style={ colorEncodingStyles[6].popover }>
              <div style={ colorEncodingStyles[6].cover } onClick={ this.handleClose_6 }/>
              <SketchPicker color={ colorEncoding_6 } onChange={ this.handleChange_6 } />
            </div> : null }
          </div>
          <div className="colorBox">
            <div style={ colorEncodingStyles[7].swatch } onClick={ this.handleClick_7 }>
              <div style={ colorEncodingStyles[7].color } />
            </div>
            { displayColorPicker_7 ? <div style={ colorEncodingStyles[7].popover }>
              <div style={ colorEncodingStyles[7].cover } onClick={ this.handleClose_7 }/>
              <SketchPicker color={ colorEncoding_7 } onChange={ this.handleChange_7 } />
            </div> : null }
          </div>
        </div>
        }
      </div>
      

      {/* col 2 */}
      <div className="dataVisualizationWrap">
        { select_analysisStyle !== null && select_analysisStyle !== undefined && select_analysisStyle.value == "scanpath" && 
        <div className="section-header">
          <h4> Scanpath Visualization </h4>
        </div>
        }
        { select_analysisStyle !== null && select_analysisStyle !== undefined && select_analysisStyle.value == "scanpath" && 
        <div className="scanpathVisualizationViewWrap">
          <div className="visViewDiv">
            <ScanpathVisualization 
              width={900}
              height={600}
              stimulusURL={stiURL}
              scanpathList={scanpathList}
              imageOpacity={alphaPicker_stimulusAlpha}
              colorEncoding={colorEncodings}
            />
          </div>
          <div className="viewControlDiv">
            { select_analysisStyle !== null && select_analysisStyle !== undefined && select_analysisStyle.value == "scanpath" &&
            <div>
              <Select
                value={select_main_scanpath}
                isDisabled={select_isDisabled_mainScanpath}
                options={select_option_mainScanpath}
                onChange={this.select_onChanged_mainScanpath}
                placeholder="Scanpath for calculation similarity"
              />
              <Select
                value={select_scanpathSimilarityMetohd}
                isDisabled={select_isDisabled_scanpathSimilarity}
                options={select_option_scanpathSimilarity}
                onChange={this.select_onChanged_scanpathSimilarity}
                placeholder="Scanpath similarity calculation method"
              />
            </div>
            }
            <AlphaPicker
              width={280}
              color={alphaPicker_stimulusColor}
              onChange={this.alphaPicker_onChange_stimulusAlpha}
            />
          </div>
        </div>
        }
        { select_analysisStyle !== null && select_analysisStyle !== undefined && select_analysisStyle.value == "patch" && 
        <div className="section-header">
          <h4> Patch Visualization View </h4>
        </div>
        }
        { select_analysisStyle !== null && select_analysisStyle !== undefined && select_analysisStyle.value == "patch" && 
        <div className="patchVisualizationViewWrap">
          { patchDataList.length != 0 && select_patchView != null && select_patchView != undefined && select_patchView.value == "single" &&
          <div className="patchView">
            <PatchVisualization 
              width={900}
              height={600}
              patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
              patchList={patchDataList}
              patchDrawFlag={select_patchImageFlag.value}
              patchBoxOpacity={alphapicker_patchBoxAlpha}
              colorEncoding={colorEncodings}
            />
          </div>
          }
          { patchDataList_multi.length == 25 && select_patchView != null && select_patchView != undefined && select_patchView.value == "multi" &&
          <div className="multiPatchVisWrap">
            <div className="multiPatchView">
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[0]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[1]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <PatchVisualization 
                  width={180}
                  height={120}
                  patchDrawLength={8}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[2]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[3]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[4]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
            </div>
            <div className="multiPatchView">
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[5]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[6]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[7]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[8]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
              <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[9]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
            </div>
            <div className="multiPatchView">
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[10]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[11]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[12]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[13]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[14]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
            </div>
            <div className="multiPatchView">
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[15]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[16]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[17]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[18]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[19]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
            </div>
            <div className="multiPatchView">
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[20]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[21]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[22]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[23]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
              <div className="multiPartView">
                <MultiPatchVisualization 
                  width={180}
                  height={120}
                  patchURLs={`http://${window.location.hostname}:5000/static/__cache__/aggregated_patch.png?`+Math.random()}
                  patchList={patchDataList_multi[24]}
                  patchDrawFlag={select_patchImageFlag.value}
                  patchBoxOpacity={alphapicker_patchBoxAlpha}
                  colorEncoding={colorEncodings}
                />
              </div>
            </div>
          </div>
          }
          <div className="patchViewControl">
          { select_analysisStyle !== null && select_analysisStyle !== undefined && select_analysisStyle.value == "patch" && 
            <Select
              value={select_patchView}
              options={select_option_patchView}
              onChange={this.select_onChange_patchView}
              placeholder="Patch view style"
            />
          }
          { select_analysisStyle !== null && select_analysisStyle !== undefined && select_analysisStyle.value == "patch" && select_patchView != null && select_patchView != undefined && select_patchView.value == "single" &&
            <Select
              value={select_useCache}
              isDisabled={select_isDisabled_useCache}
              options={select_option_useCache}
              onChange={this.select_onChange_useCache}
              placeholder="Use cache file or not"
            />
          }
          {/* { select_option_cacheFile.length > 0 && select_useCache.value == "use" && select_analysisStyle !== null && select_analysisStyle !== undefined && select_analysisStyle.value == "patch" &&
          <div>
            <Select
              value={select_cacheFile}
              isDisabled={select_isDisabled_cacheFile}
              options={select_option_cacheFile}
              onChange={this.select_onChange_cacheFile}
              placeholder="Cache file"
            />
          </div>
          } */}
          { select_useCache !== null && select_useCache !== undefined && select_analysisStyle !== null && select_analysisStyle !== undefined && select_analysisStyle.value == "patch" && select_patchView != null && select_patchView != undefined && select_patchView.value == "single" &&
          <div>
          <Select
            value={select_dataTransformation}
            isDisabled={select_isDisabled_dataTransformation}
            options={select_option_dataTransformation}
            onChange={this.select_onChanged_dataTransformation}
            placeholder="Transformation method"
          />
          <Select
            value={select_dimensionReduction}
            isDisabled={select_isDisabled_dimensionReduction}
            options={select_option_dimensionReduction}
            onChange={this.select_onChanged_dimensionReduction}
            placeholder="Dimension reduction method"
          />
          </div>
          }
          { select_patchView != null && select_patchView != undefined &&
          <div>
            <Select
              value={select_patchImageFlag}
              options={select_option_patchImageFlag}
              onChange={this.select_onChanged_patchImageFlag}
              placeholder="Fixated image patch style"
            />
            <br></br>
            <AlphaPicker
              width={280}
              color={alphapicker_patchBoxColor}
              onChange={this.alphaPicker_onChange_patchBoxAlpha}
            />
            </div>
          }
          <br></br>
          { humanFixationMapURL.length != 0 && rawDataList.length != 0 &&
          <div>
            <HumanFixationMap
              width={280}
              height={290}
              humanFixationMapURL={humanFixationMapURL}
              patchDataList={rawDataList}
              colorEncoding={colorEncodings}
            />
            <Select
              value={select_humanFixationMapStyle}
              options={select_option_humanFixationMapStyle}
              onChange={this.select_onChanged_humanFixationMapStyle}
            />
          </div>
          }
          </div>
        </div>
        }
        <div className="section-header">
          <h4> Saliency Feature Visaulzation View </h4>
        </div>
        <div className="saliencyVisualizationWrap">
          { cacheFilePath !== "" &&
          <div className="visualizationDiv">
            <ParallelCoordinateChart
              width={900}
              height={530}
              patchDataFileURL={cacheFilePath}
              colorEncoding={colorEncodings}
            />
          </div>
          }
          <div className="subSaliencyVisDiv">
            { patchDataList.length != 0 &&
            <div className="section-header">
              <h4> All patches: {patchDataList.length} </h4>
            </div>
            }
            { patchDataList.length != 0 && 
            <div className="saliencyView_boxplot">
              <BoxPlot
                width={290}
                height={140}
                patchDataList={patchDataList}
                colorEncoding={colorEncodings}
              />
            </div>
            }
            { patchDataList.length != 0 &&
            <div className="section-header">
              <h4> Patches on HFM: {patchesOnHumanFixationMap.length} </h4>
            </div>
            }
            { patchDataList.length != 0 && 
            <div className="saliencyView_boxplot">
              <BoxPlot
                width={290}
                height={140}
                patchDataList={patchesOnHumanFixationMap}
                colorEncoding={colorEncodings}
              />
            </div>
            }
            { patchDataList.length != 0 &&
            <div className="section-header">
              <h4> Patches outside on HFM: {patchesOutsideHumanFixationMap.length} </h4>
            </div>
            }
            { patchDataList.length != 0 && 
            <div className="saliencyView_boxplot">
              <BoxPlot
                width={290}
                height={140}
                patchDataList={patchesOutsideHumanFixationMap}
                colorEncoding={colorEncodings}
              />
            </div>
            }
          </div>

        </div>
        
      </div>

      {/* col 3 */}
      <div className="featureVisualizationViewWrap">
        {/* <div className="colorEncodeLabelDescriptionBox">
          Salinecy feature color encode description
        </div> */}
        
        
        {/* { patchDataList.length != 0 && 
        <div className="saliencyView_linechart">
          <LineChart
            width={390}
            height={200}
            patchDataList={patchDataList}
            colorEncoding={colorEncodings}
          />
        </div>
        } */}
        
        
        {/* { patchDataList.length != 0 && 
        <div className="saliencyView_linechart">
          <LineChart
            width={390}
            height={200}
            patchDataList={patchesOnHumanFixationMap}
            colorEncoding={colorEncodings}
          />
        </div>
        } */}
        
        
        {/* { patchDataList.length != 0 && 
        <div className="saliencyView_linechart">
          <LineChart
            width={390}
            height={200}
            patchDataList={patchesOutsideHumanFixationMap}
            colorEncoding={colorEncodings}
          />
        </div>
        } */}
      </div>
    </>
    );
  }
}

export default Analysis;
