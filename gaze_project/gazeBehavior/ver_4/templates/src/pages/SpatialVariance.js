import React, { useState } from 'react';
import axios from 'axios';
import { AgGridColumn, AgGridReact } from 'ag-grid-react';

import '../../node_modules/ag-grid-enterprise';
import '../../node_modules/ag-grid-community/dist/styles/ag-grid.css';
import '../../node_modules/ag-grid-community/dist/styles/ag-theme-alpine.css';

class SpatialVariance extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      tableData: [{
        userID: '',
        featureType: '',
        stimulusClass: '',
        stimulusName: '',
        spValue: ''
      }], 
      rowData: []
    };
  }

  componentDidMount() {
    axios.get(`http://${window.location.hostname}:5000/static/output/spatial_variance.json`)
      .then(response => {
        var _data = response.data; 
        console.log(_data);
        var _getData = [];
        for(var i=0; i<_data.length; i++){
          var _row = {
            userID: response.data[i][0],
            featureType: response.data[i][1],
            stimulusClass: response.data[i][2],
            stimulusName: response.data[i][3],
            spValue: response.data[i][4]
          };
          _getData.push(_row);
        }
        
        this.setState({
          tableData: 
          _getData
        });
      });
  }

  render() {
    const {gridApi, setGridApi} = this.state;
    const {gridColumnApi, setGridColumnApi} = this.state;
    const {rowData, setRowData} = this.state; 
      
    const { tableData } = this.state;

    // function onGridReady(params) {
    //     setGridApi(params.api);
    //     setGridColumnApi(params.columnApi);
    // }
    
    return (
      <>
        <div className="page-header">
          <h1>Spatial Variance</h1>
        </div>
        
        <div className="page-section">
          <p>{this.state.spRes}</p>

          <div style={{margin: '10px 0'}}>
            <button>A</button>
          </div>
          <div style={{margin: '10px 0'}}>
            <button>B</button>
          </div>
          <div style={{margin: '10px 0'}}>
            <button>C</button>
          </div>
          <div style={{margin: '10px 0'}}>
            <button>D</button>
          </div>
          <div style={{margin: '10px 0'}}>
            <button>E</button>
          </div>

          <div className="ag-theme-alpine" style={ { height: 600, width: 900 } }>
            <AgGridReact
              rowData={tableData}>
              <AgGridColumn field="userID"></AgGridColumn>
              <AgGridColumn field="featureType"></AgGridColumn>
              <AgGridColumn field="stimulusClass"></AgGridColumn>
              <AgGridColumn field="stimulusName"></AgGridColumn>
              <AgGridColumn field="spValue"></AgGridColumn>
            </AgGridReact>
          </div>
        </div>
      </>
    );
  }
}

export default SpatialVariance;
