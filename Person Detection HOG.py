import numpy as np
import cv2
import serial
import time

arduino=serial.Serial(port='COM3',baudrate=115200,timeout=.1)
def sendToArduino(x):
    arduino.write(bytes(x,'utf-8'))
    time.sleep(0.05)

#HOG descriptor
#HOG stands for histogram of Oriented Gradients
#An edge in a picture leads to a larger gradient
#images are split into cells and the gradients are put into a histogram. The value is the angle of gradient while the weight is the magnitude.
hog=cv2.HOGDescriptor()

#Sets coefficients for SVM classifier
#SVM stands for support vector machines which is a machine learning algorithm
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


cv2.startWindowThread()
input = cv2.VideoCapture(0)
output=cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'MJPG'),15.,(640,480))

while(True):
    # reading the frame
    #read() function returns a tuple with the first value being the return value and second being the image
    ret, frame = input.read()

    # turn to greyscale
    #cvtColor() converts an image from one color space to another
    #first paremter is the source while the second is the conversion code
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    cv2.imshow('gray',gray)

    #threshold() set each pixle to a value based on the pixle value
    #first parameter is a gray scale image, second is the threshold value, third value is pixle value given when more than threshold value
    #THRESH_BINARY the value is set to 0 or 255
    #ret,frame = cv2.threshold(frame,80,255,cv2.THRESH_BINARY)

    #winStride is the step size in x and y direction
    box, weight=hog.detectMultiScale(frame,winStride=(8,8))
    #creates and array for the points on the box
    box=np.array([[x,y,x+w,y+h] for (x,y,w,h) in box])

    for(x1,y1,x2,y2) in box:
        #cv2.rectangle draws rectangle on an image
        i=cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
        center=(x1+x2)/2
        if(center<320-15):
            cv2.putText(i,'Left',(x1,y1-10),cv2.FONT_HERSHEY_COMPLEX,0.9,(0,255,0),2)
            sendToArduino('-1')
        elif(center>320+15):
            cv2.putText(i,'Right',(x1,y1-10),cv2.FONT_HERSHEY_COMPLEX,0.9,(0,255,0),2)
            sendToArduino('1')
        else:
            cv2.putText(i,'Center',(x1,y1-10),cv2.FONT_HERSHEY_COMPLEX,0.9,(0,255,0),2)


    
    output.write(frame.astype('uint8'))

    #display image
    #first parameter is the window name and second is the image
    cv2.imshow('result',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        #type q
        break
       
     

input.release()
output.release()
cv2.destroyAllWindows()
