import './App.css';
import './XeoBIM.css';
import React,{useState,useRef,useEffect} from "react";
import Unity, { UnityContext } from "react-unity-webgl";
import TimeLine from './page/TimeLine';
import Dashboard from './page/Dashboard';
import History from './page/History';
import PageHeader from './page/PageHeader';

import {Server, BIMViewer} from '@xeokit/xeokit-bim-viewer';
import tippy from 'tippy.js';

let colormap = require('colormap')


//import CHART from './component/CHART';

const unityContext = new UnityContext({
  loaderUrl: "Build/test.loader.js",
  dataUrl: "Build/test.data",
  frameworkUrl: "Build/test.framework.js",
  codeUrl: "Build/test.wasm",
  preserveDrawingBuffer: true,
});



const dynamics = ['풍향풍속계','지진계','지진 가속도계','동적 변형률계','케이블 가속도계','가속도계']

function App() {
  const [Seconds, Seconds_on] = useState(0)
  const [PlayHook, PlayHook_on] = useState(false)
  const [dynamic_graphs, dynamic_graphs_change] = useState([]);
  const [checked_types, checked_types_change] = useState('');
  const [check_yeol, check_yeol_on] = useState(false);
  const [picked_list, picked_list_change] = useState([]);
  
  const historyRef = useRef();
  const renderRef = useRef();

  const secondUpdate=(val)=>{
    Seconds_on(val)
  }
  const PlayHookUpdate=(val)=>{
    PlayHook_on(val)
  }

  const spawnEnemies = (checked_types)=>{
    console.log(checked_types)
    checked_types_change(checked_types)
    

  };

  useEffect(()=>{
    console.log(checked_types)
    unityContext.send("Object Manager", "ManageVisibilityJS", checked_types);
  },[checked_types]);


  useEffect(()=>{
    window.picked_list = [];
    window.picked_colormap = colormap({
        colormap: 'blackbody',
        nshades: 100,
        format: 'float',
        alpha: 1
    });
    const requestParams = getRequestParams();

        // Project to load into the viewer
        const projectId = requestParams.projectId;
        if (!projectId) {
            return;
        }

        // Open the explorer tab?
        const openExplorer = requestParams.openExplorer;
        setExplorerOpen(openExplorer === "true");

        const enableEditModels = (requestParams.enableEditModels === "true");

        // Server client will load data from the file systems
        const server = new Server({
            dataDir: "./data"
        });

        // Create  BIMViewer that loads data via the Server
        const bimViewer = new BIMViewer(server, {
            canvasElement: document.getElementById("myCanvas"), // WebGL canvas
            explorerElement: document.getElementById("myExplorer"), // Left panel
            toolbarElement: document.getElementById("myToolbar"), // Toolbar
            navCubeCanvasElement: document.getElementById("myNavCubeCanvas"),
            busyModelBackdropElement: document.getElementById("myViewer"),
            enableEditModels: enableEditModels
        });

        // Create tooltips on various HTML elements created by BIMViewer
        tippy('[data-tippy-content]', {
            appendTo: function () {
                return document.querySelector('#myViewer')
            }
        });

        // Configure our viewer
        bimViewer.setConfigs({});

        // Log info on whatever objects we click with the BIMViewer's Query tool
        bimViewer.on("queryPicked", (event) => {
            console.log("queryPicked: " + JSON.stringify(event, null, "\t"));
        });

        bimViewer.on("addModel", (event) => { // "Add" selected in Models tab's context menu
            console.log("addModel: " + JSON.stringify(event, null, "\t"));
        });

        bimViewer.on("editModel", (event) => { // "Edit" selected in Models tab's context menu
            console.log("editModel: " + JSON.stringify(event, null, "\t"));
        });

        bimViewer.on("deleteModel", (event) => { // "Delete" selected in Models tab's context menu
            console.log("deleteModel: " + JSON.stringify(event, null, "\t"));
        });

        //--------------------------------------------------------------------------------------------------------------
        // Process page request params, which set up initial viewer state
        //--------------------------------------------------------------------------------------------------------------

        // Viewer configurations
        const viewerConfigs = requestParams.configs;
        if (viewerConfigs) {
            const configNameVals = viewerConfigs.split(",");
            for (let i = 0, len = configNameVals.length; i < len; i++) {
                const configNameValStr = configNameVals[i];
                const configNameVal = configNameValStr.split(":");
                const configName = configNameVal[0];
                const configVal = configNameVal[1];
                bimViewer.setConfig(configName, configVal);
            }
        }

        // Load a project
        bimViewer.loadProject(projectId, () => {

                // The project may load one or models initially.

                // Withe request params, we can also specify:
                //  - models to load
                // - explorer tab to open


                const modelId = requestParams.modelId;
                if (modelId) {
                    bimViewer.loadModel(modelId);
                }

                const tab = requestParams.tab;
                if (tab) {
                    bimViewer.openTab(tab);
                }

                //
                window.setInterval((function () {
                    var lastHash = "";
                    return function () {
                        const currentHash = window.location.hash;
                        if (currentHash !== lastHash) {
                            parseHashParams();
                            lastHash = currentHash;
                        }
                    };
                })(), 200);
            },
            (errorMsg) => {
                console.error(errorMsg);
            });

        function getRequestParams() {
            var vars = {};
            window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, (m, key, value) => {
                vars[key] = value;
            });
            return vars;
        }

        function parseHashParams() {
            const params = getHashParams();
            const actionsStr = params.actions;
            if (!actionsStr) {
                return;
            }
            const actions = actionsStr.split(",");
            if (actions.length === 0) {
                return;
            }
            for (var i = 0, len = actions.length; i < len; i++) {
                const action = actions[i];
                console.log(action);
                switch (action) {
                    case "focusObject":
                        const objectId = params.objectId;
                        if (!objectId) {
                            console.error("Param expected for `focusObject` action: 'objectId'");
                            break;
                        }
                        bimViewer.setAllObjectsSelected(false);
                        bimViewer.setObjectsSelected([objectId], true);
                        bimViewer.flyToObject(objectId, () => {
                            // FIXME: Showing objects in tabs involves scrolling the HTML within the tabs - disable until we know how to scroll the correct DOM element. Otherwise, that function works OK

                            // bimViewer.showObjectInObjectsTab(objectId);
                            // bimViewer.showObjectInClassesTab(objectId);
                            // bimViewer.showObjectInStoreysTab(objectId);
                        });
                        break;
                    case "focusObjects":
                        const objectIds = params.objectIds;
                        if (!objectIds) {
                            console.error("Param expected for `focusObjects` action: 'objectIds'");
                            break;
                        }
                        const objectIdArray = objectIds.split(",");
                        bimViewer.setAllObjectsSelected(false);
                        bimViewer.setObjectsSelected(objectIdArray, true);
                        bimViewer.viewFitObjects(objectIdArray, () => {
                        });
                        break;
                    case "clearFocusObjects":
                        bimViewer.setAllObjectsSelected(false);
                        bimViewer.viewFitAll();
                        // TODO: view fit nothing?
                        break;
                    case "openTab":
                        const tabId = params.tabId;
                        if (!tabId) {
                            console.error("Param expected for `openTab` action: 'tabId'");
                            break;
                        }
                        bimViewer.openTab(tabId);
                        break;
                    default:
                        console.error("Action not supported: '" + action + "'");
                        break;
                }
            }
        }

        function getHashParams() {
            const hashParams = {};
            let e;
            const a = /\+/g;  // Regex for replacing addition symbol with a space
            const r = /([^&;=]+)=?([^&;]*)/g;
            const d = function (s) {
                return decodeURIComponent(s.replace(a, " "));
            };
            const q = window.location.hash.substring(1);
            while (e = r.exec(q)) {
                hashParams[d(e[1])] = d(e[2]);
            }
            return hashParams;
        }

        function setExplorerOpen(explorerOpen) {
            const toggle = document.getElementById("explorer_toggle");
            if (toggle) {
                toggle.checked = explorerOpen;
            }
        }

        var lastEntity = null;

        bimViewer.viewer.scene.input.on("dblclick", (coords) =>{
    
            let hit = bimViewer.viewer.scene.pick({
                canvasPos: coords
            });
    
            if (hit) {
                    hit.entity.picked = true;
                    hit.entity.colorize = [0.3,0.7,0.5];
                    window.picked_list.push(
                        {
                            oid:hit.entity.id,
                            val:Math.floor(Math.random() * 100),
                            a:window.picked_list.length%2==1?true:false,
                        });
                    console.log(hit.entity.id)
                    console.log(window.picked_list)
            } 
            /*
            else {
    
                if (lastEntity) {
                    lastEntity.selected = false;
                    lastEntity = null;
                }
            }
            */
        });

        window.bimViewer = bimViewer; // For debugging
  },[]);


  unityContext.on("clickElement", (element) => {
    console.log(typeof(element));
    if(dynamics.includes(element)){
      console.log(element);
      spawnEnemies(checked_types);
    }
    else{
      check_yeol_on(true);
    }
    //
  });
  
  unityContext.on("setScreenCoord", (coordArray) => {
    let sel_sensor = coordArray.filter((el)=>el[3]===1);
    dynamic_graphs_change(sel_sensor.map((el)=>{return el[2]}))
  });

  const SaveHistory=()=>{
    historyRef.current.addHistory(renderRef.current.htmlCanvasElementReference.toDataURL());

  }

  /*
  <Unity ref={renderRef} className="overview" unityContext={unityContext} />
  
  */

  return (
    <div className="containerWrap">
      <div className="container">
        <div className="content">
          <div className="dashboard">
          <Dashboard  
          check_yeol={check_yeol}
          PlayHook={PlayHook}
          Seconds={Seconds}
          SpawnEnemies={spawnEnemies}
          dynamic_graphs={dynamic_graphs}
          dynamic_graphs_change={dynamic_graphs_change}
          >
          
          </Dashboard>
          </div>
          {//CHART></CHART>
          }
          <div className="overviewWrap">
            <PageHeader msg={'Overview'} ></PageHeader>
            <input type="checkbox" id="explorer_toggle"/>
            <label for="explorer_toggle" class="explorer_toggle_label xeokit-btn fas fa-2x fa-sitemap" data-tippy-content="Toggle explorer panel"></label>
            <div id="myExplorer"></div>
            <div id="myToolbar"></div>
            <div id="myViewer">
                <canvas id="myCanvas"></canvas>
            </div>
            <canvas id="myNavCubeCanvas"></canvas>
          </div>
        </div>
        <div className="timeline">
        <TimeLine 
        PlayHookUpdate={PlayHookUpdate}
        secondUpdate={secondUpdate}></TimeLine>
        </div>
      </div>
      <div className="history">
      <History ref={historyRef} SaveHistory={SaveHistory} />
      </div>
    </div>
  );
}

export default App;
