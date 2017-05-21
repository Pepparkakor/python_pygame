#2D gravity simulator
import numpy as np
import random, string, math, time 
from operator import add 
import pygame
from pygame.locals import *
import os, sys

pygame.init()
FPS = 60
res = [1920, 1080]
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(res, RESIZABLE)
white = (255, 255, 255)
black = (0,0,0)
objects = []
font = pygame.font.Font(None, 36)



#random name gen, src:"http://pythonfiddle.com/random-word-generator/"
vowels = list('aeiou')

def gen_word(min, max):
    word = ''
    syllables = min + int(random.random() * (max - min))
    for i in range(0, syllables):
        word += gen_syllable()
    return word.capitalize()


def gen_syllable():
    ran = random.random()
    if ran < 0.333:
        return word_part('v') + word_part('c')
    if ran < 0.666:
        return word_part('c') + word_part('v')
    return word_part('c') + word_part('v') + word_part('c')


def word_part(type):
    if type is 'c':
        return random.sample([ch for ch in list(string.ascii_lowercase) if ch not in vowels], 1)[0]
    if type is 'v':
        return random.sample(vowels, 1)[0]

def newName():
    for i in range(0, 10):
        return gen_word(2,4)

def drawCircle(pos, radius, color, name):
    pos = (int(pos[0]),int(pos[1]))
    pygame.draw.circle(screen, color, pos, radius)
    text = font.render(name, 25, (255, 255, 255))
    text_rect = text.get_rect(center=(pos))
    screen.blit(text,text_rect)

def newObject(pos, radius):
    name = newName()
    color = (random.randrange(0, 255),random.randrange(0, 255),random.randrange(0, 255))
    velocity = [1,0]
    global objects
    props = [pos, radius, name, color, velocity]
    objects.append(props)
    print("Last object:", objects[-1])

def Distance(o1, o2):
    global objects
    dist = ((o2[0][0]-o1[0][0]),(o2[0][1]-o1[0][1]))
    #visualization
    #pygame.draw.line(screen, white, o1[0], o2[0], 1)
    return dist

def vectorSum(vectors):
    #format(from 0,0):[(1,2),(-1,3),(3,0)...]
    vectorstack=[0]
    if vectors != []:
        vectorstack = list(zip(*vectors))
        vectorsum = [sum(vectorstack[0]), sum(vectorstack[1])]
        return vectorsum
    else:
        return [0,0]

def Collision(o1, o2):
    global objects
    '''pos =  
    objects[objects.index(o1)] = [pos, radius, name, color, velocity]'''
    if o1 != o2:
        #print('Collision:', o1,o2)
        pass
    else:
        pass

def Physics():
    global objects
    density = 1
    for p in range(len(objects)):
        vectors = []
        po = objects[p]
        pos1 = po[0]
        radius1 = po[1]
        velocity1 = po[4]
        area1 = 3.1415*radius1**2
        mass1 = area1*density
        for q in objects:
            pos2 = q[0]
            radius2 = q[1]
            velocity2 = q[4]
            area2 = 3.1415*radius2**2
            mass2 = area2*density
            distancevector = Distance(po, q)
            distance = math.hypot(distancevector[0], (distancevector[1]))
            if distance <= po[1]+q[1]:
                Collision(po, q)
            else:
                cos = distancevector[0]/distance
                sin = distancevector[1]/distance
                accer = (mass2/(distance**2))*(10**0)
                accervector = [cos*accer, sin*accer]
                vectors.append(accervector)
            vectorsum = vectorSum(vectors)
            objects[p][4] = list(tuple(map(add, po[4], vectorsum)))

def main():
    global screen, objects
    #newObject([res[0]/2,res[1]/2], 200)
    while True:
        screen.fill(black)
        events = pygame.event.get
        
        for event in events():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.key == K_SPACE:
                    pos = [random.randrange(int(res[0]*0.05), int(res[0]*0.95)), random.randrange(int(res[1]*0.05), int(res[1]*0.95))]
                    radius = random.randrange(3, 40)
                    newObject(pos, radius)
        
        if event.type == VIDEORESIZE:
            res[0] = event.w
            res[1]= event.h
            screen = pygame.display.set_mode(res, RESIZABLE)
        i = 0
        while i < len(objects):
            objects[i][0] = list(tuple(map(add, objects[i][0], objects[i][4])))
            drawCircle(objects[i][0],objects[i][1],objects[i][3],objects[i][2])
            radboxw = objects[i][0][0]+objects[i][1]
            radboxh = objects[i][0][1]+objects[i][1]
            if radboxw >= res[0] or radboxw <= 0:
                objects[i][4][0] = 0-objects[i][4][0]
            elif radboxh <= 20 or radboxh >= res[1]:
                objects[i][4][1] = 0-objects[i][4][1]
            i+=1
        if objects != []:
            objects[0][4]=[0,0]
        pygame.event.pump()
        mousepos = pygame.mouse.get_pos()
        Physics()
        pygame.display.update()
        fpsClock.tick(FPS)

main()