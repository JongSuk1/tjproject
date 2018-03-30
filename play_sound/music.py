from pygame import mixer
import time
    
class soundThread(threading.Thread):
    def __init__(self, sound):
        threading.Thread.__init__(self)
        self.sound = sound
        
    def run(self):
        mixer.init()
        mixer.music.load('music/'+self.sound)
        mixer.music.play()
        while mixer.music.get_busy():
            pass