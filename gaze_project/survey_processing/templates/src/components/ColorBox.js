import React, { useEffect } from 'react';
// import Select from 'react-select';

import ColorPoint from './ColorPoint';


const ColorBox =(props)=>{
  const { colorArray, selectedColorIdx, selectedArea, colorAddFunction, restBtnFunction, updateColorIndex } = props;
  const genColorBoxDivs =()=>{
    let divArr = [];
    for(let i=0; i<colorArray.length; i++){
      divArr.push(<ColorPoint divClassName={".colorBoxArea"} colorArray={colorArray} selectedColor={i} selectedColorIdx={selectedColorIdx} heightVal={22} selectedColorUpdate={updateColorIndex} key={i}/>);
    }
    return divArr;
  }

  function onClick_colorAdd_button(){
    if(selectedArea.length == selectedColorIdx+1){
      if(selectedColorIdx==0){
        if(selectedArea[selectedColorIdx].length == 0){
          alert("Plz press this button after area selecting");
        }else{
          colorAddFunction();
        }
      }else{
        colorAddFunction();
      }
    }
  }

  function onClick_colorReset_button() {
    let initAnswer = window.confirm("이 페이지에서의 기록이 지워집니다.");
    if(initAnswer){
      // loging
      restBtnFunction();
    }
  }
  
  
  useEffect(() => {
    if(selectedColorIdx !== null)
      return
    
    
}, [ props.selectedColorIdx ]);
  
  return (
    <>
      <div className="btnColorDiv">
        <div className="btnArea">
          <button onClick={onClick_colorAdd_button}>Add</button>
          <button onClick={onClick_colorReset_button}>Reset</button>
        </div>
        <div className="colorBoxArea">
          {genColorBoxDivs()}
        </div>
      </div>
    </>
  );
}

export default ColorBox;