#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import time
import datetime
def dtmove(cap = cv2.VideoCapture(0)):
    occflag = 0
    motionCounter = 0
    avg = None
    times = 0
    time.sleep(1)
    for i in range(0,50):
        ret,frame = cap.read()
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    avg = cv2.GaussianBlur(gray, (21, 21), 0)
    grabold = avg.copy()
    diflx = avg.copy()

    while True:
        timestamp = datetime.datetime.now()
        ret,frame = cap.read()
        grab = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(grab, (21, 21), 0)
        differ = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
        ret, thresh = cv2.threshold(differ, 50, 255, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, iterations=8)
        (cnts,_) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            if cv2.contourArea(c) < 500:
                continue
            # 计算轮廓的边界框，在当前帧中画出该框
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            occflag = 1

        #背景重新获取
        if (occflag == 0):    
            (difavg,_,_,_) = cv2.mean(differ)
            print 'm', difavg
            if(difavg >2):
                avg = gray.copy()
        else:
            if times >= 30:
                times = 0
                diflx = cv2.absdiff(gray, cv2.convertScaleAbs(grabold))
                (difzx,_,_,_) = cv2.mean(diflx)
                print 'd',difzx
                grabold = gray.copy()
                if difzx<2 :  
                    avg = gray.copy()
            times=times + 1
            occflag = 0

        cv2.imshow('farme',frame)
        cv2.imshow('thresh',thresh)
        cv2.imshow('avg',avg)
        cv2.imshow('differ',differ)
        key = cv2.waitKey(15)&0xFF
        if key == ord('s') :
            ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
            cv2.imwrite("/home/lucky_d/pyex/images/"+ts+'.jpg',frame)
            print 'imgsaved!as'+ts+'.jpg'
        if key == ord('q') :
            break

    cap.release()
    cv2.destoryAllWindows()
    return
cap = cv2.VideoCapture(1)
dtmove(cap)
