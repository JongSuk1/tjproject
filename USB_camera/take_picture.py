# Take video from camera and show it
import numpy as np  
import cv2
import os
import datetime

def store_img(folder, img_name, frame):
    if not os.path.isdir(folder):
       os.mkdir(folder)
    # make sound need
    cv2.imwrite(folder+'/'+img_name, frame)

capture = cv2.VideoCapture(0)  
print 'image width %d' % capture.get(3)  
print 'image height %d' % capture.get(4)  
  
capture.set(3, 640)  
capture.set(4, 480)  

period = 0

while(1):  
    ret,frame = capture.read()  
    cv2.imshow('webcam', frame )
    
    if period%60 == 0:
        img_name = datetime.datetime.now().strftime('%y%m%d-%H%M%S%f')+'.jpg'
        folder_name = datetime.datetime.now().strftime('%y%m%d')
        store_img(folder_name, img_name, frame)
    
    key = cv2.waitKey(1)&0xFF

    # auto record - store_img(folder_name,img_name,frame)

    if  key == ord('c'):
        img_name = datetime.datetime.now().strftime('%y%m%d-%H%M%S%f')+'.jpg'
        store_img("myimage", img_name, frame)

    elif key == ord('q'):
        break;  
    
    period = period+1

capture.release()  
cv2.destroyAllWindows()  