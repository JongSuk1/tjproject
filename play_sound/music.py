from pygame import mixer
import time

mixer.init()

def play_music(sound):
    mixer.music.load(sound)
    mixer.music.play()
    time.sleep(5.0)

def BLE_check(a):
    if a == 0:
        play_music('BLE_uncon.mp3')
        
    elif a == 1:
        play_music('BLE_con.mp3')
        
    else:
        print("Wrong input")
        

def CAM_check(a):
    if a == 0:
        play_music('CAM_back.mp3')

    elif a == 1:
        play_music('CAM_self.mp3')
        
    else:
        print("Wrong input")   
    
def soundtest():
    play_music('BLE_con.mp3')
    play_music('BLE_uncon.mp3')
    play_music('CAM_back.mp3')
    play_music('CAM_self.mp3')

# soundtest()