from pygame import mixer
import time
import threading

class soundThread(threading.Thread):
    def __init__(self, sound):
        threading.Thread.__init__(self)
        self.sound = sound
        
    def run(self):
        mixer.init()
        mixer.music.load('music/'+self.sound)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)

def play(sound):
    soundTh = soundThread(sound)
    soundTh.start()
    return soundTh