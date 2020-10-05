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
        var _td = []
        var _getData = {
          featureType: response.data[0],
          stimulusClass: response.data[1],
          stimulusName: response.data[2],
          spValue: response.data[3]
        };
        _td.push(_getData);

        this.setState({
          tableData: 
            _td
        });
        var _t = [];
        var _vv = {make: "Toyota", model: "Celica", price: 35000};
        _t.push(_vv);
        _vv = {make: "Ford", model: "Mondeo", price: 32000};
        _t.push(_vv);
        _vv = {make: "Porsche", model: "Boxter", price: 72000};
        _t.push(_vv);
        _vv = {make: "Toyota", model: "Celica", price: 35000};
        _t.push(_vv);
        this.setState({
          rowData:
            _t
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

          <div className="ag-theme-alpine" style={ { height: 400, width: 800 } }>
            <AgGridReact
              rowData={tableData}>
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
