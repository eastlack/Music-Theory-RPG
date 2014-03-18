import sys, pygame, random
from unit import PlayerChar, Enemy
from pygame.locals import *

# print menu options and arrows in battle
def printBattleMenu(DISPLAYSURF, keys, actionArrow, actions, allyTurn, innerPanel):
	# print possible actions
	font = pygame.font.SysFont("timesNewRoman", 25)
	action0Surface = font.render("ATTACK", True, (0, 0, 0))
	action1Surface = font.render("ITEM", True, (200, 200, 200))
	action2Surface = font.render("GUARD", True, (0, 0, 0))
	action3Surface = font.render("RUN", True, (0, 0, 0))
	action0Rect = action0Surface.get_rect()
	action1Rect = action1Surface.get_rect()
	action2Rect = action2Surface.get_rect()
	action3Rect = action3Surface.get_rect()
	action0Rect.center = (SCREENX * 5 / 8, MENUTOP + 75 * .25)
	action1Rect.center = (SCREENX * 7 / 8, MENUTOP + 75 * .25)
	action2Rect.center = (SCREENX * 5 / 8, MENUTOP + 75 * .75)
	action3Rect.center = (SCREENX * 7 / 8, MENUTOP + 75 * .75)
	DISPLAYSURF.blit(action0Surface, action0Rect)
	DISPLAYSURF.blit(action1Surface, action1Rect)
	DISPLAYSURF.blit(action2Surface, action2Rect)
	DISPLAYSURF.blit(action3Surface, action3Rect)
	# display action selection box
	pygame.draw.line(DISPLAYSURF, (0, 0, 0), (0, MENUTOP), (SCREENX, MENUTOP), 3)						# top horizontal line
	pygame.draw.line(DISPLAYSURF, (0, 0, 0), (SCREENX / 2, MENUTOP), (SCREENX / 2, SCREENY), 3)				# center vertical line
	pygame.draw.line(DISPLAYSURF, (0, 0, 0), (SCREENX * .75, MENUTOP), (SCREENX * .75, SCREENY), 2)				# rightmost vertical line
	pygame.draw.line(DISPLAYSURF, (0, 0, 0), (SCREENX / 2, (MENUTOP + SCREENY) / 2), (SCREENX, (MENUTOP + SCREENY) / 2), 2)	# middle horizontal line	

	if allyTurn:
		# arrow for attack/item/guard/run
		if not innerPanel:
			if actionArrow % 4 == 0:
				pygame.draw.polygon(DISPLAYSURF, (252, 0, 0), ((action0Rect.left, action0Rect.centery), (action0Rect.left - 6, action0Rect.centery - 6), (action0Rect.left - 6, action0Rect.centery + 6)))
			elif actionArrow % 4 == 1:
				pygame.draw.polygon(DISPLAYSURF, (252, 0, 0), ((action1Rect.left, action1Rect.centery), (action1Rect.left - 6, action1Rect.centery - 6), (action1Rect.left - 6, action1Rect.centery + 6)))
			elif actionArrow % 4 == 2:
				pygame.draw.polygon(DISPLAYSURF, (252, 0, 0), ((action2Rect.left, action2Rect.centery), (action2Rect.left - 6, action2Rect.centery - 6), (action2Rect.left - 6, action2Rect.centery + 6)))
			elif actionArrow % 4 == 3:
				pygame.draw.polygon(DISPLAYSURF, (252, 0, 0), ((action3Rect.left, action3Rect.centery), (action3Rect.left - 6, action3Rect.centery - 6), (action3Rect.left - 6, action3Rect.centery + 6)))
		# arrow for specific attacks/items and description of selected one
		else:
			start = 0
			end = 69
			height = 0
			pygame.draw.polygon(DISPLAYSURF, (252, 0, 0), ((SCREENX / 2 + 8, 93 + 25 * actionArrow), (SCREENX / 2 + 2, 87 + 25 * actionArrow), (SCREENX / 2 + 2, 99 + 25 * actionArrow)))
			smallerFont = pygame.font.SysFont("timesNewRoman", 20)
	
			# print description, accounting for multiple lines
			if len(actions[actionArrow].description) > 69:
				while end < len(actions[actionArrow].description):
					assert height < 2, "Move description is too long"
					if end > len(actions[actionArrow].description):
						end = len(actions[actionArrow].description)
					else:
						while actions[actionArrow].description[end] != ' ':
							end -= 1
	 				descriptionSurface = smallerFont.render(actions[actionArrow].description[start:end], True, (0, 0, 0))
					descriptionRect = descriptionSurface.get_rect()
					descriptionRect.top = 5 + height * 20
					descriptionRect.left = SCREENX / 2 + 5
					DISPLAYSURF.blit(descriptionSurface, descriptionRect)
					start = end + 1
					end += 69
					height += 1
			descriptionSurface = smallerFont.render(actions[actionArrow].description[start:], True, (0, 0, 0))
			descriptionRect = descriptionSurface.get_rect()
			descriptionRect.top = 5 + height * 20
			descriptionRect.left = SCREENX / 2 + 5
			DISPLAYSURF.blit(descriptionSurface, descriptionRect)


# user input for overworld character control. Currently a placeholder.
def overworldUserInput(DISPLAYSURF, keys, leader):
	# placeholder overworld movement
	if keys[K_RIGHT]:
		leader.move("right", SCREENX, SCREENY)
	elif keys[K_LEFT]:
		leader.move("left", SCREENX, SCREENY)
	elif keys[K_UP]:
		leader.move("up", SCREENX, SCREENY)
	elif keys[K_DOWN]:
		leader.move("down", SCREENX, SCREENY)


# variable initializations
SCREENX = 1275
SCREENY = 750
MENUTOP = SCREENY - 75

mode = "overworld"
newMode = True
showAttacks = False
showItems = False
allyTurn = True
wanderLoop = (0, 0)
actionArrow = 0		# indicates where action selection arrow is
accuracy = 0.0

pygame.init()
DISPLAYSURF = pygame.display.set_mode((SCREENX, SCREENY))
pygame.display.set_caption("Music Theory RPG")
FPSclock = pygame.time.Clock()

tallis = PlayerChar("Tallis", 1, "pianist", 20, 20, 20, "images/allyPlaceholder")
tallis.addBasicAttack("Seconds", 10, "Play a minor or major second. Maybe it will annoy the enemy enough to make them leave you alone.")
tallis.addBasicAttack("Night of Nights", 80, "Use time magic to slice your opponent to pieces.")
tallis.addBasicAttack("Death Waltz", 90, "Damage and confuse your opponent with Cool&Create's hyperactive and frequently misnomered remix of ZUN's 'UN Owen Was Her?', composed for the Touhou Project Series. Has nothing to do with John Stump.")
tallis.addBasicAttack("Senbonzakura", 100, "Summon a thousand cherry trees from the earth to crush your foe.")
tallis.setLoc(50, 150, "right")

enemy = Enemy(10, "Marhot", 1, "flautist", 20, 20, 20, "images/enemyPlaceholder")
enemy.addBasicAttack("Seconds", 10, "Play a minor or major second. Maybe it will annoy the enemy enough to make them leave you alone.")
enemy.setLoc(445, 150, "left")

while True:
	DISPLAYSURF.fill((255, 255, 255))	# white background
	keys = pygame.key.get_pressed()		# all currently pressed keys
	tallis.draw(DISPLAYSURF)			# draw protagonist
	enemy.draw(DISPLAYSURF)				# draw enemy

	# all user input unaffected by holding down keys goes here
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if mode == "battle":
			# cursor movement
			if event.type == KEYDOWN:
				if event.key == K_x:	# select action with x
					if showAttacks:		# use specific attack
						accuracy = tallis.basicAttacks[actionArrow].calcAccuracy()
						tallis.attack(tallis.basicAttacks[actionArrow], accuracy, enemy, DISPLAYSURF)
						showAttacks = False
						actionArrow = 0
						allyTurn = False
					else:			# select general action
						if(actionArrow % 4 == 0):	# attack
							actionArrow = 0
							showAttacks = True
						elif(actionArrow % 4 == 1):	# item
							showItems = True	# currently only shows empty inventory
						elif(actionArrow % 4 == 2):	# defend
							tallis.defend()
							actionArrow = 0
							allyTurn = False
						elif(actionArrow % 4 == 3):	# run
							showItems = False
							mode = "overworld"
							newMode = True
				elif event.key == K_z:		# go back with z
					showAttacks = False
					showItems = False
					actionArrow = 0

				if showAttacks:		# attack selection with arrows
					if event.key == K_UP:
						actionArrow -= 1
					elif event.key == K_DOWN:
						actionArrow += 1
					if actionArrow < 0:
						actionArrow = 0
					elif actionArrow >= len(tallis.basicAttacks):
						actionArrow = len(tallis.basicAttacks) - 1
				elif showItems:		# item selection with arrows [unimplemented; currently assuming empty inventory]
					actionArrow = 0
				else:			# general action selection with arrows
					if event.key == K_RIGHT:	# move selection arrow right with right key
						actionArrow += 1
					elif event.key == K_LEFT:	# move selection arrow left with left key
						actionArrow -= 1
					elif event.key == K_UP or event.key == K_DOWN:	# move selection arrow up/down with up/down key
						actionArrow += 2


	# overworld movement and interaction mechanics
	if mode == "overworld":
		# initialize overworld
		if newMode:
			newMode = False
			tallis.setLoc(SCREENX / 2 - 150, SCREENY / 2 - 50, "right")
			enemy.setLoc(SCREENX / 2 + 150, SCREENY / 2 - 50, "left")
			pygame.mixer.music.load("music/overworldPlaceholder.wav")
			pygame.mixer.music.play(-1, 0.0)

		# all unit movement
		overworldUserInput(DISPLAYSURF, keys, tallis)
		wanderLoop = enemy.wander(SCREENX, SCREENY, wanderLoop[0], wanderLoop[1])

		# begin battle mode if player/enemy touch
		if(tallis.x > enemy.x - 100 and tallis.x < enemy.x + 100 and tallis.y > enemy.y - 100 and tallis.y < enemy.y + 100):
			mode = "battle"
			newMode = True

	# print battle layout
	elif mode == "battle":
		# initialize battle sequence
		if newMode:
			enemy.stats["curHP"] = enemy.stats["maxHP"]
			enemy.status = "normal"
			newMode = False
			showAttacks = False
			showItems = False
			allyTurn = True
			actionArrow = 0
			tallis.setLoc(75, MENUTOP / 2 - 50, "right")
			enemy.setLoc(SCREENX - 200, MENUTOP / 2 - 50, "left")
			pygame.mixer.music.load("music/battleThemePlaceholder.wav")
			pygame.mixer.music.play(-1, 0.0)

		# display award exp and return to overworld upon victory
		if enemy.status == "dead":
			mode = "overworld"
			newMode = True

		# show selection box for attacks or items
		if showAttacks or showItems:
			pygame.draw.rect(DISPLAYSURF, (64, 64, 255), (SCREENX / 2, 0, SCREENX / 2, MENUTOP))		# menu background
			pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (SCREENX / 2, 0, SCREENX / 2, MENUTOP), 3)		# menu border
			pygame.draw.line(DISPLAYSURF, (0, 0, 0), (SCREENX / 2, 75), (SCREENX, 75), 3)			# description lower border
		
		# print attacks in selection box
		if showAttacks:
			lineNum = 0
			font = pygame.font.SysFont("timesNewRoman", 25)
			for i in tallis.basicAttacks:
				attackSurface = font.render(i.name, True, (0, 0, 0))
				powerSurface = font.render(str(i.power), True, (0, 0, 0))
				attackRect = attackSurface.get_rect()
				powerRect = powerSurface.get_rect()
				attackRect.left = SCREENX / 2 + 10
				attackRect.top = 80 + 25 * lineNum
				powerRect.right = SCREENX - 10
				powerRect.top = 80 + 25 * lineNum
				DISPLAYSURF.blit(attackSurface, attackRect)
				DISPLAYSURF.blit(powerSurface, powerRect)
				lineNum += 1				

		tallis.showHPbar(DISPLAYSURF, SCREENY)
		printBattleMenu(DISPLAYSURF, keys, actionArrow, tallis.basicAttacks, allyTurn, showAttacks)

		# simple enemy AI
		if not allyTurn:
			allyTurn = True
			if enemy.status != "dead":
				accuracy = (random.random() + random.random()) / 2	# may need to modify
				enemy.attack(enemy.basicAttacks[0], accuracy, tallis, DISPLAYSURF)
	else:
		print "INVALID MODE DETECTED. EXPECTED 'battle' OR 'overworld', INSTEAD FOUND " + mode
	pygame.display.update()
	FPSclock.tick(30)

print "DONE"