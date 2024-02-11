import pygame
import math
import sys
from pygame.locals import *

# 3D Engine created by Alex Decker

# All the variables!
viewFactor = 600
camX = 100
camY = -300
camZ = 100
x1 = 0
y1 = 0
z1 = 0
x2 = 0
y2 = 0
z2 = 0
nearPlane = 30
clipPercent = 0
rotX = 0
rotY = -90
sinX = 0
cosX = 0
sinY = 0
cosY = 0
keysPressed = ''
stepsPerSecond = 60
counter = 0
increment = 1
gravity = -1
downVel = 10
jumpCounter = 0

rect1s = 0
rect2s = 0
rect3s = 0
rect4s = 0
rect5s = 0
rect6s = 0
rect7s = 0
rect8s = 0
rect9s = 0
rect10s = 0
rect11s = 0
rect12s = 0
rect13s = 0
rect14s = 0
rect15s = 0
rectList = []
rectSlist = []

rectValues = None

rect1 = (100, 100, 100, 100, 100, 100, (255, 0, 0))
rect2 = (300, 100, 100, 200, 100, 100, (250, 0, 0))
rect3 = (500, 100, 100, 300, 100, 100, (240, 0, 0))
rect4 = (700, 200, 100, 300, 100, 100, (220, 0, 0))
rect5 = (900, 300, 100, 200, 100, 100, (180, 0, 0))
rect6 = (1100, (300 - counter), 100, 100, 100, 100, (100, 50, 0))
rect7 = (1300, 200, 100, 100, 100, 100, (0, 150, 0))
rect8 = (1400, 0, (200 - (counter * 2)), 100, 100, 100, (0, 250, 0))
rect9 = (1500, 100, 100, 100, 100, 100, (0,150, 0))
rect10 = (1700, 100-counter, 0-counter, 100, 200, 100, (0, 50, 100))
rect11 = (1700, 50-counter, 100-counter, 100, 200, 200, (0, 0, 180))
rect12 = (1700, 50-counter, -100-counter, 100, 200, 200, (0, 0, 220))
rect13 = (1700, -100-counter, 0-counter, 300, 200, 100, (0, 0, 240))
rect14 = (2000, 0, 100, 100, 100, 100, (0, 0, 250))
rect15 = (2200, -100, 100, 100, 100, 100, (0, 0, 255))

# Pygame initialization
pygame.init()

# Set up display
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Engine")

# Clock for controlling the frame rate
clock = pygame.time.Clock()


# 3D startpoint of given line
def point1(p1x, p1y, p1z):
    global x1, y1, z1
    x1, y1, z1 = p1x, p1y, p1z


# 3D endpoint of the same line
def point2(p2x, p2y, p2z):
    global x2, y2, z2
    x2, y2, z2 = p2x, p2y, p2z


# Start point of that line on the screen
def screenPoint1(sp1x, sp1y):
    global x1, y1
    x1, y1 = sp1x, sp1y


# Endpoint of that line on the screen
def screenPoint2(sp2x, sp2y):
    global x2, y2
    x2, y2 = sp2x, sp2y


# No lines rendered behind the camera!
def zClipping():
    global z1, z2, nearPlane, clipPercent, x1, x2, y1, y2, face
    if z1 < nearPlane or z2 < nearPlane:
        clipPercent = (nearPlane - z1) / (z2 - z1)
        if z1 < nearPlane:
            point1(x1 + ((x2 - x1) * clipPercent), y1 + ((y2 - y1) * clipPercent), nearPlane)
        else:
            if z2 < nearPlane:
                point2(x1 + ((x2 - x1) * clipPercent), y1 + ((y2 - y1) * clipPercent), nearPlane)


# Keeps the angles between -180 and 180 degrees
def confineAngle():
    global rotX, rotY
    if rotX > 180:
        rotX = -180
    if rotX < -180:
        rotX = 180
    if rotY > 180:
        rotY = -180
    if rotY < -180:
        rotY = 180


# Sine functions without being sine functions (parabolic functions, good enough)
def estimateTrig():
    global sinX, sinY, cosX, cosY, rotX, rotY
    confineAngle()
    if (rotX < -90):
        cosX = ((1/8100) * ((rotX + 180) * (rotX + 180))) - 1
    if (rotX > 90):
        cosX = ((1/8100) * ((rotX - 180) * (rotX - 180))) - 1
    if (rotX >= -90):
        if (rotX <= 90):
            cosX = (-(1/8100) * (rotX * rotX)) + 1
    if (rotY < -90):
        cosY = ((1/8100) * ((rotY + 180) * (rotY + 180))) - 1
    if (rotY > 90):
        cosY = ((1/8100) * ((rotY - 180) * (rotY - 180))) - 1
    if (rotY >= -90):
        if (rotY <= 90):
            cosY = (-(1/8100) * (rotY * rotY)) + 1
    if (rotX > 0):
        sinX = (-(1/8100) * ((rotX - 90) * (rotX - 90))) + 1
    if (rotX <= 0):
        sinX = ((1/8100) * ((rotX + 90) * (rotX + 90))) - 1
    if (rotY > 0):
        sinY = (-(1/8100) * ((rotY - 90) * (rotY - 90))) + 1
    if (rotY <= 0):
        sinY = ((1/8100) * ((rotY + 90) * (rotY + 90))) - 1


# Adding it all together to render lines
def drawLine(X1, Y1, Z1, X2, Y2, Z2, lineColor):
    global camX, camY, camZ, x1, x2, y1, y2
    point1(X1 - camX, Y1 - camY, Z1 - camZ)
    point2(X2 - camX, Y2 - camY, Z2 - camZ)
    point1((z1 * sinY) + (x1 * cosY), y1, (z1 * cosY) - (x1 * sinY))
    point2((z2 * sinY) + (x2 * cosY), y2, (z2 * cosY) - (x2 * sinY))
    point1(x1, (y1 * cosX) - (z1 * sinX), (y1 * sinX) + (z1 * cosX))
    point2(x2, (y2 * cosX) - (z2 * sinX), (y2 * sinX) + (z2 * cosX))
    if not (z1 < nearPlane and z2 < nearPlane):
        zClipping()
        screenPoint1(viewFactor * (x1 / z1), viewFactor * (y1 / z1))
        screenPoint2(viewFactor * (x2 / z2), viewFactor * (y2 / z2))
        pygame.draw.line(screen, lineColor, (x1 + 200, y1 + 200), (x2 + 200, y2 + 200), 5)


# Sort a list of rectangle origins furthest to closest from the camera
def sortList():
    global camX, camY, camZ, rect1s, rect2s, rect3s, rect4s, rect5s, rect6s, rect7s, rect8s, rect9s, rect10s, rect11s, rect12s, rect13s, rect14s, rect15, srectList, rectSlist, rectList

    rectList = [rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8, rect9, rect10, rect11, rect12, rect13, rect14, rect15]

    # Calculate distance from rectangle origins to the camera
    rect1s = abs((camX - rect1[0])) + abs((camY - rect1[1])) + abs((camZ - rect1[2]))
    rect2s = abs((camX - rect2[0])) + abs((camY - rect2[1])) + abs((camZ - rect2[2]))
    rect3s = abs((camX - rect3[0])) + abs((camY - rect3[1])) + abs((camZ - rect3[2]))
    rect4s = abs((camX - rect4[0])) + abs((camY - rect4[1])) + abs((camZ - rect4[2]))
    rect5s = abs((camX - rect5[0])) + abs((camY - rect5[1])) + abs((camZ - rect5[2]))
    rect6s = abs((camX - rect6[0])) + abs((camY - rect6[1])) + abs((camZ - rect6[2]))
    rect7s = abs((camX - rect7[0])) + abs((camY - rect7[1])) + abs((camZ - rect7[2]))
    rect8s = abs((camX - rect8[0])) + abs((camY - rect8[1])) + abs((camZ - rect8[2]))
    rect9s = abs((camX - rect9[0])) + abs((camY - rect9[1])) + abs((camZ - rect9[2]))
    rect10s = abs((camX - rect10[0])) + abs((camY - rect10[1])) + abs((camZ - rect10[2]))
    rect11s = abs((camX - rect11[0])) + abs((camY - rect11[1])) + abs((camZ - rect11[2]))
    rect12s = abs((camX - rect12[0])) + abs((camY - rect12[1])) + abs((camZ - rect12[2]))
    rect13s = abs((camX - rect13[0])) + abs((camY - rect13[1])) + abs((camZ - rect13[2]))
    rect14s = abs((camX - rect14[0])) + abs((camY - rect14[1])) + abs((camZ - rect14[2]))
    rect15s = abs((camX - rect15[0])) + abs((camY - rect15[1])) + abs((camZ - rect15[2]))

    rectSlist = [rect1s, rect2s, rect3s, rect4s, rect5s, rect6s, rect7s, rect8s, rect9s, rect10s, rect11s, rect12s, rect13s, rect14s, rect15s]

    # Sort distances from greatest to smallest
    rectList = [rect for _, rect in sorted(zip(rectSlist, rectList), key=lambda x: x[0], reverse=True)]
    
    return rectList


# What do you want to draw?
def render():
    global rectList, rectValues
    screen.fill((255, 255, 255))
    estimateTrig()
    sortList()

    rectValues = rectList[0]
    rect(rectValues[0], rectValues[1], rectValues[2], rectValues[3], rectValues[4], rectValues[5], rectValues[6])
    rectValues = rectList[1]
    rect(rectValues[0], rectValues[1], rectValues[2], rectValues[3], rectValues[4], rectValues[5], rectValues[6])
    rectValues = rectList[2]
    rect(rectValues[0], rectValues[1], rectValues[2], rectValues[3], rectValues[4], rectValues[5], rectValues[6])
    rectValues = rectList[3]
    rect(rectValues[0], rectValues[1], rectValues[2], rectValues[3], rectValues[4], rectValues[5], rectValues[6])
    rectValues = rectList[4]
    rect(rectValues[0], rectValues[1], rectValues[2], rectValues[3], rectValues[4], rectValues[5], rectValues[6])
    rectValues = rectList[5]
    rect(rectValues[0], rectValues[1], rectValues[2], rectValues[3], rectValues[4], rectValues[5], rectValues[6])
    rectValues = rectList[6]
    rect(rectValues[0], rectValues[1], rectValues[2], rectValues[3], rectValues[4], rectValues[5], rectValues[6])
    rectValues = rectList[7]
    rect(rectValues[0], rectValues[1], rectValues[2], rectValues[3], rectValues[4], rectValues[5], rectValues[6])
    rectValues = rectList[8]
    rect(rectValues[0], rectValues[1], rectValues[2], rectValues[3], rectValues[4], rectValues[5], rectValues[6])
    rectValues = rectList[9]
    rect(rectValues[0], rectValues[1], rectValues[2], rectValues[3], rectValues[4], rectValues[5], rectValues[6])
    rectValues = rectList[10]
    rect(rectValues[0], rectValues[1], rectValues[2], rectValues[3], rectValues[4], rectValues[5], rectValues[6])
    rectValues = rectList[11]
    rect(rectValues[0], rectValues[1], rectValues[2], rectValues[3], rectValues[4], rectValues[5], rectValues[6])
    rectValues = rectList[12]
    rect(rectValues[0], rectValues[1], rectValues[2], rectValues[3], rectValues[4], rectValues[5], rectValues[6])
    rectValues = rectList[13]
    rect(rectValues[0], rectValues[1], rectValues[2], rectValues[3], rectValues[4], rectValues[5], rectValues[6])
    rectValues = rectList[14]
    rect(rectValues[0], rectValues[1], rectValues[2], rectValues[3], rectValues[4], rectValues[5], rectValues[6])

    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 12, height // 35)
    screen.blit(text_surface, text_rect)       
    
    camX_text_surface = font.render(camX_text, True, (0, 0, 0))
    camX_text_rect = camX_text_surface.get_rect()
    camX_text_rect.center = (width // 12, height // 25)
    screen.blit(camX_text_surface, camX_text_rect)   
    
    camZ_text_surface = font.render(camZ_text, True, (0, 0, 0))
    camZ_text_rect = camZ_text_surface.get_rect()
    camZ_text_rect.center = (width // 12, height // 19)
    screen.blit(camZ_text_surface, camZ_text_rect)   
    
    camY_text_surface = font.render(camY_text, True, (0, 0, 0))
    camY_text_rect = camY_text_surface.get_rect()
    camY_text_rect.center = (width // 12, height // 15)
    screen.blit(camY_text_surface, camY_text_rect)   

    pygame.display.flip()


# Make a rectangle
def rect(x, y, z, length, width, height, color):
    global x1, x2, y1, y2, camX, camY, camZ, downVel
    Xdist, Ydist, Zdist, Xside, Yside, Zside = 0, 0, 0, 0, 0, 0

    if (x - 0.5 * width) < camX < (x + 0.5 * width) and \
   (z - 0.5 * length) < camZ < (z + 0.5 * length) and \
   (y - 0.5 * height) < camY < (y + 0.5 * height):
        if abs((camX - (x - 0.5 * width))) < abs((camX - (x + 0.5 * width))):
            Xdist = abs((camX - (x - 0.5 * width)))
            Xside = 0
        else:
            Xdist = abs((camX - (x + 0.5 * width)))
            Xside = 1

        if abs((camY - (y - 0.5 * height))) < abs((camY - (y + 0.5 * height))):
            Ydist = abs((camY - (y - 0.5 * height)))
            Yside = 0
        else:
            Ydist = abs((camY - (y + 0.5 * height)))
            Yside = 1

        if abs((camZ - (z - 0.5 * length))) < abs((camZ - (z + 0.5 * length))):
            Zdist = abs((camZ - (z - 0.5 * length)))
            Zside = 0
        else:
            Zdist = abs((camZ - (z + 0.5 * length)))
            Zside = 1

        if Xdist < Ydist and Xdist < Zdist:
            if Xside == 0:
                camX = (x - 0.5 * width)
            else:
                camX = (x + 0.5 * width)
        elif Ydist < Xdist and Ydist < Zdist:
            if Yside == 0:
                camY = (y - 0.5 * height)
                downVel = 0
            else:
                camY = (y + 0.5 * height)
        else:
            if Zside == 0:
                camZ = (z - 0.5 * length)
            else:
                camZ = (z + 0.5 * length)

    # Back of Rectangle
    drawLine(x + (0.5 * width), y + (0.5 * height)+50, z + (0.5 * length), x + (0.5 * width), y - (0.5 * height)+50, z + (0.5 * length), color)
    drawLine(x + (0.5 * width), y - (0.5 * height)+50, z + (0.5 * length), x - (0.5 * width), y - (0.5 * height)+50, z + (0.5 * length), color)
    drawLine(x - (0.5 * width), y - (0.5 * height)+50, z + (0.5 * length), x - (0.5 * width), y + (0.5 * height)+50, z + (0.5 * length), color)
    drawLine(x - (0.5 * width), y + (0.5 * height)+50, z + (0.5 * length), x + (0.5 * width), y + (0.5 * height)+50, z + (0.5 * length), color)

    # Front of rectangle
    drawLine(x + (0.5 * width), y + (0.5 * height)+50, z - (0.5 * length), x + (0.5 * width), y - (0.5 * height)+50, z - (0.5 * length), color)
    drawLine(x + (0.5 * width), y - (0.5 * height)+50, z - (0.5 * length), x - (0.5 * width), y - (0.5 * height)+50, z - (0.5 * length), color)
    drawLine(x - (0.5 * width), y - (0.5 * height)+50, z - (0.5 * length), x - (0.5 * width), y + (0.5 * height)+50, z - (0.5 * length), color)
    drawLine(x - (0.5 * width), y + (0.5 * height)+50, z - (0.5 * length), x + (0.5 * width), y + (0.5 * height)+50, z - (0.5 * length), color)

    # Connecting lines
    drawLine(x + (0.5 * width), y - (0.5 * height)+50, z - (0.5 * length), x + (0.5 * width), y - (0.5 * height)+50, z + (0.5 * length), color)
    drawLine(x - (0.5 * width), y - (0.5 * height)+50, z - (0.5 * length), x - (0.5 * width), y - (0.5 * height)+50, z + (0.5 * length), color)
    drawLine(x - (0.5 * width), y + (0.5 * height)+50, z - (0.5 * length), x - (0.5 * width), y + (0.5 * height)+50, z + (0.5 * length), color)
    drawLine(x + (0.5 * width), y + (0.5 * height)+50, z - (0.5 * length), x + (0.5 * width), y + (0.5 * height)+50, z + (0.5 * length), color)


jump_frames = 10

# Font setup
font = pygame.font.Font(None, 16)  # You can replace 'None' with a specific font file path if needed

# Initial text
counter_text = "counter =" + str(counter)
camX_text = str(camX)
camY_text = str(camY)
camZ_text = str(camZ)


# Main game loop

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    downVel += gravity
    if jump_frames < 5:
        downVel += 5
        jump_frames += 1
           
    if(downVel < -15):
        downVel = -15;
    camY -= downVel

    text = "counter =" + str(counter)
    camX_text = str(camX)
    camY_text = str(camY)
    camZ_text = str(camZ)





    # Check for key presses
    keysPressed = pygame.key.get_pressed()
    if keysPressed[K_a]:
        camX += -4 * cosY
        camZ += -4 * sinY
    if keysPressed[K_w]:
        camZ += 4 * cosY
        camX += -4 * sinY
    if keysPressed[K_s]:
        camZ += -4 * cosY
        camX += 4 * sinY
    if keysPressed[K_d]:
        camX += 4 * cosY
        camZ += 4 * sinY
    if keysPressed[K_SPACE]:
        if (jumpCounter > 50):
            jump_frames = 0
            jumpCounter = 0
        

    render()

    rel_x, rel_y = pygame.mouse.get_rel()
    rotY += -((9/10) * rel_x)
    rotX += ((9/20) * rel_y)
    
    counter += increment

    if counter >= 100 or counter <= 0:
        increment *= -1
        
    if camY >= 2000:
        camX = 100
        camY = -300
        camZ = 100

    rect6 = (1100, (300 - counter), 100, 100, 100, 100, (100, 50, 0))
    rect8 = (1400, 0, (200 - (counter * 2)), 100, 100, 100, (0, 250, 0))
    rect10 = (1700, 100-counter, 0-counter, 100, 200, 100, (0, 50, 100))
    rect11 = (1700, 50-counter, 100-counter, 100, 200, 200, (0, 0, 180))
    rect12 = (1700, 50-counter, -100-counter, 100, 200, 200, (0, 0, 220))
    rect13 = (1700, -100-counter, 0-counter, 300, 200, 100, (0, 0, 240))

    jumpCounter += 1
    clock.tick(stepsPerSecondthsw

