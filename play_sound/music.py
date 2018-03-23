import pygame
import time

pygame.mixer.init()
bang=pygame.mixer.Sound('sample.mp3')

bang.play()
time.sleep(5.0)

#for i in range (3):
#    bang.play()
#    print(i)
#    time.sleep(2.0)