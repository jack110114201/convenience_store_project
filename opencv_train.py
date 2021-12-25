import cv2
import numpy as np
import os
import time

mypath = './data/image'
cameraBrightness = 190
modulval = 10 #改採每10偵保存
minBlur = 500 #最小闊值 確保影像太模糊不會保存
grayImage =False
savefloder = True
saveData = False #保存影像
showImage = True
w = 180
h = 120


cap = cv2.VideoCapture(1)
cap.set(3 , 600)
cap.set(4 , 400)
cap.set(10 , cameraBrightness)

global countFolder

def saveDataFunc():
    global countFolder
    countFolder = 0
    while os.path.exists(mypath + str(countFolder)) :
        countFolder += 1
    os.makedirs(mypath + str(countFolder)) #查看資料夾並創建一個新的資料夾

count = 0
countSave  = 0

if savefloder == True:
    saveDataFunc()

while True:
    s , vimg = cap.read()
    cv2.imshow('video' , vimg)
    img = cv2.resize(vimg , (w ,h))
    if grayImage == True:
        img = cv2.cvtColor(img  , cv2.COLOR_BGR2GRAY)
    if saveData == True:
        blur = cv2.Laplacian(img, cv2.CV_64F).var()
        if count % modulval == 0 and blur > minBlur :
            nowTime = time.time()
            cv2.imwrite(mypath + str(countFolder) +'/' + str(countSave) + "_"+ str(int(blur))+"_"+str(nowTime)+".png" , img )
            countSave +=1
        count += 1

    if showImage == True :
        cv2.imshow("image" , img)

    if cv2.waitKey(1) & 0xFF == ord('p'):
        break

    if cv2.waitKey(1) & 0xFF == ord('d'):
        saveData = True
        print('save start')
    elif cv2.waitKey(1) & 0xFF == ord('s'):
        saveData = False
        print('save stop')

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)


