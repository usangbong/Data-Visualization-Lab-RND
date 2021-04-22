import pandas as pd
import json

if __name__ == "__main__":
  traffic_data = {}

  with open("../../public/data/traffic_data.json", "r", encoding='utf-8') as jsonFile:
    traffic_data = json.load(jsonFile)

  colume = [""]
  time_list = []
  converted_data_speed = {}
  converted_data_volume = {}

  first = True
  for key, data in traffic_data.items():
    colume.append(key)
    converted_data_speed[key] = []
    converted_data_volume[key] = []
    for i in range(len(data["traffic"])):
      if first:
        time_list.append(data["traffic"][i]["time"])

      converted_data_speed[key].append(data["traffic"][i]["avs"])
      converted_data_volume[key].append(data["traffic"][i]["volume"])

    if first:
      first = False

  df_avs = pd.DataFrame(columns=colume)
  df_vol = pd.DataFrame(columns=colume)
  df_avs[""] = time_list
  df_vol[""] = time_list
  for key in colume:
    if key != "":
      df_avs[key] = converted_data_speed[key]
      df_vol[key] = converted_data_volume[key]

  store_avs = pd.HDFStore('./dcrnn/data/dataset_avs.h5')
  store_vol = pd.HDFStore('./dcrnn/data/dataset_vol.h5')
  store_avs.put('data', df_avs, format='table', data_columns=True)
  store_vol.put('data', df_avs, format='table', data_columns=True)
  store_avs.close()
  store_vol.close()