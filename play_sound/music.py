from pygame import mixer
import time

mixer.init()
mixer.music.load('BLE_con.mp3')
mixer.music.play()
time.sleep(5.0)

mixer.music.load('BLE_uncon.mp3')
mixer.music.play()
time.sleep(5.0)

mixer.music.load('CAM_back.mp3')
mixer.music.play()
time.sleep(5.0)

mixer.music.load('CAM_self.mp3')
mixer.music.play()
time.sleep(5.0)
