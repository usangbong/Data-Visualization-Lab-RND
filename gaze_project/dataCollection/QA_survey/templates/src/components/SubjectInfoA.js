import React from 'react';
import Select from 'react-select';

const OPT_ED_LEVEL=[
  {value: 'opt_ed_level1', label: '중학교 졸업'}, 
  {value: 'opt_ed_level2', label: '고등학교 졸업'}, 
  {value: 'opt_ed_level3', label: '학사학위 취득'}, 
  {value: 'opt_ed_level4', label: '석사학위 취득'}, 
  {value: 'opt_ed_level5', label: '박사학위 취득'}, 
  {value: 'opt_ed_level6', label: '기타'} 
];

const OPT_EYE_COLOR_WEAK=[
  {value: 'opt_color_w1', label: '없음'}, 
  {value: 'opt_color_w2', label: '전색맹'}, 
  {value: 'opt_color_w3', label: '적록 색맹'}, 
  {value: 'opt_color_w4', label: '황청 색맹'}, 
  {value: 'opt_color_w5', label: '적록 색약'}, 
  {value: 'opt_color_w6', label: '황청 색약'}, 
  {value: 'opt_color_w7', label: '기타'}, 
];


class SubjectInfoA extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      SUBJECT_NAME: null,
      SUBJECT_AGE: 0,
      SUBJECT_ED_LEVEL: null,
      SUBJECT_EYE_COLOR_W: "opt_color_w1",
    };
  }

  onChange_subject_ed_level = SUBJECT_ED_LEVEL =>{
    this.setState({SUBJECT_ED_LEVEL});
  }
  onChange_subject_eye_color_weak = SUBJECT_EYE_COLOR_W =>{
    this.setState({SUBJECT_EYE_COLOR_W});
  }

  onChange_subject_name =(e)=>{
    this.setState({
      SUBJECT_NAME:e.target.value
    });
  }

  onChange_subject_age =(e)=>{
    this.setState({
      SUBJECT_AGE:e.target.value
    });
  }
  
  onSubmit_subject_info_A =()=>{
    console.log(this.state.SUBJECT_NAME);
    console.log(this.state.SUBJECT_AGE);
    console.log(this.state.SUBJECT_ED_LEVEL);
    console.log(this.state.SUBJECT_EYE_COLOR_W);
  }

  
  render() {
    const {SUBJECT_NAME, SUBJECT_AGE, SUBJECT_ED_LEVEL, SUBJECT_EYE_COLOR_W} = this.state;

    return (
      <div className="bodyContDiv">
        이름: 
        <input 
          type="text" 
          name="subjectName" 
          onCompositionEnd={this.onChange_subject_name}
        />
        <br></br>
        만나이: 
        <input 
          type="text" 
          name="subectAge"
          onChange={this.onChange_subject_age}
        />
        <br></br>
        최종학력: 
        <Select 
          value={SUBJECT_ED_LEVEL} 
          placeholder="최종학력을 선택해주세요"
          options={OPT_ED_LEVEL}
          onChange={this.onChange_subject_ed_level}
        />
        <br></br>
        색각 이상 증상:
        <Select 
          value={SUBJECT_EYE_COLOR_W} 
          placeholder="색각 이사 증상을 선택해주세요"
          options={OPT_EYE_COLOR_WEAK}
          onChange={this.onChange_subject_eye_color_weak}
        />
        <br></br>
        <button onClick={this.onSubmit_subject_info_A}>저장</button>
      </div>
    );
  }
}

export default SubjectInfoA;
