# conda activate detect
# command : python app_modify_fin.py --video_folder="videodata/200200130_2.mp4" --news="news" --diff_path="videodata/20200130_9.mp4" --news2="ne"
import cv2
#from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
#from PyQt5.QtGui import QImage, QPixmap
#from gui import *
import copy
from counter import CounterThread
from utils.sort import *
from models import *
from utils.utils import *
from utils.datasets import *
from config import *
import entropy_calculator
import video_crawler
import video_trimmer

import argparse
import predict
from torch.utils.data import DataLoader
import predict

import glob
import pandas as pd
import csv
import json
import time
import random
import requests
import shutil
import math

videoList = []
header_num = 0
history = {}
model = ""
device = ""
clean_vid_list = []
point_list = []
count = 0
check_diff = ""
fcnt = 0
timestamp = 0
sampling_period_min = 5 * 60
sampling_period_max = 5 * 60
fps = 15
capture_per_sec = 2

def cal_iou(box1,box2):
    x1 = max(box1[0],box2[0])
    y1 = max(box1[1],box2[1])
    x2 = min(box1[2],box2[2])
    y2 = min(box1[3],box2[3])
    i = max(0,(x2-x1))*max(0,(y2-y1))
    u = (box1[2]-box1[0])*(box1[3]-box1[1]) + (box2[2]-box2[0])*(box2[3]-box2[1]) -  i
    iou = float(i)/float(u)
    return iou

def get_objName(item,objects):
    iou_list = []
    for i,object in enumerate(objects):
        x, y, w, h = object[2]
        x1, y1, x2, y2 = int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)
        iou_list.append(cal_iou(item[:4],[x1,y1,x2,y2]))
    max_index = iou_list.index(max(iou_list))
    return objects[max_index][0]

def filter_out_repeat(objects):
    objects = sorted(objects,key=lambda x: x[1])
    l = len(objects)
    new_objects = []
    if l > 1:
        for i in range(l-1):
            flag = 0
            for j in range(i+1,l):
                x_i, y_i, w_i, h_i = objects[i][2]
                x_j, y_j, w_j, h_j = objects[j][2]
                box1 = [int(x_i - w_i / 2), int(y_i - h_i / 2), int(x_i + w_i / 2), int(y_i + h_i / 2)]
                box2 = [int(x_j - w_j / 2), int(y_j - h_j / 2), int(x_j + w_j / 2), int(y_j + h_j / 2)]
                if cal_iou(box1,box2) >= 0.7:
                    flag = 1
                    break
            #if no repeat
            if not flag:
                new_objects.append(objects[i])
        #add the last one
        new_objects.append(objects[-1])
    else:
        return objects

    return list(tuple(new_objects))

def update_counter_results(counter_results,vid_name):
    with open("results/results_"+vid_name+".txt", "a") as f:
        
        for i, result in enumerate(counter_results):
            print("result: {}\n".format(result))
            f.writelines(' '.join(map(lambda x: str(x),result)))
            #f.wirte(result)
            f.write("\n")

def update_counter_results_gubun(cnt,vid_name):
    global fcnt
    with open("results/results_"+vid_name+".txt", "a") as f:
        f.write(str(fcnt))
        f.write(" frame changed\n\n")

header_num = 0
def make_df(arr,vid_name):
    global header_num
    if header_num == 0:
      open("results/results_"+vid_name+".csv","w",newline='')

    with open("results/results_"+vid_name+".csv","a",newline='') as f:
        writer = csv.writer(f)
        if header_num == 0:
            columns = ["frame_num","id","d2x","d2y","rx","ry","heading"]
            writer.writerow(columns)
        for result in arr:
            result.insert(0,header_num)
            writer.writerow(result)
        header_num += 1


def counter(permission,colorDict,frame,mot_tracker,videoName,viul):
    global history
    global model
    global device

    class_names = ['bicycle','bus','car','motorbike','truck']
    objects = predict.yolo_prediction(model,device,frame,class_names)
    objects = filter(lambda x : x[0] in permission, objects)
    objects = filter(lambda x : x[1] > 0.5, objects)

    objects = filter_out_repeat(objects)
    detections = []
    for item in objects:
        detections.append([int(item[2][0] - item[2][2] / 2),
                           int(item[2][1] - item[2][3] / 2),
                           int(item[2][0] + item[2][2] / 2),
                           int(item[2][1] + item[2][3] / 2),
                           item[1]])
    track_bbs_ids = mot_tracker.update(np.array(detections))

    if len(track_bbs_ids) > 0:
        for bb in track_bbs_ids:
            id = int(bb[-1])
            objectName = get_objName(bb,objects) 
            if id not in history.keys():
                history[id] = {}
                history[id]["no_update_count"] = 0
                history[id]["his"] = [] 
                history[id]["his"].append(objectName)
            else:
                history[id]["no_update_count"] = 0
                history[id]["his"].append(objectName)

    df_input = []
    
    for i, item in enumerate(track_bbs_ids):
        bb = list(map(lambda x: int(x), item))
        id = bb[-1]
        x1, y1, x2, y2 = bb[:4]

        his = history[id]["his"]
        result = {}
        for i in set(his):
            result[i] = his.count(i)
        res = sorted(result.items(), key=lambda d: d[1], reverse=True)
        objectName = res[0][0]

        boxColor = colorDict[objectName]
        cv2.rectangle(frame, (x1, y1), (x2, y2), boxColor, thickness=2)
        cx = int((x2+x1)/2)
        cy = int((y2+y1)/2)
        rx = cx * viul
        ry = cy * viul

        # print("points\nid:{}, obj:{}, x:{}, y:{}, rx:{}, ry:{}".format(str(id),objectName,cx,cy,rx,ry))
        save = []
        save.append([id,objectName,[cx,cy]])
        update_counter_results(save,videoName)
        cv2.putText(frame, str(id) + "_" + objectName, (x1 - 1, y1 - 3), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                    boxColor,
                    thickness=2) 
        v_id = "V"+str(id)
        df_input.append([v_id,cx,cy,rx,ry,''])
    make_df(df_input,videoName)
    
    counter_results = []

    for id in history.keys():    #extract id after tracking
        history[id]["no_update_count"] += 1
        if  history[id]["no_update_count"] > 5:
            his = history[id]["his"]
            result = {}
            for i in set(his):
                result[i] = his.count(i)
            res = sorted(result.items(), key=lambda d: d[1], reverse=True)
            objectName = res[0][0]
            counter_results.append([videoName,id,objectName])

    return frame

def cal_heading(df_path,direction):
    df = pd.read_csv(df_path)
    vid_list = []
    # vehicle id 갖고와
    for i in range(len(df)):
        vid = df["id"].loc[i]
        vid_list.append(vid)
    #중복 제거
    my_set = set()
    global clean_vid_list
    clean_vid_list = []
    for e in vid_list:
        if e not in my_set:
            clean_vid_list.append(e)
            my_set.add(e)

    #print(clean_vid_list)
    
    for idd in clean_vid_list:
        df_id = df[df["id"]==idd]
        tmp=0
        while True:
            vfx,vfy = int(df_id["d2x"].iloc[tmp]),int(df_id["d2y"].iloc[tmp])
            #print(vfx,vfy)
            #NS
            if len(direction)==1:
                nx,ny = point_list[2][0],point_list[2][1]
                if vfy > ny:
                    heading = "N"
                else:
                    heading = ""
            elif len(direction)==2:
                nx,ny = point_list[2][0],point_list[2][1]
                sx,sy = point_list[3][0],point_list[3][1]
                if vfy > ny:
                    heading = "N"
                elif vfy < sy:
                    heading = "S"
                else:
                    heading = ""

            elif len(direction)==4:
                nx,ny = point_list[2][0],point_list[2][1]
                ex,ey = point_list[3][0],point_list[3][1]
                wx,wy = point_list[4][0],point_list[4][1]
                sx,sy = point_list[5][0],point_list[5][1]
                if vfx<wx and vfy<=wy:
                    heading = "W"
                elif vfx>ex and vfy>ey:
                    heading = "E"
                elif vfx>nx and vfy<ny:
                    heading = "N"
                elif vfx<sx and vfy>sy:
                    heading = "S" 
                else:
                    heading = ''  
            else:
                heading = ''  
            #print(heading)                                                    
            df_id.iloc[tmp, df.columns.get_loc('heading')]= heading
            tmp += 1
            if tmp==len(df_id):
                df[df["id"]==idd] = df_id
                break

          
    return df

point_list = []
init_frame_cnt = 0

def mouse_callback(event, x, y, flags, param):
    global point_list, count


    # click
    if event == cv2.EVENT_LBUTTONDOWN:
        point_list.append((x, y))
        cv2.circle(videoList[0], (x, y), 3, (0, 0, 255), -1)

def make_flow(vid, flow_df, frame_count):
    global capture_per_sec, fps
    df = pd.read_csv("results/f_results_"+vid+".csv")
    df = df.dropna().reset_index(drop=True)
    df_list = []
    for frame_step in range(math.ceil(frame_count / capture_per_sec / 60)):
      df_list.append(df[(df["frame_num"]>=0 * frame_step) & (df["frame_num"]<60 * frame_step)])

    vehicle_speed_list = []
    
        #두개 한꺼번에
    time_cnt=len(flow_df)
    idx=len(flow_df)
    for dl in df_list:
        idx+=1
        time_cnt += 1
        h_list = []

        clean_v_list=[]
        # count 구하기
        v_list = []
        news_sum = 0
        for i in range(len(dl)):
            v_id = dl["id"].iloc[i]
            v_list.append(v_id) 
        #print(v_list)
        v_set = set()
        for e in v_list:
            if e not in v_set:
                clean_v_list.append(e)
                v_set.add(e)
        # print(clean_v_list)
        # heading 별 속도
        speed_list = []
        for _dir in ["N","E","W","S"]:
            speed_sum = 0
            vehicle_count = 0
            for _id in clean_v_list:
                df_sub2 = dl[(dl["heading"]==_dir) & (dl["id"]==_id)]
                if len(df_sub2)<=1:
                    pass
                else:
                    point1x,point1y = df_sub2["rx"].iloc[0],df_sub2["ry"].iloc[0]
                    point2x,point2y = df_sub2["rx"].iloc[-1],df_sub2["ry"].iloc[-1]
                    time = ((df_sub2["frame_num"].iloc[-1] - df_sub2["frame_num"].iloc[0]) / capture_per_sec) / 60
                    distance = abs(math.sqrt(math.pow(point2x-point1x,2)+math.pow(point2y-point2x,2)))/100000
                    speed = distance/time
                    speed_sum += speed
                    vehicle_speed_list.append(speed)
                    vehicle_count += 1
            if vehicle_count > 0:
                speed_avg = speed_sum / vehicle_count
                h_list.append(vehicle_count)
            else:
                speed_avg = 0
                h_list.append(0)
            speed_list.append(speed_avg)
            
        output = [time_cnt, h_list[0],h_list[1],h_list[2],h_list[3],speed_list[0],speed_list[1],speed_list[2],speed_list[3],timestamp]
        flow_df.loc[idx] = output
        #idx +=1

    df_speed = pd.DataFrame(columns=["speed"])
    df_speed["speed"] = vehicle_speed_list

    try:
      shutil.move("./results/speed_"+vid+"_target.csv", "./results/speed_"+vid+"_diff.csv")
    except:
      df_speed.to_csv("./results/speed_"+vid+"_diff.csv", index=False)
    
    df_speed.to_csv("./results/speed_"+vid+"_target.csv", index=False)

    return flow_df

def framediff(current_frame_gray,previous_frame_gray):
    global check_diff
    check_diff=0
    frame_diff = cv2.absdiff(current_frame_gray,previous_frame_gray)
    cv2.imshow('frame diff ',frame_diff)
    #n_diff = np.mean(frame_diff,axis=2)
    #therhold = 20
    #n_diff[n_diff<=20]=0
    #n_diff[n_diff>therhold]=255
    #mask = np.dstack([n_diff]*3)
    #print(np.sum(mask))
    diff = np.mean(frame_diff)
    if diff>50:
        check_diff=1
    return frame_diff

def Proceed(opt):
    global videoList, header_num, history, model, device, clean_vid_list, point_list, count, check_diff, fps, capture_per_sec
    diff_first_frame = []

    #model_def = opt["model_def"]
    #weight_path = opt["weight_path"]
    #video_folder = opt["video_folder"]
    data_config = opt["data_config"]
    news_config = opt["news"]
    data_config = parse_data_config(data_config)
    yolo_calss_names = load_classes(data_config["names"])
    vid_path = opt["cctv_id"]
    #print(yolo_calss_names)

    diff_path = "./videodata/"+vid_path+".jpg"
    
    if opt["start"] == "":
      videoList = video_crawler.crawl_video(vid_path, opt["sampling_period"], fps, capture_per_sec)
    else:
      start = int(opt["start"])
      time_list = []
      left = start % (60 * 60)
      time_list.append((start - left) / (60 * 60))
      time_list.append((left - (left % 60)) / 60)
      left = left % 60
      time_list.append(left)
      starttime = str(int(time_list[0])) + ":" + str(int(time_list[1])) + ":" + str(int(time_list[2]))

      start += opt["sampling_period"]
      time_list = []
      left = start % (60 * 60)
      time_list.append((start - left) / (60 * 60))
      time_list.append((left - (left % 60)) / 60)
      left = left % 60
      time_list.append(left)
      endtime = str(int(time_list[0])) + ":" + str(int(time_list[1])) + ":" + str(int(time_list[2]))

      videoList = video_trimmer.trim_video(vid_path, starttime, endtime, fps, capture_per_sec)
    print("Captured video complete")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("current device = {}".format(device))

    print("Loading model...")
    model = Darknet(opt["model_def"]).to(device)
    if opt["weights_path"].endswith(".weights"):
        model.load_darknet_weights(opt["weights_path"])
    else:
        model.load_state_dict(torch.load(opt["weights_path"]))
    model.eval()

    if opt["viul"] == -1:
      diff_first_frame = videoList[0]
    else:
      diff_first_frame = cv2.imread(diff_path)

    cv2.imwrite(diff_path, videoList[0])

    print("Compare...")
    fgbg =  cv2.createBackgroundSubtractorMOG2()

    b_frame = videoList[0]
    a_frame = diff_first_frame

    b_frame_gray = cv2.cvtColor(b_frame, cv2.COLOR_BGR2GRAY)
    a_frame_gray = cv2.cvtColor(a_frame, cv2.COLOR_BGR2GRAY)
    frame_diff = framediff(b_frame_gray,a_frame_gray)
          
    cv2.destroyAllWindows()
    
    print("Finish Compare .. absdiff")
    if check_diff==1:
        print("video is different with past")

        f = open("./results/diff_"+convertedOpt["cctv_id"], "w")
        f.close()

    save_dir = "results"
    if not os.path.exists(save_dir): os.makedirs(save_dir)

    permission = names
    colorDict = color_dict
    history = {}
    mot_tracker = Sort(max_age=10, min_hits=2)

    if len(opt["chasun"]) == 0:
        cv2.namedWindow('original')
        cv2.setMouseCallback('original', mouse_callback)
        
        while(True):
            cv2.imshow("original", videoList[0])


            height, width = videoList[0].shape[:2]
            #print(point_list)
            #x2,y2 = point_list[1]
            #x1,y1 = point_list[2]
            #width,height  = x2-x1,y2-y1

            if cv2.waitKey(1)&0xFF == 32: # space bar -> loop exit
                break
        #print(point_list)

        # 차선 길이 
        x0,y0 = point_list[0][0],point_list[0][1]
        x1,y1 = point_list[1][0],point_list[1][1]
        print(x0, y0, x1, y1)
        # heading
        print("pointlist###################")
        print(point_list)

        #px1 = 0.026
        #height*px1 : length = rw : 2000
        #height : real = length : 800
        length = (math.sqrt(math.pow(x1-x0,2)+math.pow(y1-y0,2)))
        #rh = int((800 * height * px1)/(length*px1))
        rh = height*800/length
        print("video height : {}".format(height))
        print("chasun len : {}".format(length))
        print("real height: {}".format(rh))
        viul = int(rh/height)  #차선 to 차선 길이 8m

        #img_result = cv2.warpPerspective(img_original, M, (width2*viul ,height2*viul)) ##비율 문제


        #cv2.imshow("result1", img_result)
        #cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif len(opt["chasun"]) != 0:
        point_list = opt["chasun"]
        viul = opt["viul"]
        
#for video in videoList:
    last_max_id = 0
    #out =  cv2.VideoWriter(os.path.join(save_dir,video.split("/")[-1]), cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 10, (1920, 1080))
    
    fcnt = 0
    cv2.namedWindow('original')
    for frame in videoList:
        print(str(fcnt) + "/" + str(len(videoList)))
        frame = counter(permission, colorDict, frame, mot_tracker, vid_path,viul)
        cv2.imshow("original", frame)
        while(True):
          if cv2.waitKey(1)&0xFF == 32: # space bar -> loop exit
            break
        update_counter_results_gubun(fcnt,vid_path)
        fcnt +=1
    cv2.destroyAllWindows()

    KalmanBoxTracker.count = 0
    print("detect A finish\n Start cal_heading...")


    final_df = cal_heading("results/results_"+vid_path+".csv",news_config)

    final_df.to_csv("results/f_results_"+vid_path+".csv",index=False)
    #final_df2 = cal_outlier("results/f_results.csv")
    #mp4_kind = openfile_name[10:-4]
    #final_df.to_csv("results/results_"+mp4_kind+".csv",index=False)
    #print(clean_vid_list)
    #print("cal heading finish\n Start Making flow...")
    print("cal heading finish")
    try:
      _flow_df = pd.read_csv("results/flow_"+vid_path+".csv")
    except:
      _flow_df = pd.DataFrame(columns=["time",'n_v count','e_v count','w_v count','s_v count','n_avg speed','e_avg speed','w_avg speed','s_avg speed','timestamp'])
    finally:
      _flow_df = make_flow(vid_path, _flow_df, fcnt)
    _flow_df.to_csv("results/flow_"+vid_path+".csv",index=False)
    header_num=0

    print("All finish")

    return [check_diff, point_list, viul]
            
if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cctv_id",type=str)
    parser.add_argument("--model_def",type=str,default="config/yolov3.cfg")
    parser.add_argument("--weights_path",type=str,default="weights/yolov3.weights")
    parser.add_argument("--data_config",type=str,default="config/coco.data")
    parser.add_argument("--img_size",type=int,default=416)
    parser.add_argument("--n_cpu", type=int,default=0, help="number of cpu threads to use during batch generation")
    parser.add_argument("--batch_size", type=int,default=1, help="size of the batches")
    parser.add_argument("-o",type=str)
    parser.add_argument("--news",type=str)
    parser.add_argument("--start",type=str,default="")
    opt = parser.parse_args()
    
    timestamp = time.time()
    convertedOpt = vars(opt)

    try:
        df_arg = pd.read_csv("results/argData_"+convertedOpt["cctv_id"]+".csv")
        chasun_x = df_arg["chasun_x"].tolist()
        chasun_y = df_arg["chasun_y"].tolist()
        chasun_list = []
        for i in range(len(chasun_x)):
            chasun_list.append([chasun_x[i], chasun_y[i]])
        convertedOpt["chasun"] = chasun_list
        convertedOpt["viul"] = int(df_arg.loc[0]["viul"])
        sampling_interval = int(df_arg.loc[0]["interval"])
        convertedOpt["sampling_period"] = int(df_arg.loc[0]["period"])
    except:
        convertedOpt["viul"] = -1
        convertedOpt["chasun"] = []
        sampling_interval = 5 * 60
        convertedOpt["sampling_period"] = 5 * 60

    data = Proceed(convertedOpt)

    argData = pd.DataFrame(columns=["chasun_x", "chasun_y", "viul", "interval", "period"])
    chasun_x = []
    chasun_y = []
    for i in range(len(data[1])):
        chasun_x.append(data[1][i][0])
        chasun_y.append(data[1][i][1])
    argData["chasun_x"] = chasun_x
    argData["chasun_y"] = chasun_y
    argData["viul"] = data[2]
    argData["interval"] = sampling_interval
    argData["period"] = ((convertedOpt["sampling_period"] - (convertedOpt["sampling_period"] % fps)) / fps)

    argData.to_csv("results/argData_"+convertedOpt["cctv_id"]+".csv",index=False)

    entropy_calculator.main(convertedOpt["cctv_id"])

    f = open("./results/done_"+convertedOpt["cctv_id"], "w")
    f.close()