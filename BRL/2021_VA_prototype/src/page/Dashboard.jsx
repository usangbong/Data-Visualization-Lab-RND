import './Dashboard.scoped.scss';
import React, {useState, useEffect} from "react";
import DataSelection from '../component/DataSelection';
import DataSetting from '../component/DataSetting';
import SimulateModel from '../component/SimulateModel';
import ExternalData from '../component/ExternalData';
import StaticGraphs from '../component/StaticGraphs';
import DynamicGraphs from '../component/DynamicGraphs';

import PageHeader from './PageHeader';

import axios from 'axios';

function Dashboard(props) {
  const [static_value, static_value_change] = useState({});
  const [static_checks, static_checks_change] = useState([]);

  const [dynamic_value, dynamic_value_change] = useState({});



  const static_check_update = (value) => {
    console.log(value);
    static_checks_change(value)
  }


  useEffect(()=>{
    axios.get('http://localhost:3000/api/data/static/').then((tes)=>{
      static_value_change(tes.data)
    })

    axios.get('http://localhost:3000/api/data/dynamic/').then((res)=>{
      dynamic_value_change(res.data)
    })
  }
  ,[]);

  useEffect(()=>{
    console.log('static',static_value);
  }
  ,[static_value]);

  useEffect(()=>{
    console.log('dynamic',dynamic_value);
  }
  ,[dynamic_value]);


  return (
    <div className="Dashboard">
      <div className="SocketG" >
      
      <DynamicGraphs 
      check_yeol={props.check_yeol}
      PlayHook={props.PlayHook}
      Seconds={props.Seconds}
      dynamic_graphs={props.dynamic_graphs}
      dynamic_value={dynamic_value}
      ></DynamicGraphs>
      
      <StaticGraphs 
      PlayHook={props.PlayHook}
      Seconds={props.Seconds}
      static_checks={static_checks}
      static_value={static_value}
      ></StaticGraphs>

      </div>
      

      <div className="Dashboard_H">
      <PageHeader msg={'Dashboard'} ></PageHeader>
      </div>
      <DataSelection 
      SpawnEnemies={props.SpawnEnemies}></DataSelection>
      <DataSetting></DataSetting>
      <SimulateModel></SimulateModel>
      <ExternalData static_check_update={static_check_update}></ExternalData>
    </div>
  );
}

export default Dashboard;
