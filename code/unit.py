import sys, pygame, random
from basicAttack import BasicAttack
from pygame.locals import *

# general framework of units
# children: PlayerChar, Enemy
class Unit(object):
	# create a unit with the given name, class, and stats, initializing at full HP
	def __init__(self, name, level, unitClass, HP, melody, rhythm, imgLoc):	
		# class statistics
		self.stats = {}
		self.basicAttacks = []
		self.name = name
		self.unitClass = unitClass
		self.level = level
		self.totalExp = 0
		self.expAtNext = int(4 * (level ** 3.15) + 10)
		self.expToNext = self.expAtNext - self.totalExp

		# battle statistics
		self.status = "normal"
		self.stats["maxHP"] = HP
		self.stats["curHP"] = HP
		self.stats["melody"] = melody
		self.stats["rhythm"] = rhythm

		# drawing data
		self.x = 0
		self.y = 0
		self.imgLoc = imgLoc
		self.direction = "down"


	# print out name, class, all stats, and all learned moves
	def printSummary(self):
		print self.name
		print "level " + str(self.level) + ' ' + self.unitClass
		print "Total EXP: " + str(self.totalExp)
		print "Next: " + str(self.expAtNext)
		print "Remaining: " + str(self.expToNext)
		print "HP: " + str(self.stats["curHP"]) + " / " + str(self.stats["maxHP"])
		print "Melody: " + str(self.stats["melody"])
		print "Rhythm: " + str(self.stats["rhythm"])

		print "Basic Attacks:"
		for i in self.basicAttacks:
			print "   " + i.name + " " + i.power + ": " + i.description
		print ""


	# learn a new basic attack
	def addBasicAttack(self, name, power, description):
		newAttack = BasicAttack(name, power, description)
		self.basicAttacks.append(newAttack)


	# Take the given amount of damage. Use negative values for recovery.
	def takeDamage(self, dmg, DISPLAY):
#		print self.name + " took " + str(dmg) + " damage."


		# CURRENTLY TRYING TO MAKE THE VALUE SHOW ABOVE THE TARGET'S HEAD AND DRIFT UPWARDS
		font = pygame.font.SysFont("timesNewRoman", 25)
		if dmg >= 0:	# red for damage
			dmgSurface = font.render(str(dmg), True, (255, 0, 0))
		else:		# green for healing
			dmgSurface = font.render(str(dmg), True, (0, 255, 0))
		dmgRect = dmgSurface.get_rect()
		dmgRect.midbottom = (self.x + 50, self.y)
		i = 0
		while i < 5:
			i += 1
			dmgRect.bottom -= 1
			pygame.draw.rect(DISPLAY, (255, 255, 255), (dmgRect.left, dmgRect.top, dmgRect.right - dmgRect.left, dmgRect.bottom - dmgRect.top), 1)
			DISPLAY.blit(dmgSurface, dmgRect)
			pygame.display.update()
			pygame.time.wait(100)
		


		self.stats["curHP"] -= dmg

		# HP will never exceed maximum or be negative
		if self.stats["curHP"] > self.stats["maxHP"]:
			self.stats["curHP"] = self.stats["maxHP"]
		elif self.stats["curHP"] <= 0:
			self.stats["curHP"] = 0
			self.status = "dead"
			print self.name + " died."


	# attack a target to deal damage
	# also checks for victory and awards experience accordingly
	def attack(self, move, accuracy, target, DISPLAY):
		if move in self.basicAttacks:
			attack = self.stats["melody"]
			defense = target.stats["melody"]
			dmg = attack * move.power * move.power * accuracy * accuracy / defense / 15
			print self.name + " used " + move.name + " on " + target.name
			if target.status == "defend":
				dmg /= 2
			target.takeDamage(int(dmg), DISPLAY)
			if isinstance(self, PlayerChar) and target.status == "dead":
				self.getExp(target, accuracy)
		else:
			print "ERROR: " + self.name + " used invalid move " + move + " on " + target.name


	# change the x y position and direction
	def setLoc(self, xPos, yPos, direction):
		self.x = xPos
		self.y = yPos
		self.direction = direction


	# move in specified direction and changing image to face that direction
	def move(self, direction, screenX, screenY):
		if(direction == "right"):
			self.direction = direction
			if self.x < screenX - 100:
				self.x += 4
		elif(direction == "left"):
			self.direction = direction
			if  self.x >= 4:
				self.x -= 4
		elif(direction == "up" and self.y >= 4):
			self.direction = direction
			if self.y >= 4:
				self.y -= 4
		elif(direction == "down" and self.y < screenY - 100):
			self.direction = direction
			if self.y < screenY - 100:
				self.y += 4
		

	# draw unit on screen
	def draw(self, screen):
		image = pygame.image.load(self.imgLoc + '/' + self.direction + ".png")
		screen.blit(image, (self.x, self.y))



class PlayerChar(Unit):

	# change player status 
	def defend(self):
		self.status = "defend"
		print self.name + " defended."

	# gain experience and check for leveling up
	def getExp(self, target, accuracy):
		print "Defeated enemy!"
		print "Gained " + str(target.expVal) + " experience"
		self.totalExp += target.expVal * accuracy
		if self.totalExp >= self.expAtNext:
			self.levelUp()


	# increase level by one, recalculate experience for next level, and increase stats
	def levelUp(self):
		self.level += 1
		self.expToNext = int(4 * (self.level ** 3.15) + 10)

		"""

		figure out how you want stat gains to work and put the code here

		"""


	# displays unit name, HP filled green to current percent, and integer values of current and maximum health
	# place in correct Y position based on y length of screen
	# potential errors: will not work without correct font installed on computer
	def showHPbar(self, screen, screenY):
		X = 10
		Y = screenY - 40
		length = 80
		height = 20

		# draw bar
		pygame.draw.rect(screen, (0, 255, 0), (X, Y, int(length * self.stats["curHP"] / self.stats["maxHP"]), height))	# shows percent remaining HP as green bar
		pygame.draw.rect(screen, (0, 0, 0), (X, Y, length, height), 1)		# shows maximum HP as black border
		
		# create text surfaces
		font = pygame.font.SysFont("timesNewRoman", 18)
		
		slashSurface = font.render(" / ", True, (0, 0, 0))
		HPleftSurface = font.render(str(self.stats["curHP"]), True, (0, 0, 0))
		HPtotalSurface = font.render(str(self.stats["maxHP"]), True, (0, 0, 0))
		nameSurface = font.render(self.name, True, (0, 0, 0))

		# create rectangles of surfaces
		slashRect = slashSurface.get_rect()
		HPleftRect = HPleftSurface.get_rect()
		HPtotalRect = HPtotalSurface.get_rect()
		nameRect = nameSurface.get_rect()

		# move text to their respective locations
		slashRect.center = (X + length / 2, Y + height / 2)
		HPleftRect.topright = slashRect.topleft
		HPtotalRect.topleft = slashRect.topright
		nameRect.midbottom = (X + length / 2, Y)

		# print text
		screen.blit(slashSurface, slashRect) 
		screen.blit(HPleftSurface, HPleftRect)
		screen.blit(HPtotalSurface, HPtotalRect)
		screen.blit(nameSurface, nameRect)



class Enemy(Unit):
	def __init__(self, expVal, name, level, unitClass, HP, melody, rhythm, imgLoc):
		Unit.__init__(self, name, level, unitClass, HP, melody, rhythm, imgLoc)
		self.expVal = expVal	# maximum amount of experience gained from defeating

	# randomly move around overworld, avoiding edge of screen
	def wander(self, screenX, screenY, loop, direction):
		loop -= 1
		if loop <= 0:
			loop = random.randint(1, 30)
			direction = random.randint(0, 5)
		if direction == 0:
			self.move("right", screenX, screenY)
		elif direction == 1:
			self.move("left", screenX, screenY)
		elif direction == 2:
			self.move("up", screenX, screenY)
		elif direction == 3:
			self.move("down", screenX, screenY)
		return (loop, direction)

