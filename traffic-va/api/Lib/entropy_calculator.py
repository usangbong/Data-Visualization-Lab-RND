import argparse
import pandas as pd
import csv
import math

sampling_period_min = 1 * 60
sampling_period_max = 7 * 60

def main(cctv_id):
  # entropy = [0,0]
  # for i in range(0,2):
  #   path_df = ""
  #   if i == 0:
  #     path_df = "./results/speed_"+cctv_id+"_diff.csv"
  #   else:
  #     path_df = "./results/speed_"+cctv_id+"_target.csv"

  #   df_speed = pd.read_csv(path_df)

  #   step_sum = len(df_speed)
  #   speed_step = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  #   for speed in df_speed["speed"]:
  #     step = min(int((float(speed) - (float(speed) % 5)) / 5 - 1), len(speed_step) - 1)
  #     speed_step[step] += 1

  #   for value in speed_step:
  #     if value > 0:
  #       prob = value / step_sum
  #       entropy[i] -= prob * math.log2(prob)

  # time_values = [0,0]

  df_arg = pd.read_csv("./results/argData_"+cctv_id+".csv")
  # current_interval = int(df_arg.loc[0]["interval"])
  # current_video_length = int(df_arg.loc[0]["period"])

  # if entropy[0] < entropy[1]:
  #   entropy_factor = 1 * 60
  # else:
  #   entropy_factor = -1 * 60

  # time_values[0] = int(max(current_interval + entropy_factor, current_video_length))
  # time_values[1] = int(min(max(current_video_length - entropy_factor, sampling_period_min), sampling_period_max))

  # print(time_values)

  # df_arg["interval"] = time_values[0]
  # df_arg["period"] = time_values[1]

  df_arg["interval"] = 5 * 60
  df_arg["period"] = 5 * 60

  df_arg.to_csv("./results/argData_"+cctv_id+".csv")

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--cctv_id",type=str)
  opt = parser.parse_args()
  convertedOpt = vars(opt)

  main(convertedOpt["cctv_id"])