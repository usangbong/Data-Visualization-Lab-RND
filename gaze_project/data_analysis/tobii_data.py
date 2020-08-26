# Python 3.7 version
import sys
import csv
from database import constant as dbconstant
import pymysql
global c

userID = "default"
conn = pymysql.connect(host=dbconstant.HOST, user=dbconstant.USER, password=dbconstant.PASSWORD, db=dbconstant.DB_NAME, charset=dbconstant.CHARSET,)
curs = conn.cursor(pymysql.cursors.DictCursor)

sql = "SELECT * FROM data_tobii"
curs.execute(sql)

rows = curs.fetchall()
userID = rows[0]['id']
fileName = ""

#c = csv.writer(open(fileName, "wb"))
prevFilename = fileName
gazePointCount = 0
pointCountSum = 0
fileCount = 1
minCount = 999999
maxCount = 0
for _row in rows:
    userID = _row['id']
    showCount = str(_row['count'])
    stiName = _row['sti']
    t = str(_row['t'])
    t_order = str(_row['t_order'])
    img_w = str(_row['img_w'])
    img_h = str(_row['img_h'])
    sti_x = str(_row['sti_x'])
    sti_y = str(_row['sti_y'])
    
    left_x = _row['left_x']
    left_y = _row['left_y']
    right_x = _row['right_x']
    right_y = _row['right_y']
    if left_x <= 0 or left_y <= 0 or right_x <= 0 or right_y <= 0:
        prevFilename = fileName
        continue
    left_x = str(left_x)
    left_y = str(left_y)
    right_x = str(right_x)
    right_y = str(right_y)
    avg_x = str(_row['avg_x'])
    avg_y = str(_row['avg_y'])
    left_validity = _row['left_validity']
    right_validity = _row['right_validity']
    if left_validity == 0 or right_validity == 0:
        prevFilename = fileName
        continue
    left_validity = str(left_validity)
    right_validity = str(right_validity)
    true_validity = str(_row['true_validity'])
    fileName = "./data_tobii/" + userID + "_" + showCount + "_" + stiName + ".csv"
    if fileName != prevFilename:
        c = csv.writer(open(fileName, "w", newline=''))
        print(gazePointCount)
        pointCountSum += gazePointCount
        
        if fileCount != 1:
            if gazePointCount < minCount:
                minCount = gazePointCount
            if gazePointCount > maxCount:
                maxCount = gazePointCount
        gazePointCount = 0
        fileCount += 1
        
    _d = [userID, showCount, stiName, t, t_order, img_w, img_h, sti_x, sti_y, left_x, left_y, right_x, right_y, avg_x, avg_y, left_validity, right_validity, true_validity]
    
    c.writerow(_d)
    gazePointCount += 1

    prevFilename = fileName

avgPoint = pointCountSum / fileCount
print("minPoint: %d"%minCount)
print("maxPoint: %d"%maxCount)
print("avgPoint: %d"%avgPoint)