# Take video from camera and show it
import numpy as np  
import cv2  
  
capture = cv2.VideoCapture(0)  
print 'image width %d' % capture.get(3)  
print 'image height %d' % capture.get(4)  
  
capture.set(3, 640)  
capture.set(4, 480)  
  
img_num = 0  
  
while(1):  
    ret,frame = capture.read()  
    cv2.imshow( 'webcam', frame )
    
    key = cv2.waitKey(1)&0xFF

    if  key == ord('c'):
        print("capture")
        img_name = "image"+str(img_num)+".jpg"
        cv2.imwrite(img_name,frame)
        img_num = img_num+1
        
    elif key == ord('q'):
        break;  

capture.release()  
cv2.destroyAllWindows()  