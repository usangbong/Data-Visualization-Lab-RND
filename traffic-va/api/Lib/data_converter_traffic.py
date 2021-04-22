import argparse
import pandas as pd
import json
import time
import datetime

def correct_heading(cctv_id, cctv_info, cutting_time):
  count_list = {}
  avgspeed_list = {}
  cctv_heading = cctv_info["heading"]
  
  tmp_count = []
  tmp_avgspeed = []
  start_index = -1

  try:
    df_flow = pd.read_csv("results/flow_"+cctv_id+".csv")

    for i in range(len(df_flow)):
      if float(df_flow.loc[i]["timestamp"]) > cutting_time:
        start_index = i
        break

    if start_index == -1:
      print("Nothing to convert")
      for i in range(0, 4):
        tmp_count.append([-2])
        tmp_avgspeed.append([-2])
    else:
      tmp_count.append(df_flow.loc[start_index:]["n_v count"].tolist())
      tmp_count.append(df_flow.loc[start_index:]["e_v count"].tolist())
      tmp_count.append(df_flow.loc[start_index:]["s_v count"].tolist())
      tmp_count.append(df_flow.loc[start_index:]["w_v count"].tolist())

      tmp_avgspeed.append(df_flow.loc[start_index:]["n_avg speed"].tolist())
      tmp_avgspeed.append(df_flow.loc[start_index:]["e_avg speed"].tolist())
      tmp_avgspeed.append(df_flow.loc[start_index:]["s_avg speed"].tolist())
      tmp_avgspeed.append(df_flow.loc[start_index:]["w_avg speed"].tolist())
  except:
    print("No data")
    for i in range(0, 4):
      tmp_count.append([-1])
      tmp_avgspeed.append([-1])

  if cctv_heading == "":
    print("CCTV has not been initalized")
    corrector = 0
  else:
    if cctv_heading == "E":
      corrector = 1
    elif cctv_heading == "S":
      corrector = 2
    elif cctv_heading == "W":
      corrector = 3
    else:
      corrector = 0

  for i in range(0,4):
    index = (i + corrector) % 4
    
    if index == 0:
      direction = "N"
    elif index == 1:
      direction = "E"
    elif index == 2:
      direction = "S"
    else:
      direction = "W"
      
    count_list[direction] = tmp_count[i]
    avgspeed_list[direction] = tmp_avgspeed[i]

  for direction in ["N", "E", "W", "S"]:
    remove_list = []

    for j in range(len(count_list[direction])-1,0,-1):
      if count_list[direction][j] <= 0:
        remove_list.append(j)

    for index in remove_list:
      count_list[direction].pop(index)
      avgspeed_list[direction].pop(index)

  return {"count": count_list, "avg": avgspeed_list}

def make_data(cctv_data):
  print("Making data")
  traffic_data = {}
  place_info = {}

  with open("../../public/data/traffic_data.json", "r", encoding="utf-8") as jsonFile:
    traffic_data = json.load(jsonFile)
  with open("../../public/data/place_data.json", "r", encoding="utf-8") as jsonFile:
    place_info = json.load(jsonFile)

  for edge, traffic in traffic_data.items():
    exist = False
    target_traffic = traffic
    heading = ""
    for place in place_info.values():
      if edge in place["edge"].values():
        for direction, value in place["edge"].items():
          if value == edge:
            heading = direction
            break

      if heading != "":
        break

    for data in cctv_data.values():
      if data["cctv"]["heading"] == heading and data["cctv"]["name"] == traffic["from"]:
        count_list = data["count"]
        avgspeed_list = data["avg"]
        exist = True
        break
    
    if exist and len(target_traffic["traffic"]) > 0:
      target_avgspeed = 0
      target_volume = 0

      print(avgspeed_list)

      if avgspeed_list[heading][0] == -2:
        print("Coping last data")
        target_avgspeed = target_traffic["traffic"][-1]["avs"]
        target_volume = target_traffic["traffic"][-1]["volume"]
      else:
        for j in range(len(avgspeed_list[heading])):
          target_avgspeed += avgspeed_list[heading][j]
        target_avgspeed /= len(avgspeed_list[heading])

        for j in range(len(count_list[heading])):
          target_volume += count_list[heading][j]

      converted_data_list = []
      if len(target_traffic["traffic"]) > 11:
        for j in range(1, len(target_traffic["traffic"])):
          converted_data_list.append(target_traffic["traffic"][j])

        target_traffic["traffic"] = converted_data_list
    else:
      target_avgspeed = -1
      target_volume = -1

    newData = {
      "time": len(target_traffic["traffic"]),
      "volume": target_volume,
      "avs": target_avgspeed
    }

    target_traffic["traffic"].append(newData)
    traffic = target_traffic

  with open("../../public/data/traffic_data.json", "w", encoding="utf-8") as jsonFile:
    json.dump(traffic_data, jsonFile, ensure_ascii=False, indent=2)

if __name__ =="__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--prev_time",type=str)
  opt = parser.parse_args()
  convertedOpt = vars(opt)

  cctv_list = []
  with open("../../public/data/cctv_data.json", "r", encoding='utf-8') as jsonFile:
    cctv_data = json.load(jsonFile)

  data_dict = {}
  for cctv_id, data in cctv_data.items():
    cctv_heading = ""
    print("Now " + str(cctv_id))
    new_data = correct_heading(cctv_id, data, int(convertedOpt['prev_time']))
    new_data["cctv"] = data
    data_dict[cctv_id] = new_data

  make_data(data_dict)