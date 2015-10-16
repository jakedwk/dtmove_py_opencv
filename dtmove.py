#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import time
import datetime
def dtmove(cap = cv2.VideoCapture(0)):
    occflag = 0
    motionCounter = 0
    avg = None
    time.sleep(1)
    for i in range(0,50):
        ret,frame = cap.read()
    ret,frame = cap.read()
    grabold = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    print "[INFO] starting background model..."
    avg = cv2.GaussianBlur(grabold, (21, 21), 0)
    while True:
        if cv2.waitKey(10)&0xFF == ord(' '):
            while True:
                if cv2.waitKey(10)&0xFF == ord(' '):
                    break
        ret,frame = cap.read()
        timestamp = datetime.datetime.now()
        grab = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray = cv2.absdiff(grab, cv2.convertScaleAbs(avg))
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ret, thresh = cv2.threshold(gray, 55, 255, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts,_) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        # print cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cv2.waitKey(5)

        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 1000:
                continue
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            # 计算轮廓的边界框，在当前帧中画出该框
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # 计算背景变化程度重新选取背景
            occflag = 1
            diflx = cv2.absdiff(grab, cv2.convertScaleAbs(grabold))
            (difzx,_,_,_) = cv2.mean(diflx)
            if difzx<4 :  #背景重新获取
                # print "[INFO] starting background model..."
                avg = cv2.GaussianBlur(grab, (21, 21), 0)
        #背景重新获取
        if (occflag == 0):    
            (difavg,_,_,_) = cv2.mean(gray)
            diflx = cv2.absdiff(grab, cv2.convertScaleAbs(grabold))
            (difzx,_,_,_) = cv2.mean(diflx)
            print difavg,difzx
            if(difavg >7):
            # if(difavg >9)|(difzx < 4):
                # print "[INFO] starting background model..."
                avg = cv2.GaussianBlur(grab, (21, 21), 0)

        occflag = 0
        grabold = grab.copy()
        cv2.imshow('farme',frame)
        cv2.imshow('thresh',thresh)
        cv2.imshow('gray',gray)
        cv2.imshow('difxx',diflx)
        if cv2.waitKey(1)&0xFF == ord('s'):
            ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
            cv2.imwrite("/home/lucky_d/pyex/images/"+ts+'.jpg',frame)
            print 'imgsaved!as'+ts+'.jpg'

        if cv2.waitKey(1)&0xFF == ord('q'):
            break 
    cap.release()
    cv2.destoryAllWindows('frame')
    return

dtmove()
