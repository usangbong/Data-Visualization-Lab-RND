import sys
import os
import csv

data_path = './data_tobii'
dataFile_list = os.listdir(data_path)

i = 0
for _dataFilePath in dataFile_list:
    _filePath = data_path + "/" + _dataFilePath
    rf = open(_filePath, 'r', encoding='utf-8')
    rdr = csv.reader(rf)
    rowsInFile = []
    for _row in rdr:
        rowsInFile.append(_row)
    rf.close()    

    outDirPath = "./processed_data_tobii"
    outputFilePath = outDirPath + "/" + rowsInFile[i][0] + "_" + rowsInFile[i][1] + "_" + rowsInFile[i][2] + ".csv"
    
    wf = open(outputFilePath, 'w', newline='')
    wdr = csv.writer(wf)
    
    _fflag = True
    for _row in rowsInFile:
        t = _row[3]
        t_order = _row[4]
        avg_x = _row[13]
        avg_y = _row[14]

        sti_x = _row[7]
        sti_y = _row[8]

        gaze_x = float(avg_x) - float(sti_x)
        gaze_y = float(avg_y) - float(sti_y)
        gaze_x = str(gaze_x)
        gaze_y = str(gaze_y)

        if _fflag:
            wdr.writerow(["t", "x", "y"])
            _fflag = False
        
        #_in = [t, t_order, gaze_x, gaze_y]
        _in = [t, gaze_x, gaze_y]
        wdr.writerow(_in)
    i += 1
    
    
