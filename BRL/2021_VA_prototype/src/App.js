import './App.css';
import React,{useState,useRef,useEffect} from "react";
import Unity, { UnityContext } from "react-unity-webgl";
import TimeLine from './page/TimeLine';
import Dashboard from './page/Dashboard';
import History from './page/History';
import PageHeader from './page/PageHeader';

//import CHART from './component/CHART';

const unityContext = new UnityContext({
  loaderUrl: "Build/test.loader.js",
  dataUrl: "Build/test.data",
  frameworkUrl: "Build/test.framework.js",
  codeUrl: "Build/test.wasm",
});



const dynamics = ['풍향풍속계','지진계','지진 가속도계','동적 변형률계','케이블 가속도계','가속도계']

function App() {
  const [Seconds, Seconds_on] = useState(0)
  const [PlayHook, PlayHook_on] = useState(false)
  const [dynamic_graphs, dynamic_graphs_change] = useState([]);
  const [checked_types, checked_types_change] = useState('');
  const [check_yeol, check_yeol_on] = useState(false)
  
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

    

    /*
    console.log(renderRef)
    let C = renderRef.current.htmlCanvasElementReference.GLctxObject.GLctx;
    console.log(C)
    var cvs = document.getElementsByClassName('overview')[0];
    var gl = cvs.getContext('webgl2',{preserveDrawingBuffer: true})
  

    let unit8 = new Uint16Array(cvs.width * cvs.height * 4);
    gl.readPixels (0, 0, cvs.width, cvs.height, gl.RGBA, gl.UNSIGNED_SHORT, unit8);

    // clone canvas generation
    var create_clone = document.createElement ("canvas");
    create_clone.id = "clone_canvas";
    create_clone.width = cvs.width;
    create_clone.height = cvs.height;
    // Clone Element
    var clone_canvas = create_clone;
    var context_clone = clone_canvas.getContext ("2d");
    // Create ImageData and putImage
    var img_data = {
        data: unit8,
        height: cvs.height,
        width: cvs.width
    };
    var tmpimgdata = new ImageData(unit8,cvs.width);
    console.log(tmpimgdata);
    context_clone.putImageData (tmpimgdata, 0, 0);
    // Imaging with toDataURL
    var canvas_img = clone_canvas.toDataURL ();
    console.log(canvas_img);
    */
    historyRef.current.addHistory(renderRef.current.htmlCanvasElementReference.toDataURL());

  }

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
            <Unity ref={renderRef} className="overview" unityContext={unityContext} />
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
