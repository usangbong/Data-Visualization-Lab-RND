import './DataSetting.scoped.scss';
import Slider from 'rc-slider';

function DataSetting() {
  return (
    <div className="DataSetting">
      <div className="Title">DataSetting</div>
      <div className="SettingTimeLength">
        Time Length
        <div className="SilderWrap">
        <Slider min={0} max={24} />
      </div>
      </div>
      <div className="SettingGraph">
        <div className="THBOX">
          <div>Graph Type</div>
          <div>Data</div>
        </div>
        <div className="TBODYBOX">
        <div className="SelectBox_code_1">
          <div>
            <input type="radio" id="Line" name="d4" defaultChecked={true}/>
            <label htmlFor="Line">Line</label>
          </div>
          <div>
            <input type="radio" id="Histogram" name="d4" />
            <label htmlFor="Histogram">Histogram</label>
          </div>
          <div>
            <input type="radio" id="Density" name="d4" />
            <label htmlFor="Density">Density</label>
          </div>
          <div>
            <input type="radio" id="Scatter" name="d4" />
            <label htmlFor="Scatter">Scatter</label>
          </div>
            </div>
            <div className="ValueBox_code_1">
            <div>
            <input type="radio" id="Raw" name="d5" />
            <label htmlFor="Raw">Raw</label>
            </div>
            <div>
              <input type="radio" id="Preprocessed" name="d5" />
              <label htmlFor="Preprocessed">Preprocessed</label>
            </div>
            <div>
              <input type="radio" id="Deleted" name="d5" />
              <label htmlFor="Deleted">Deleted</label>
            </div>
            </div>
        </div>
        </div>

    </div>
  );
}

export default DataSetting;
