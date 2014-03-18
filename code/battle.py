import sys, pygame, random
import config
from unit import PlayerChar, Enemy
from pygame.locals import *

# NEW TASK: change locations depending on number of characters
def init(player, enemy):
	#pygame.mixer.music.load("music/battleThemePlaceholder.wav")
	#pygame.mixer.music.play(-1, 0.0)
	player.setLoc(75, config.MENUTOP / 2 - 50, "right")
	enemy.setLoc(config.SCREENX - 200, config.MENUTOP / 2 - 50, "left")
	enemy.stats["curHP"] = enemy.stats["maxHP"]
	enemy.status = "normal"

	"""for player in playerChars:
		player.setLoc(75, MENUTOP / 2 - 50, "right")
	for enemy in enemies:
		enemy.setLoc(SCREENX - 200, MENUTOP / 2 - 50, "left")
		enemy.stats["curHP"] = enemy.stats["maxHP"]
		enemy.status = "normal"		
	"""


# NEW TASK: add game over mode and return "gameOver" when the enemy wins
def runBattle(playerChars, enemies):
	if getBattleStatus(playerChars, enemies) == "continue":
		playerPhase(units)
	else:
		return "overworld"
	if getBattleStatus(playerChars, enemies) == "continue":
		enemyPhase(units)
	else:
		return "overworld"


# return loss if all players are dead, victory if all enemies are dead, and continue if both sides are still alive
def getBattleStatus(playerChars, enemies):
	battleStatus = "loss"
	for player in playerChars:
		if player.status != "dead":
			battleStatus = "victory"
			break
	for enemy in enemies:
		if enemy.status != "dead":
			battleStatus = "continue"
	return battleStatus


# select all player actions
def playerPhase(playerChars, enemies):
	for player in playerChars:
		"do the thing"


# perform all enemy actions
def enemyPhase(playerChars, enemies):
	for enemy in enemies:
		accuracy = (random.random() + random.random()) / 2	# may need to modify
		enemy.attack(enemy.basicAttacks[0], accuracy, playerChars[0], DISPLAYSURF)


# award experience upon victory
def endBattle(playerChars, enemies, performance = 0.5):
	exp = 0
	for enemy in enemies:
		exp += enemies.expVal
	for playerChar in playerChars:
		playerChar.gainExperience(exp, performance)



