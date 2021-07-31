import traci
import time
import traci.constants as tc
import pytz
import datetime
from random import randrange
import pandas as pd


sumoCmd = ["sumo", "-c", "osm.sumocfg"]
traci.start(sumoCmd)

time_cnt = 0

packBigData = []

while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()

    lanes = traci.lane.getIDList()

    for i in range(len(lanes)):
        id = lanes[i]
        spd = round(traci.lane.getLastStepMeanSpeed(lanes[i])*3.6, 2)
        time = time_cnt
        if spd == round(traci.lane.getMaxSpeed(lanes[i])*3.6, 2):
            spd = 0

        _list = [time, id, spd]

        packBigData.append(_list)

        # print(traci.lane.getLastStepVehicleIDs(lanes[i]))

    time_cnt += 1

traci.close()
data = pd.DataFrame(packBigData, columns=['time', 'id', 'spd'])
data.to_csv("result_make.csv", index=False)
