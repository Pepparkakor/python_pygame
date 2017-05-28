#intrepid mouse unexplainably going towards cheese in allocentric world

import pygame
from pygame.locals import *
import numpy as np
import sys, os, math, random, time


pygame.init()
screen = pygame.display.set_mode([750,750], RESIZABLE)
sqr = pygame.image.load("sqr.bmp").convert()
sqr = pygame.transform.scale(sqr, (75, 75))
squeeks = pygame.image.load("squeeks.bmp").convert()
squeeks = pygame.transform.scale(squeeks, (75, 75))
cheese = pygame.image.load("cheese.png").convert_alpha()
cheese = pygame.transform.scale(cheese, (75, 75))
squeeks.set_colorkey((255,0,255))
visdist = 2
onCheese = False
episodes = np.array([0,0,0])
episode = np.array([])

def emptyRoom():
	global room, mousepos
	room = np.zeros((10,10))
	mousepos = [0,0]
	room[mousepos[0]][mousepos[1]]= 2
	return room

#def emptyStates():

def spawnCheese():
	global room
	cheesepos = [random.randrange(10),random.randrange(10)]
	while cheesepos == mousepos:
		cheesepos = [random.randrange(10),random.randrange(10)]
	room[cheesepos[0]][cheesepos[1]] = 1


def reward():
	global onCheese
	if onCheese == True:
		return 100

		
def sliceMouse():
	global room, visdist, mousepos, state
	xleft = mousepos[0]-visdist
	yleft = mousepos[1]-visdist
	xright = mousepos[0]+visdist+1
	yright = mousepos[1]+visdist+1

	if xleft<0:
		xleft = 0
	if yleft<0:
		yleft = 0

	state = room[xleft: xright, yleft: yright]
	return state

def move(d):
	global mousepos, onCheese
	direction = d
	temp = list(mousepos)
	if direction == 0 and mousepos[0]>0:
		mousepos[0]-=1
	if direction == 1 and mousepos[0]<9:
		mousepos[0]+=1
	if direction == 2 and mousepos[1]>0:
		mousepos[1]-=1
	if direction == 3 and mousepos[1]<9:
		mousepos[1]+=1
	room[temp[0]][temp[1]] = 0
	if room[mousepos[0]][mousepos[1]] == 1:
		onCheese = True
	room[mousepos[0]][mousepos[1]] = 2

def control():
	events = pygame.event.get
	pygame.event.pump()
	for event in events():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key == K_r:
				emptyRoom()
				spawnCheese()
			if event.key == K_UP:
				move(0)
			if event.key == K_DOWN:
				move(1)
			if event.key == K_LEFT:
				move(2)	
			if event.key == K_RIGHT:
				move(3)
		sliceMouse()
		saveState()
def visual():
	global room
	for i in range(len(room)):
		for k in range(len(room)):
			screen.blit(sqr, (k*75,i*75))
			if room[i][k] == 2:
				screen.blit(squeeks, (k*75,i*75))
			if room[i][k] == 1:
				screen.blit(cheese, (k*75,i*75))
	pygame.display.update()

def saveState():
	global episode, state
	episode = np.dstack((episode,  [state]))
	print(episodes)

def decide():
	global episodes, state



def train():
	global onCheese, episode, episodes
	emptyRoom()
	spawnCheese()

	while 1:
		screen.fill((0,0,0))
		control()
		visual()
		if onCheese == True:
			spawnCheese()
			onCheese = False
			episodes = np.append(episodes, episode)
			episode = np.array([])
		
		decide()
		
train()
