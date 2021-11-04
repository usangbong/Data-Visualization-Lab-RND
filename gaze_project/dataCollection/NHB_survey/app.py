import json
import pandas as pd
import numpy as np
from flask import *
from flask_cors import CORS

app = Flask(__name__)
if __name__ == '__main__':
  app.jinja_env.auto_reload = True
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.run(debug=True)
CORS(app)

@app.route('/api/savedata', methods=['POST'])
def saveData():
  # print("/api/savedata")
  # print(request.form)
  response = {}
  try:
    SUBJECT_ID = request.form['SUBJECT_ID']
    SUBJECT_CELL = request.form['SUBJECT_CELL']
    SUBJECT_BIRTH = request.form['SUBJECT_BIRTH']
    SUBJECT_ED_LEVEL = request.form['SUBJECT_ED_LEVEL']
    SUBJECT_EYE_WEAK = request.form['SUBJECT_EYE_WEAK']
    SELECTED_AREA_ARR = request.form['SELECTED_AREA_ARR']
    LIKERT_SCORE_ARR = request.form['LIKERT_SCORE_ARR']
    SELECTED_REWARD = request.form['SELECTED_REWARD']
    EVENT_LOG = request.form['EVENT_LOG']
    
    DIR_LOCATION = "./data/"


    # print("SUBJECT_ID")
    # print(SUBJECT_ID)

    INFO_FILE_NAME = DIR_LOCATION+SUBJECT_ID+"_INFO"+".csv"
    # print(INFO_FILE_NAME)
    subject_info = [[SUBJECT_ID, SUBJECT_CELL, SUBJECT_BIRTH, SUBJECT_ED_LEVEL, SUBJECT_EYE_WEAK, SELECTED_REWARD]]
    subject_info_columns = ["id", "cell", "birth", "education", "colorweak", "reward"]
    subject_info_df = pd.DataFrame(subject_info, columns=subject_info_columns)
    # print(subject_info_df)
    subject_info_df.to_csv(INFO_FILE_NAME, index=False)

    LOG_FILE_NAME = DIR_LOCATION+SUBJECT_ID+"_LOG"+".csv"
    # print(LOG_FILE_NAME)
    LOG_SPLIT = EVENT_LOG.split(';')
    event_log = []
    event_log_columns = ["id", "event", "subevent", "stimulus", "colorindex", "time"]
    for _log in LOG_SPLIT:
      _logRowSplit = _log.split('|')
      # print(_logRowSplit)
      _l = [_logRowSplit[0], _logRowSplit[1], _logRowSplit[2], _logRowSplit[3], _logRowSplit[4], _logRowSplit[5]]
      event_log.append(_l)
    event_log_df = pd.DataFrame(event_log, columns=event_log_columns)
    # print(event_log_df)
    event_log_df.to_csv(LOG_FILE_NAME, index=False)

    AREA_FILE_NAME = DIR_LOCATION+SUBJECT_ID+"_AREA"+".csv"
    # print(AREA_FILE_NAME)
    AREA_SPLIT = SELECTED_AREA_ARR.split(';')
    area_data = []
    area_data_columns = ["stimulus", "selectindex", "ix", "iy", "ic", "colorindex"]
    stiIdx = 0
    # print(AREA_SPLIT)
    for _areaArr in AREA_SPLIT:
      _areaSplit = _areaArr.split('|')
      # print("_areaSplit")
      # print(_areaSplit)
      for _area in _areaSplit:
        down = _area.split('/')
        # print("down")
        # print(down)
        _idx = 0
        for _pixel in down:
          # print("_pixel")
          # print(_pixel)
          # print(_pixel.split(','))
          if _pixel == '':
            continue
          area_data.append([stiIdx, _idx, _pixel.split(',')[0], _pixel.split(',')[1], _pixel.split(',')[2], _pixel.split(',')[3]])
          _idx = _idx+1
      stiIdx = stiIdx+1
    area_data_df = pd.DataFrame(area_data, columns=area_data_columns)
    # print(area_data_df)
    area_data_df.to_csv(AREA_FILE_NAME, index=False)

    LIKERT_FILE_NAME = DIR_LOCATION+SUBJECT_ID+"_LIKERT"+".csv"
    # print(LIKERT_FILE_NAME)
    LIKERT_SPLIT = LIKERT_SCORE_ARR.split(';')
    likert_data = []
    likert_data_columns = ["stimulus", "colorindex", "score"]
    arrIdx = 0
    for _l in LIKERT_SPLIT:
      _rowSplit = _l.split('|')
      _idx = 0
      for _lp in _rowSplit:
        likert_data.append([arrIdx, _idx, _lp])
        _idx = _idx+1
      arrIdx = arrIdx+1
    likert_data_df = pd.DataFrame(likert_data, columns=likert_data_columns)
    # print(likert_data_df)
    likert_data_df.to_csv(LIKERT_FILE_NAME, index=False)
    

    response['status'] = 'success'
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  return json.dumps(response)


