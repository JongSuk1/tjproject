# Take video from camera and show it
import cv2
import os
import datetime
import threading
import time

def store_img(folder, img_name, frame):
    if not os.path.isdir(folder):
       os.mkdir(folder)
    cv2.imwrite(folder+'/'+img_name, frame)


def setup():
    capture = cv2.VideoCapture(0)  
    print ('image width %d' % capture.get(3)  )
    print ('image height %d' % capture.get(4) ) 
      
    capture.set(3, 640)  
    capture.set(4, 480)  
    return capture

def capture():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    folder, img_name = make_name()
    store_img("myimage", img_name, frame)

def make_name():
    img_name = datetime.datetime.now().strftime('%y%m%d-%H%M%S%f')+'.jpg'
    folder = datetime.datetime.now().strftime('%y%m%d')
    return folder, img_name


class camThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None
        self.set = True
        self.clock = 0
        
    def run(self):
        capture = setup()
        while(self.set):
            ret, self.frame = capture.read()
            time.sleep(0.1)
            self.clock = self.clock+1
            if self.clock%60 == 0:
                folder, img_name = make_name()
                store_img(folder, img_name, self.frame)

        capture.release()  
        cv2.destroyAllWindows() 
        print('camera closed')
        
    def turnon(self):
        self.set = True

    def capture(self):
        folder, img_name = make_name()
        store_img("myimage", img_name, self.frame)   
       
    def quit(self):
        self.set = False

    def is_running(self):
        return self.set
    
    def set_period(self,period):
        pass


        
