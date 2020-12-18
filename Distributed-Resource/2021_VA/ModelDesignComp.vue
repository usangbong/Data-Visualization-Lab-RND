<template>
  <div>
    <div class="ComponentTitle">
      <h3> Model Design</h3>
    </div>
    <v-card class="ModelDesignContainer" elevation="4">
      <div class="WrapComponent DataWrap">
        <v-card class="CardComponent DataCard" elevation="2.5">
          <div id="DataInput">
            <div class="dataBtnComponent">
              <label for="file_uploads">Choose file to upload (.csv)</label>
              
              <button id="file-select" @click="fileSelect">Choose a file</button>
              <input type="file" id="file_uploads" name="file_uploads" accept=".csv" @change="uploadDataFile">
              <!--
              <v-btn class="dataBtn" text icon color="rgba(253,205,172,1)">
                <v-icon x-large>mdi-alpha-x-circle</v-icon>
              </v-btn>
              <v-btn class="dataBtn" text icon color="rgba(204,204,204,1)">
                <v-icon x-large>mdi-alpha-x-circle-outline</v-icon>
              </v-btn>
              <v-btn class="dataBtn" text icon color="rgba(253,205,172,1)">
                <v-icon x-large>mdi-alpha-y-box</v-icon>
              </v-btn>
              <v-btn class="dataBtn" text icon color="rgba(204,204,204,1)">
                <v-icon x-large>mdi-alpha-y-box-outline</v-icon>
              </v-btn>-->
            </div>
            <v-file-input
              chips
              multiple
              label="File input X"
              @change="uploadDataFile"
              type="file"
            ></v-file-input>
            <v-file-input
              small-chips
              multiple
              label="File input Y"
            ></v-file-input>
          </div>
        </v-card>
        <div class="StepName">
          <h2>Data</h2>
        </div>
      </div>
    
      <div class="NextArrow"> 
          <img src="../assets/arrow_bold.png">
      </div>
      
      <div class="WrapComponent FeatureWrap">
        <v-card class="CardComponent FeatureCard" elevation="1">
            <CorrBarChart  v-if="featureDataLoaded" :chartData="featureBarChart" :style="corrBarStyle" />
        </v-card>
        <div class="StepName">
          <h2>Feature</h2>
        </div>
      </div>
      <div class="NextArrow"> 
          <img src="../assets/arrow_bold.png">
      </div>
      
      <div class="WrapComponent TransformWrap">
        <v-card class="CardComponent TransformCard" elevation="1">
          <div class="TransformRadio">
            <input type="radio" @change="setTransformMode" name="transform" id="radio1" value="1" v-model="picked">
            <label for="radio1"> Log Transformation</label><br>
            <input type="radio" @change="setTransformMode" name="transform" id="radio2" value="2" v-model="picked">
            <label for="radio2"> Square Root Transformation</label><br>
            <input type="radio" @change="setTransformMode" name="transform" id="radio3" value="3" v-model="picked">
            <label for="radio3"> Yeo-Johonson Transformation</label><br>
            <input type="radio" @change="setTransformMode" name="transform" id="radio4" value="4" v-model="picked">
            <label for="radio4"> Box-Cox Transformation</label><br>
            <input type="radio" @change="setTransformMode" name="transform" id="radio5" value="5" v-model="picked">
            <label for="radio5"> Wavelet Transformation</label><br>
          </div>
          <br><div> Picked : {{ picked }}</div>
          <div class="TransformChart" elevation="1">
              <TransfmBarChart  v-if="transfmDataLoaded" :chartData="transfmBarChart" :style="transfmBarStyle"/>
          </div>
        </v-card>
        <div class="StepName">
          <h2>Transformation</h2>
        </div>
      </div>
      
      <div class="NextArrow"> 
          <img src="../assets/arrow_bold.png">
      </div>
      
      <div class="WrapComponent ModelWrap">
        <v-card class="CardComponent ModelCard" elevation="1">
          <div class="ModelLoad">  
            <v-text-field label="Model" :rules="rules" hide-details="auto"></v-text-field>
            <v-text-field label="number of models"></v-text-field>
            <v-text-field label="number of datasets"></v-text-field>
            <v-text-field label="number of epochs"></v-text-field>
            <!--<v-text-field label="optimizer"></v-text-field>
            <v-text-field label="learning rate"></v-text-field>
            <v-text-field label="number of hidden"></v-text-field>-->
          </div>
        </v-card>
        <div class="StepName">
          <h2>Model</h2>
        </div>
      </div>
      <div class="NextArrow"> 
          <img src="../assets/arrow_bold.png">
      </div>
      <v-btn RUN elevation="2" @click="runDeepLearning">RUN</v-btn>
    </v-card>
  </div>
</template>

<script>
/***************************************** [ JAVASCRIPT ] */
import axios from 'axios';
import CorrBarChart from './CorrBarChart.vue';
import TransfmBarChart from './TransfmBarChart.vue';
const csv = require('csvtojson')

var myColors = {
  dark_orange:'rgba(250, 79, 49, 0.7)',
  orange: 'rgba(253,205,172, 1.0)',
  blue: 'rgba(203,213,232,0.7) ',
  pink: 'rgba(244,202,228, 0.7)',
  melon: 'rgba(230,245,201,0.7) ',
  green: 'rgba(179,226,205,0.7) ',
  yellow: 'rgba(255,242,174,0.7) ',
  beige: 'rgba(241,226,204,0.7) ',
  grey: 'rgba(204,204,204,0.7) ',
};

//const FEATURE_GRAPH_WIDTH='200px';
  export default {
    name: 'ModelDesignComp',
    components: {
      'CorrBarChart':CorrBarChart,
      'TransfmBarChart':TransfmBarChart,
    },
    data: () => ({
      dlResult: '',
      rawData:undefined,
      featureIdxs:undefined,
      slicedData:undefined,
      transformedData:undefined,
      modelParams:undefined,

      corrBarStyle:{
        width:'300px',
        height:'300px',
        label: "correlation bar chart",
      },
      transfmBarStyle:{
        width:'150px',
        height:'150px',
        label: "transformation bar chart",
      },
      picked: '',
      rules: [
        value => !!value || 'Required.',
        value => (value && value.length >= 3) || 'Min 3 characters',
      ],
      file: null,
      featureDataLoaded:false,
      featureBarChart: {
        labels: ['None'],
        datasets: [{
          label: 'None',
          backgroundColor: myColors.grey, //'#f87979',
          data: [10],
          }]
      },
      transfmDataLoaded:false,
      transfmBarChart: {
        labels: ['None'],
        datasets: [{
          label: 'None',
          backgroundColor: myColors.grey, //'#f87979',
          data: [10]
          }]
      },
    }),
    /***--------------------------
     * uploadDataFile
     * param   : data input 파일
     * return  : 상관계수 계산값
     * --------------------------*/
    methods: {
      setFeatureIdxs: function(arr) {
        this.featureIdxs = arr;
        console.log("SetFeatureIdxs Result: ",this.featureIdxs);

        this.featureIdxs.sort();
        console.log("FeatureIdxs Sorted Result: ",this.featureIdxs);
        var tempARR = this.rawData.map((el,index)=>{
          let tempEl=[];
          for(let i = 0;i<this.featureIdxs.length;i++)
          {
            if(index!=0)
              tempEl.push(Number(el[this.featureIdxs[i]]))
            else{
              tempEl.push(el[this.featureIdxs[i]])
            }
          }
          return tempEl;
        })    
        this.slicedData=tempARR;
        console.log("slicedData Result : ",this.slicedData)
      },
      uploadDataFile: function(e) {
        const reader = new FileReader();
        this.file = e.target.files[0];
        if (this.file.length==0)
          return;
        
        reader.onload = async (e) => {
          // SAVE origin file
          // READ -> calculate Pearson Correlation
          csv({
              noheader:true,
              output: "csv"
          })
          .fromString(e.target.result)
          .then((jsonObj)=>{
            this.rawData = jsonObj;
            console.log(this.rawData);
            axios.post('http://localhost:5000/calPC',{datas:jsonObj}).then((r)=>{
              console.log("r : " + r)
              let corr = JSON.parse(r.data)[0]
              
              this.featureDataLoaded = true;
              this.featureBarChart= {
                labels: Object.keys(corr),
                datasets: [
                  {
                    label: 'PCC',//Pearson Correlation Coefficient
                    backgroundColor: Array.from({length: Object.values(corr).length}, () => 'rgba(204,204,204,0.7)'),//'#f87979',
                    borderColor: myColors.dark_orange,
                    hoverBorderColor: myColors.blue,
                    data: Object.values(corr),
                    clickedBarIndexes:[],
                    updateFeatureIdxs:this.setFeatureIdxs,
                  }
                ],
              }
                console.log(corr)
              }).catch((e)=>console.log(e));
          })
        };
        reader.readAsText(this.file);
      },
      /***--------------------------
       * setTransformMode
       * param   : 선택된 transformation mode
       * return  : transformed data
       * --------------------------*/
      setTransformMode: function(e) {
        // SET Piceked Transform Mode
        var picked = e.target.defaultValue
        console.log("setTransformMode : " + picked)
        console.log(e.target)
        
        // GET Transformed Data
        axios.post('http://localhost:5000/getTD', 
                  { data:this.slicedData, mode:picked}).then((r) => {
          console.log("picked transform mode: " + picked)
          console.log("r.data : "  + r.data)
          
          this.transformedData = JSON.parse(r.data)//[0]
          this.transfmDataLoaded = true;
          this.transfmBarChart= {
            labels: Object.keys(this.transformedData),
            datasets: [
              {
                label: 'PCC',//Pearson Correlation Coefficient
                backgroundColor: myColors.grey,//'#f87979',
                borderColor: myColors.dark_orange,
                hoverBorderColor: myColors.blue,
                data: Object.values(this.transformedData),
              }
            ]
          }
          console.log(this.transformedData)
          // Transformation 그래프 찍기
          /*
          this.featureDataLoaded = true;
          this.featureBarChart= {
            labels: Object.keys(transform),
            datasets: [
              {
                label: 'Data One',
                backgroundColor: '#f87979',
                data: Object.values(transform),
              }
            ]
          }*/
        }).catch((e)=>console.log(e));
        
      },
      /***--------------------------
       * runDeepLearning
       * param   : 모든 선택 option
       * return  : 딥러닝 결과
       * --------------------------*/
      runDeepLearning: function() {
        // SET model input
        // GET deep learning result
        var temp = 0;
        console.log("runDeepLearning");
        axios.post('http://localhost:5000/runDL', {data:temp}).then((r) => { 
          console.log("r.data : "  + r.data) 
          
          // Result Component에 결과 찍기
        }).catch((e)=>console.log(e));
      },
      transformIconTest: function() {
        console.log("transformIconTest")
      },
      fileSelect() {
        document.getElementById("file_uploads").click()
      },
    }
  }
</script>

<style scoped scss>
/***************************************** [ CSS ] */
/* COMMON */
.NextArrow{
  width: 50px;
  height: 50px;
  margin: 10px;
}
.NextArrow img{
  width: 100%;
  height: 100%;
}
.ModelDesignContainer{
  display: flex;
  justify-content: space-evenly; /*center*/
  align-items: center;
  width: 1870px;
  height: 540px;
  margin-right: auto;
  margin-left: auto;
  margin-top: 25px;
  padding: 50px;
}
.ComponentTitle{
  width: 1870px;
  height: 20px;
  margin-left: auto;
  margin-top: 50px;
  color: rgb(128, 126, 126);
}
.WrapComponent{
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
  height: 500px !important; 
}
.CardComponent {
  height: 350px !important;
  padding: 5px;
  border-radius: 10px !important;
  background: rgb(2,56,88);
  /*background-color: rgba(236,231,242,0.8) !important;*/
}

/* MODULE_ETC */
.DataWrapComponent .StepName{
  color:#989595;
  font-style: oblique;
  font-size: 20pt;
}
.dataBtnComponent{
  align-items: right;
}

/* WRAP */
.DataWrap{
  width: 400px;
}
.FeatureWrap{
  width: 350px;
}
.TransformWrap{
  width:250px;
}
.ModelWrap{
  width:250px;
}

/* CARD */
.DataCard {
  width: 400px;
  padding: 10px;
}
.FeatureCard {
  display: flex;
  width: 350px !important;
  align-items: center;
  justify-content: center;
}
.FeatureGraph {
  width: 300px;
  height: 300px;
  display: flex;
  overflow-x: scroll;
  justify-content: center;
  align-items: center;
}
.TransformCard {
  width:250px;
  padding: 10px;
}
.ModelCard {
  width:250px;
}

/* LOAD */
.TransformLoad{
  padding: 10px;
}
.TransformRadio{
  padding-top: 20px;
  padding-left: 10px;
  padding-right: 10px;
}
.ModelLoad{
  padding: 10px;
}
</style>