import pygame
import time

pygame.mixer.init()
bang=pygame.mixer.Sound('sample.wav')
for i in range (3):
    bang.play()
    print(i)
    time.sleep(2.0)