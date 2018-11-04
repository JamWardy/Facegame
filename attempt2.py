import pygame
from random import randint

import cv2
import numpy as np

print ("Midlands invaders, face detection game. Play by moving your head up and down to move the ship up and down. Press space to fire a missile. Good luck! ")

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def ReadFaces(frame):
    faces = face_cascade.detectMultiScale(frame, 1.3, 5)
    a = 0
    b = 0
    for (x,y,w,h) in faces:
        if h > a:
            a = y
    return a

def DoTheFaceThing():
    cap = cv2.VideoCapture(0)
    ret, frame= cap.read()
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    value = ReadFaces(frame)
    return value, height


pygame.init()
pygame.display.set_caption("Don't look here - lmao gottem")
gameDisplay = pygame.display.set_mode((1000,600))
white = [255, 255, 255]
black = [0, 0, 0]
red = [255,0,0]
blue = [0,0,255]
clock = pygame.time.Clock()

amissile = []
bmissile = [975,0,False]
enemy = [950,randint(150,450)]
old_y = 300
new_y = 0
score = 0

pygame.display.update()

gameOver = False

while not gameOver:
    frame_pos, height = DoTheFaceThing()
    y = int(frame_pos / height * 600)
    if old_y < y:
        if old_y < y - 25:
            new_y = old_y + 25
        else:
            new_y = y
    elif old_y > y:
        if old_y > y + 25:
            new_y = old_y - 25
        else:
            new_y = y
    else:
        new_y = y
    gameDisplay.fill(black)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    pygame.draw.rect(gameDisplay, white, [25, new_y, 25, 25])
    old_y = new_y
    pygame.draw.rect(gameDisplay, white, [enemy[0], enemy[1], 25, 25])
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                amissile.append([25,new_y+6,True])
    for missile in amissile:
        if missile[2]:
            missile[0] += 40
            pygame.draw.rect(gameDisplay, white, [missile[0], missile[1], 10, 10])
        else:
            amissile.remove(missile)
    if bmissile[2]:
        bmissile[0] -= 40
        pygame.draw.rect(gameDisplay, white, [bmissile[0], bmissile[1], 10, 10])
    pygame.display.update()
    clock.tick(20)
    if not bmissile[2]:
        bmissile = [975,enemy[1],True]
    if bmissile[0] < 0:
        bmissile[2] = False
    if len(amissile) > 0:
        if amissile[0][0] > 1000:
            amissile[0][2] = False
        for missile in amissile:
            if missile[0] >= 925 and missile[0] <= 975 and missile[1] > enemy[1] and missile[1] < enemy[1] + 26:
                print ("Hit!")
                score += 1
                enemy = [975,randint(150,450)]
    if bmissile[0] >= 0 and bmissile[0] <= 50 and (bmissile[1] > new_y and bmissile[1] < new_y + 26):
        gameOver = True
    clock.tick(10)
pygame.quit()
print ("You died. Score:",score)
