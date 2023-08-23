import numpy as np
import cv2
import torch
import serial
import time


arduino=serial.Serial(port='COM3',baudrate=115200,timeout=.1)
def sendToArduino(x):
    arduino.write(bytes(str(x),'utf-8'))
    time.sleep(0.05)


model=torch.hub.load('ultralytics/yolov5','yolov5n', pretrained=True)
model.classes=[0]


cv2.startWindowThread()
input=cv2.VideoCapture(0)
output=cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'MJPG'),15.,(640,480))


while(True):
    startTime=time.time()

    ret,frame=input.read()
    results=model(frame)

    labels,coordinates=results.xyxyn[0][:,-1],results.xyxyn[0][:,:-1]
    n=len(labels)
    if(n>1):
        continue
    x_shape,y_shape=frame.shape[1],frame.shape[0]
    for i in range(n):
        row=coordinates[i]
        if(row[4]>=0.2):
            x1,y1,x2,y2=int(row[0]*x_shape),int(row[1]*y_shape),int(row[2]*x_shape),int(row[3]*y_shape)

            if(row[4]<0.4):
                bgr=(0,0,255)
            elif(row[4]<0.6):
                bgr=(0,81,187)
            elif(row[4]<0.8):
                bgr=(0,228,255)
            else:
                bgr=(0,255,0)
            
            center=(x1+x2)/2
            cv2.rectangle(frame,(x1,y1),(x2,y2),bgr,2)
            cv2.putText(frame, model.names[int(labels[i])],(x1,y1-10),cv2.FONT_HERSHEY_COMPLEX,0.9,bgr,2)
            if(center<(x_shape/2)-5):
                cv2.putText(frame,"left",(x1+120,y2+10),cv2.FONT_HERSHEY_COMPLEX,0.9,bgr,2)
                magnitude=abs(((x_shape/2)-center)/5)
                sendToArduino(magnitude*-1)
                #sendToArduino(-5)
            elif(center>(x_shape/2)+40):
                cv2.putText(frame,"right",(x1+120,y2+10),cv2.FONT_HERSHEY_COMPLEX,0.9,bgr,2)
                magnitude=abs(((x_shape/2)-center)/5)
                sendToArduino(magnitude*1)
                #sendToArduino(5)
            else:
                cv2.putText(frame,"center",(x1+120,y2+10),cv2.FONT_HERSHEY_COMPLEX,0.9,bgr,2)

    endTime=time.time()
    fps=np.round(1/(endTime-startTime),3)
    cv2.putText(frame,f'FPS:{fps}',(10,20),cv2.FONT_HERSHEY_COMPLEX,0.9,(255,80,23))
    cv2.imshow('video',frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break





input.release()
output.release()
cv2.destroyAllWindows()