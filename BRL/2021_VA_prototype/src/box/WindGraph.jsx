import React, {useState,useEffect,useRef} from 'react';
import './WindGraph.scoped.scss';

function WindGraph(props) {
  
  const [chart_data, chart_data_on] = useState([]);
  const [chart_options, chart_options_on] = useState({});
  const [preMins, MINS_on] = useState(0);
  const {NAME,VALUES,MINS} = props;
  const nameInput = useRef();
  const image = document.getElementById('source');

  //wd_rad = df.pop('wd (deg)')*Math.PI/180
  //df['max Wx'] = max_wv*np.cos(wd_rad)
  //df['max Wy'] = max_wv*np.sin(wd_rad)

  const VectorWind = (Degree)=>{
    let tmp = (Degree*Math.PI/180);
          
          return [Math.cos(tmp),Math.sin(tmp)]
  }

  useEffect(()=>{
    let cvx = nameInput.current.getContext('2d');
    let tmpDS = VectorWind(VALUES[MINS]);
    cvx.clearRect(0, 0, nameInput.current.width, nameInput.current.height);
    
    cvx.translate(nameInput.current.width / 2, nameInput.current.height / 2);
    //cvx.rotate((VALUES[MINS]*Math.PI/180));
    cvx.strokeStyle = 'rgba(255, 0, 0, 1.0)';
    cvx.beginPath();
    cvx.moveTo(0,0);
    cvx.lineTo(100*tmpDS[0],100*tmpDS[1]);
    cvx.stroke();
    
    //cvx.rotate(-(VALUES[MINS]*Math.PI/180));
    cvx.translate(-nameInput.current.width / 2, -nameInput.current.height / 2);

  },[props.MINS]);

  return (
    <div className="WindGraph">
      <img alt='' className="bangImg" src={'images/4bang.png'}></img>
      <canvas ref={nameInput} className="WGC">

      </canvas>
    </div>
  );
}

export default WindGraph;
