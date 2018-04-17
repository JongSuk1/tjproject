from pygame import mixer
import time
import threading
import sys
sys.path.insert(0, '/home/pi/tjproject/constants')
import constants as const

class soundThread(threading.Thread):
    def __init__(self, sound):
        threading.Thread.__init__(self)
        self.sound = sound
        
    def run(self):
        mixer.init()
        mixer.music.load(const.HOME_PATH+'music/'+self.sound)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)

def play(sound):
    soundTh = soundThread(sound)
    soundTh.start()
    return soundTh