#intrepid mouse unexplainably going towards cheese in egocentric world

import pygame
from pygame.locals import *
import numpy as np
import sys, os, math, random, time

pygame.init()
screen = pygame.display.set_mode([1000,1000], RESIZABLE)
sqr = pygame.image.load("sqr.bmp").convert()
sqr = pygame.transform.scale(sqr, (200, 200))
squeeks = pygame.image.load("squeeks.bmp").convert()
squeeks = pygame.transform.scale(squeeks, (200, 200))
squeeks.set_colorkey((255,0,255))

def emptyRoom():
	global room
	room = [[0,0,0,0,0] for i in range(5)]
	room[2][2] = 1
	return room

#def emptyStates():


#def spawnCheese():


#def reward():


#def learnState():


def move():

	if up:
		mousepos[1]-=1
	if down:
		mousepos[1]+=1
	if left:
		mousepos[0]-=1
	if right:
		mousepos[0]+=1

def visual():
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
	for i in range(len(room)):
		for j in range(len(room)):
			screen.blit(sqr, (i*200,j*200))
			print(i,j)
			if room[i][j] == 1:
				screen.blit(squeeks, (i*200,j*200))
	pygame.display.update()


print(emptyRoom())

def main():
	while 1:
		emptyRoom()
		visual()
main()

'''
def train(traintime):
	while passedtime < traintime:
		emptyRoom()
		spawnCheese('random')
		while onCheese == False:
			move(states) #updates state


'''