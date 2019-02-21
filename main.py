import pygame
from random import randint

import cv2
import numpy as np #imports

print ("Midlands invaders, face detection game. Play by moving your head up and down to move the ship up and down. Press space to fire a missile. Good luck! ")

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #access haar cascade for facial detection

def ReadFaces(frame): #function that finds face in image
    faces = face_cascade.detectMultiScale(frame, 1.3, 5) #object of all faces found
    a = 0
    b = 0
    for (x,y,w,h) in faces:
        if h > a:
            a = y #picks out which face is the largest
    return a #returns information for the largest face

def VideoFaces(): #video capture
    cap = cv2.VideoCapture(0)
    ret, frame= cap.read() #returns frame
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    value = ReadFaces(frame) #returns values for face in frame
    return value, height


pygame.init()
pygame.display.set_caption("Facegame")
gameDisplay = pygame.display.set_mode((1000,600)) #creates 1000 x 600 game display
white = [255, 255, 255]
black = [0, 0, 0]
red = [255,0,0]
blue = [0,0,255] #colours used
clock = pygame.time.Clock()

amissile = [] #missiles fired by the player
bmissile = [975,0,False] #enemy missiles
enemy = [950,randint(150,450)] #random start for enemy
old_y = 300 #start point for the player
new_y = 0
score = 0

pygame.display.update()

gameOver = False

while not gameOver: #whilst the game is going on
    frame_pos, height = VideoFaces() #find faces
    y = int(frame_pos / height * 600) #create new co-oridinate for where player should be based on where the face is
    if old_y < y: #changes current location of player to move it closer to where it should be
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
    gameDisplay.fill(black) #clear the screen
    if cv2.waitKey(1) & 0xFF == ord('q'): #quit game if 'q' key pressed
        break
    pygame.draw.rect(gameDisplay, white, [25, new_y, 25, 25]) #draw player on screen
    old_y = new_y
    pygame.draw.rect(gameDisplay, white, [enemy[0], enemy[1], 25, 25]) #draw enemy on screen
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: #if a key is pressed and it is space
                amissile.append([25,new_y+6,True]) #fire a new missile
    for missile in amissile: #for all player missiles that have been fired
        if missile[2]: #if missile still active in game
            missile[0] += 40 #move it along the screen
            pygame.draw.rect(gameDisplay, white, [missile[0], missile[1], 10, 10]) #draw the missile
        else:
            amissile.remove(missile) #delete misisle if not active
    if bmissile[2]: #if enemy missile still active
        bmissile[0] -= 40 #move it across screen
        pygame.draw.rect(gameDisplay, white, [bmissile[0], bmissile[1], 10, 10]) #draw the missile
    pygame.display.update() #update the display
    clock.tick(20) #wait 20 milliseconds
    if not bmissile[2]: #if no enemy missile active
        bmissile = [975,enemy[1],True] #fire a new one
    if bmissile[0] < 0: #if enemy missile leaves game boundaries
        bmissile[2] = False #deactivate it
    if len(amissile) > 0: #if there are any player missiles in the game
        if amissile[0][0] > 1000: #if outside boundaries
            amissile[0][2] = False #remove it
        for missile in amissile: #otherwise, if player missile hits enemy
            if missile[0] >= 925 and missile[0] <= 975 and missile[1] > enemy[1] and missile[1] < enemy[1] + 26:
                print ("Hit!")
                score += 1 #add one to score
                enemy = [975,randint(150,450)] #replace enemy
    if bmissile[0] >= 0 and bmissile[0] <= 50 and (bmissile[1] > new_y and bmissile[1] < new_y + 26): #if enemy missile hits player
        gameOver = True #game over
    clock.tick(10)
pygame.quit()
print ("You died. Score:",score)
