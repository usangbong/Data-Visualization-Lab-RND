import React from 'react';

class Aggrement extends React.Component {
  
  render() {
    return (
      <div className="bodyContDiv">
        <h3>1 개인정보 수집 항목 및 수집 이용 목적</h3>
        <h3>가) 수집 항목(필수항목)</h3>
        <div className="h4TextDiv">- 생년, 최종학력, 색각이상증상 여부, 연락처</div>
        <h3>나) 수집 및 이용 목적</h3>
        <div className="h4TextDiv">- 수집된 데이터 분석을 이용한 논문 작성, 리워드 제공을 위한 활용</div>
        <h3>2 개인정보 보유 및 이용기간</h3>
        <div className="h4TextDiv">2.1 리워드 제공을 위한 개인정보(연락처)는 리워드 제공 후 30일 이내에 제거합니다.</div>
        <div className="h4TextDiv">2.2 수집 데이터 구분을 위한 개인정보(성명, 생년)는 비식별화 과정을 거친 뒤 30일 이내에 제거합니다.</div>
        <div className="h4TextDiv">- 위 2.1항과 2.2항 정보를 제외한 논문 작성을 위해 수집한 설문 조사 데이터는 세종대학교 데이터 시각화 연구실에 영구 보관 됩니다.</div>
        <h3>3 동의거부관리</h3>
        <div className="h4TextDiv">- 귀하께서는 본 안내에 따른 개인정보 수집, 이용에 대하여 동의를 거부하실 권리가 있습니다. 다만, 귀하가 개인정보의 수집 이용에 동의를 거부하시는 경우 설문 참여 및 리워드 제공이 불가능함을 알려드립니다.</div>
        <div className="h4TextDiv">본 설문에서 수집한 개인정보는 연구 목적 이외에 사용하지 않습니다.</div>
        <div className="h4RedTextDiv">개인정보 수집 및 이용에 동의하신다면 아래의 다음 버튼을 눌러주세요.</div>
        <div className="h4RedTextDiv">크롬(Chrome), 엣지(Edge), 웨일 브라우저를 사용할 수 있습니다.</div>
      </div>
    );
  }
}

export default Aggrement;
