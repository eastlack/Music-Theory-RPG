import sys, pygame
import config
from pygame.locals import *


# draws arrow to cycle through given locations based on input
class arrow(object):

	# start with no given locations
	def __init__(self, moveFunc = squareMoveFunc):
		self.locs = []				# list of possible locations of arrow
		self.loc = 0				# current location on list
		self.moveFunc = moveFunc	# function that calculates changes in loc based on input
		self.visible = True


	# add new potential pixel location
	def addLoc(self, newLoc):
		self.locs.append(newLoc)


	# change arrow location based on input
	def changeLoc(self, keys):
		self.loc += self.moveFunc(keys)
		self.loc = self.loc % len(self.locs)


	# move arrow around a square
	def squareMove(self):
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RIGHT: return 1
				elif event.key == K_RIGHT: return -1
				elif event.key == K_UP: return 2
				elif event.key == K_DOWN: return -2


	# set whether or not arrow should be displayed
	def setVisility(self, visibility):
		self.visible = visibility


	# determine arrow coordinates and blit to screen
	def display(self):
		if self.visible:
			point = self.locs[self.loc]
			top = (self.locs[self.loc][0] - 6, self.locs[self.loc][1] - 6)
			bottom = (self.locs[self.loc][0] - 6, self.locs[self.loc][1] + 6)
			pygame.draw.polygon(DISPLAY, (252, 0, 0), point, top, bottom)


