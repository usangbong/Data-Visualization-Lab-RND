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
    SEGMENTATION_ARR_STRING = request.form['seg_arr']
    IMAGE_URL = request.form['img_url']
    IMAGE_WIDTH = int(request.form['img_width'])
    IMAGE_HEIGHT = int(request.form['img_height'])
    DIV_VAL = 10
    DIR_LOCATION = "./data/"
    CSV_PATH = DIR_LOCATION+IMAGE_URL.split('stimuli/')[1].split('.')[0]+".csv"

    # print(SEGMENTATION_ARR_STRING)
    SEGMENTATION_ARR_ROWS = SEGMENTATION_ARR_STRING.split("/")
    SEGMENTATION_ARR_ROWS.remove('')
    # print('SEGMENTATION_ARR_ROWS')
    # print(SEGMENTATION_ARR_ROWS)
    SEGMENTATION_ARR = []
    for _cells in SEGMENTATION_ARR_ROWS:
      # print('_cells')
      # print(_cells)
      vals = _cells.split("|")
      for _cell in vals:
        _spVal = _cell.split(",")
        # print('_spVal')
        # print(_spVal)
        _x = int(_spVal[0])
        _y = int(_spVal[1])
        _label = int(_spVal[2])+1
        SEGMENTATION_ARR.append([_x, _y, _label])
    # print("SEGMENTATION_ARR")
    # print(SEGMENTATION_ARR)

    gridArr = []
    for _i in range(0, int(IMAGE_HEIGHT/DIV_VAL)):
      _row = []
      for _j in range(0, int(IMAGE_WIDTH/DIV_VAL)):
        _row.append(0)
      gridArr.append(_row)
    
    for _cell in SEGMENTATION_ARR:
      _x = _cell[0]
      _y = _cell[1]
      _label = _cell[2]
      gridArr[_y][_x] = _label
    
    grid_df = pd.DataFrame(gridArr)
    # print(gridArr)
    grid_df.to_csv(CSV_PATH, header=False, index=False)

    response['status'] = 'success'
  except Exception as e:
    response['status'] = 'failed'
    response['reason'] = e
    print(e)
  return json.dumps(response)


