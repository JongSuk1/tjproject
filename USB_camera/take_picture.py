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
    print 'image width %d' % capture.get(3)  
    print 'image height %d' % capture.get(4)  
      
    capture.set(3, 640)  
    capture.set(4, 480)  
    return capture


def make_name():
    img_name = datetime.datetime.now().strftime('%y%m%d-%H%M%S%f')+'.jpg'
    folder = datetime.datetime.now().strftime('%y%m%d')
    return folder, img_name


class camThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None
        self.set = True
        self.period = 0
        
    def run(self):
        capture = setup()
        period = 0
        while(self.set):
            ret, self.frame = capture.read()
            print(ret)
            cv2.imshow('webcam',self.frame )
            time.sleep(0.1)
            self.period = self.period+1
            if self.period%120 == 0:
                folder, img_name = make_name()
                store_img(folder, img_name, self.frame)
            ret = False

        capture.release()  
        cv2.destroyAllWindows() 

    def turnon(self):
        self.set = True

    def capture(self):
        folder, img_name = make_name()
        store_img("myimage", img_name, self.frame)
       
    def quit(self):
        self.set = False


        
