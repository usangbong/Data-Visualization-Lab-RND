import React from 'react';

const IntroMeaning=()=>{
  return (
    <>
      <h2 className="center">설문 참가자는 이미지에서 의미있는 물체 혹은 영역을 찾아야합니다.</h2>
      <br></br>
      <div className="h4Bold">의미는 주관적인 개념이므로 정해진 정답은 없습니다.</div>
      <div className="textDiv">
        <div className="h4TextDiv">하지만, 설문의 목적은 이미지에서&nbsp;</div>
        <div className="h4RedTextDiv">눈에 띄는</div>
        <div className="h4TextDiv">&nbsp;곳을 찾는 것이&nbsp;</div>
        <div className="h4RedTextDiv">아니므로</div>
        <div className="h4TextDiv">&nbsp;아래의 설명을 참고 부탁드립니다.</div>
      </div>
      <div className="h4RedTextDiv">반드시 아래의 설명을 숙지한 상태에서 설문을 진행해주세요.</div>
      <div className="textDiv">
        <div className="h4TextDiv">다시 한 번 강조 하자면, 설문의 목적은 이미지에서&nbsp;</div>
        <div className="h4RedTextDiv">"의미 있는 영역"</div>
        <div className="h4TextDiv">을 찾는 것입니다.</div>
      </div>
    </>
  );
}

export default IntroMeaning;
