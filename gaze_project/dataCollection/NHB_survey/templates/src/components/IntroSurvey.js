import React from 'react';

const IntroSurvey=(props)=>{
  const {surveyStep, colorArray} = props;
  return (
    <>
    <h3 className="centerHigh">정보가 많거나 알아보기(인식하기) 쉬울수록 강한 의미가 있는 물체 혹은 영역입니다.</h3>
    { surveyStep == 0 &&
      <h3 className="center">이미지에서 의미있는 영역을 선택하세요(클릭 혹은 드래그로 가능).</h3>
    }
    { surveyStep == 1 &&
      <h3 className="center">선택한 영역이 얼마나 의미가 있는지 점수를 주세요.</h3>
    }
    { surveyStep == 1 &&
      <h3 className="centerHigh">{colorArray.length}개의 영역을 선택했습니다. 최소 5개의 영역을 선택해주세요.</h3>
    }
    { surveyStep == 1 &&
      <h3 className="center">다른 영역을 추가로 선택하기 위해서는 '영역 추가 선택' 버튼을 눌러주세요.</h3>
    }
    { surveyStep == 2 &&
      <h3 className="center">이미지에서 추가할 영역을 선택하세요(클릭 혹은 드래그로 가능)</h3>
    }
    { surveyStep == 3 &&
      <h3 className="center">선택한 영역이 얼마나 의미가 있는지 점수를 주세요.</h3>
    }
    { surveyStep == 3 &&
      <h3 className="centerHigh">{colorArray.length}개의 영역을 선택했습니다. 최소 5개의 영역을 선택해주세요.</h3>
    }
    { surveyStep == 3 &&
      <h3 className="center">다른 영역을 추가로 선택하기 위해서는 '영역 추가 선택' 버튼을 눌러주세요.</h3>
    }
    { colorArray.length >= 5 &&
      <h3 className="center">다음 페이지로 넘어가기를 원하시면 하단의 '다음' 버튼을 눌러주세요.</h3>
    }
      
    </>
  );
}

export default IntroSurvey;
