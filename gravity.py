###########################################################
###### 2D gravity simulator ###################################
######### SPACE - spawn new planet at mouse position ###########
######### UP / DOWN - increase/decrease speed  of simulation#####
######### g - toggle gravity ##################################
##########################################################

import numpy as np
import random, string, math, time 
from operator import add 
import pygame
from pygame.locals import *
import os, sys

pygame.init()
FPS = 60
c = 0
density = 10
infoObject = pygame.display.Info()
tempresx = infoObject.current_w
tempresy = infoObject.current_h
res = [1920, 1080]
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(res, RESIZABLE)
white = (255, 255, 255)
black = (0,0,0)
objects = []
font = pygame.font.Font(None, 36)
img = ["images/earth.png","neptune.png"]
planetimg = pygame.image.load(img[0]).convert_alpha()
resx_ratio = res[0]/tempresx
resy_ratio = res[1]/tempresy

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

#actual engine starts here
def drawCircle(pos, radius, color, name):
	pos = (int(pos[0]),int(pos[1]))
	circle = pygame.draw.circle(screen, color, pos, radius)
	#text = font.render(name, 25, (255, 255, 255))
	#text_rect = text.get_rect(center=(pos))
	#screen.blit(text,text_rect)
	#disp_img = pygame.transform.scale(planetimg, (int(radius*2.7), int(radius*2.7)))
	#img_rect = disp_img.get_rect(center=pos)
	#screen.blit(disp_img, img_rect)

def newObject(pos, radius):
	name = newName()
	color = (random.randrange(0, 255),random.randrange(0, 255),random.randrange(0, 255))
	velocity = [0,0]
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
	#format(from 0,0):[[1,2],[-1,3],[3,0]...]
	vectorstack=[]
	if vectors != []:
		vectorstack = list(zip(*vectors))
		vectorsum = [sum(vectorstack[0]), sum(vectorstack[1])]
		return vectorsum
	else:
		return [0,0]

def Collision(o1, o2, distancevector, mass1, mass2):
	global objects
	if o1 != o2:
		pos = [((o2[1])/(o1[1]+o2[1]))*distancevector[0] + o1[0][0], ((o2[1])/(o1[1]+o2[1]))*distancevector[1] + o1[0][1]]
		radius = o1[1] + o2[1]
		name = o1[2] + o2[2]
		color = [(o1[3][0]+o2[3][0])/2,(o1[3][1]+o2[3][1])/2,(o1[3][2]+o2[3][2])/2]
		mass = mass1 + mass2
		impulse1 = [mass1*o1[4][0], mass1*o1[4][1]]
		impulse2 = [mass2*o2[4][0], mass2*o2[4][1]]
		impulsesum = vectorSum([impulse1, impulse2])
		try:
			velocity = [(impulsesum[0]/mass*0.5), (impulsesum[1]/mass)*0.5]
		except ZeroDivisionError:
			velocity = [0,0]
		objects[objects.index(o1)] = [pos, radius, name, color, velocity]
		oj = objects[objects.index(o2)]
		del objects[objects.index(o2)]
		return oj
	else:
		return False
def Box():
	global objects
	i = 0
	while i < len(objects):
		objects[i][0] = list(tuple(map(add, objects[i][0], objects[i][4])))
		drawCircle(objects[i][0],objects[i][1],objects[i][3],objects[i][2])
		radboxw = [int(objects[i][0][0]-objects[i][1]), int(objects[i][0][0]+objects[i][1])]
		radboxh = [int(objects[i][0][1]-objects[i][1]), int(objects[i][0][1]+objects[i][1])]
		for x in range(radboxw[0],radboxw[1]): 
			if x not in range(res[0]):
				objects[i][4][0] = 0-objects[i][4][0]
		for y in range(radboxh[0],radboxh[1]): 
			if y not in range(res[1]):
				objects[i][4][1] = 0-objects[i][4][1]
		i+=1
def recursiveGravity(Objects):
	global density, c

	if c >= len(Objects):
		doneWithLoop = True
		c = 0
	else:
		z = 1
		while z < len(Objects):
			if z < len(Objects):
				p = Objects[0]
				pos1 = p[0]
				radius1 = p[1]
				velocity1 = p[4]
				area1 = 3.1415*radius1**2
				mass1 = area1*density
				q = Objects[z]
				pos2 = q[0]
				radius2 = q[1]
				velocity2 = q[4]
				area2 = 3.1415*radius2**2
				mass2 = area2*density
				distancevector = Distance(p, q)
				distance = math.hypot(distancevector[0], (distancevector[1]))
				if distance <= p[1]+q[1]:
					try: 
						del Objects[Objects.index(Collision(p, q, distancevector, mass1, mass2))] 
					except ValueError:
						pass

				else:
					cos = distancevector[0]/distance
					sin = distancevector[1]/distance
					accer1 = (mass2/(distance**2))*(10**0)
					accer2 = (mass1/(distance**2))*(10**0)
					accervector1 = [cos*accer1, sin*accer1]
					accervector2 = [-accervector1[0], -accervector1[1]]
					try:
						objects[objects.index(p)][4] = vectorSum([accervector1, objects[objects.index(p)][4]])
					except ValueError:
						pass
					objects[z][4] = vectorSum([accervector2, objects[z][4]])
					z+=1  

		c+=1	
		recursiveGravity(Objects[1:])

def Physics():
	global objects
	if len(objects) >= 2:
		recursiveGravity(objects)

def main():
	global screen, objects, resx_ratio, resy_ratio, density, FPS
	#newObject([res[0]/2,res[1]/2], 200)
	while True:
		screen.fill(black)
		events = pygame.event.get
		pygame.event.pump()
		mousepos = pygame.mouse.get_pos()
		
		for event in events():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
						pygame.quit()
						sys.exit()
				if event.key == K_r:
						try: 
							del objects[-1]
						except IndexError:
							pass
				if event.key == K_g:
					if density == 0:
						density = 10
					else:
						density = 0
				elif event.key == K_SPACE:
					#if mousepos in list_of_areas:
					#pos = [random.randrange(int(res[0]*0.05), int(res[0]*0.95)), random.randrange(int(res[1]*0.05), int(res[1]*0.95))]
					#radius = random.randrange(3, 40)
					pos = [mousepos[0]*resx_ratio, mousepos[1]*resy_ratio]
					radius = 50
					newObject(pos, radius)
		if event.type == VIDEORESIZE:
			tempresx = event.w
			tempresy= event.h
			screen = pygame.display.set_mode(res, RESIZABLE)
			resx_ratio = res[0]/tempresx
			resy_ratio = res[1]/tempresy
			res[0], res[1] = tempresx, tempresy
		
		#if objects != []:
		#	objects[0][4]=[0,0]
		Box()
		Physics()
		pygame.display.update()
		fpsClock.tick(FPS)

main()