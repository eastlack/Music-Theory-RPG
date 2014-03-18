import sys, pygame, random
import config, battle
from unit import PlayerChar, Enemy
from pygame.locals import *

# initialize overworld with music [and other unimplemented things like character location]
# NEW TASK: initialize enemy locations randomly across map
def init(playerChars, enemies):
	for playerChar in playerChars:
		playerChar.setLoc(config.SCREENX / 2 - 150, config.SCREENY / 2 - 50, "right")
	for enemy in enemies:
		enemy.setLoc(config.SCREENX / 2 + 150, config.SCREENY / 2 - 50, "left")
	#pygame.mixer.music.load("music/overworldPlaceholder.wav")
	#pygame.mixer.music.play(-1, 0.0)


# run all unit actions in overworld
def runOverworld(playerChars, enemies, keys):
	for playerChar in playerChars:
		act(playerChar, keys)
		for enemy in enemies:
			enemy.wander()
			if areTouching(playerChar, enemy):
				battle.init(playerChar, enemy)
				return "battle"	


# return true if units are touching 
def areTouching(unit1, unit2):
	if unit1.x < unit2.x + unit2.width and unit1.x + unit1.width > unit2.x and unit1.y < unit2.y + unit2.height and	unit1.y + unit1.height > unit2.y:
		return True
	return False


# perform action in overworld based on keyboard input then blit image
def act(player, keys):
	if keys[K_RIGHT]:
		player.move("right")
	elif keys[K_LEFT]:
		player.move("left")
	elif keys[K_UP]:
		player.move("up")
	elif keys[K_DOWN]:
		player.move("down")
	player.draw(config.SCREEN)

