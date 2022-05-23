import pygame
import time
import random

pygame.init()
pygame.font.init()


pygame.display.set_caption("MILKY_WAY2")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)


WIDTH = 600
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
FONT = pygame.font.SysFont("comicsans",30)
RUN = True
FPS = 60
SCORE = 0
LEVEL = 0
LIFES = 5

class ship:
	def __init__(self):
		self.x = None
		self.y = None
		self.health = None
		self.max_health = None
		self.damage = None
		self.image = None
		self.laser = None
		self.lasers = None
		self.laser_sound = None
		self.mask = None
		self.velocity = None
		self.randomness = None
		self.randomness_choice = None
		self.laser_velocity = None
		self.reload_time = None
		self.reload_timer = None

	def move_left(self):
		self.x -= self.velocity

	def move_right(self):
		self.x += self.velocity

	def move_up(self):
		self.y -= self.velocity

	def move_down(self):
		self.y +=self.velocity

	def reload(self):
		if self.reload_timer >= self.reload_time:
			self.reload_timer = 0
		elif self.reload_timer > 0:
			self.reload_timer += 1

	def shoot(self):
		if self.reload_timer == 0:
			laser = Laser(self.x + 27,self.y,self.laser,self.laser_velocity)
			self.lasers.append(laser)
			self.reload_timer = 1

	def draw(self):
		for laser in self.lasers:
			laser.draw()
		WINDOW.blit(self.image,(self.x,self.y))

	def get_width(self):
		return self.image.get_width()

	def get_height(self):
		return self.image.get_height()

class player_ship(ship):
	def __init__(self):
		super().__init__()
		self.x = 268
		self.y = 526
		self.health = 100
		self.max_health = 100
		self.damage = 10
		self.image = pygame.image.load("spaceship_level_1.png")
		self.laser = pygame.image.load("playerlaser_level_1.png")
		self.lasers = []
		self.mask = pygame.mask.from_surface(self.image)
		self.velocity = 10
		self.laser_velocity = -3
		self.reload_time = 10
		self.reload_timer = 0
		self.collide_sound = pygame.mixer.Sound("collide_sound.wav")
		self.level_clear = pygame.mixer.Sound("level_clear.wav")
		self.game_sound = pygame.mixer.Sound("game_sound.wav")
		self.lost_life = pygame.mixer.Sound("lost_life.wav")
		self.damage_sound = pygame.mixer.Sound("player_damage.wav")
		self.die_sound = pygame.mixer.Sound("player_die.wav")
		self.enemy_die = pygame.mixer.Sound("enemy_die.wav")

	def move_lasers(self,objects,SCORE):
		self.reload()
		for laser in self.lasers:
			laser.move()
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			else:
				for object in objects:
					if laser.collision(object):
						objects.remove(object)
						self.enemy_die.play()
						SCORE += 1
						if laser in self.lasers:
							self.lasers.remove(laser)
		return SCORE

	def shoot(self):
		if self.reload_timer == 0:
			laser = Laser(self.x + 27,self.y,self.laser,self.laser_velocity)
			self.laser_sound.play()
			self.lasers.append(laser)
			self.reload_timer = 1

	def healthbar(self):
		pygame.draw.rect(WINDOW,(255,0,0),(self.x,self.y+self.image.get_height(),self.image.get_width(),10))
		pygame.draw.rect(WINDOW,(0,255,0),(self.x,self.y+self.image.get_height(),self.image.get_width()*(self.health/self.max_health),10))

	def draw(self):
		super().draw()
		self.healthbar()

class enemey_ship(ship):
	def __init__(self,x,y,health=100):
		super().__init__()
		self.x = x
		self.y = y
		self.health = health
		if LEVEL == 1:
			image = random.choice(["enemyship_1_level_1.png","enemyship_2_level_1.png","enemyship_3_level_1.png","enemyship_4_level_1.png"])
			self.image = pygame.image.load(image)
			self.laser = pygame.image.load("enemylaser_1_level_2.png")
		elif LEVEL == 2:
			image = random.choice(["enemyship_1_level_2.png","enemyship_2_level_2.png","enemyship_3_level_2.png","enemyship_4_level_2.png","enemyship_5_level_2.png","enemyship_6_level_2.png"])
			self.image = pygame.image.load(image)
			image = random.choice(["enemylaser_1_level_2.png","enemylaser_2_level_2.png","enemylaser_3_level_2.png"])
			self.laser = pygame.image.load(image)
		elif LEVEL == 3:
			image = random.choice(["enemyship_1_level_3.png","enemyship_2_level_3.png","enemyship_3_level_3.png","enemyship_4_level_3.png","enemyship_5_level_3.png","enemyship_6_level_3.png","enemyship_7_level_3.png","enemyship_8_level_3.png"])
			self.image = pygame.image.load(image)
			image = random.choice(["enemylaser_1_level_3.png","enemylaser_2_level_3.png","enemylaser_3_level_3.png","enemylaser_4_level_3.png","enemylaser_5_level_3.png","enemylaser_6_level_3.png"])
			self.laser = pygame.image.load(image)
		elif LEVEL == 4:
			image = random.choice(["enemyship_1_level_4.png","enemyship_2_level_4.png","enemyship_3_level_4.png","enemyship_4_level_4.png","enemyship_5_level_4.png","enemyship_6_level_4.png","enemyship_7_level_4.png","enemyship_8_level_4.png","enemyship_9_level_4.png","enemyship_10_level_4.png"])
			self.image = pygame.image.load(image)
			image = random.choice(["enemylaser_1_level_3.png","enemylaser_2_level_3.png","enemylaser_3_level_3.png","enemylaser_4_level_3.png","enemylaser_5_level_3.png","enemylaser_6_level_3.png","playerlaser_level_3.png","playerlaser_level_3.png","playerlaser_level_3.png","playerlaser_level_3.png","playerlaser_level_3.png","playerlaser_level_3.png"])
			self.laser = pygame.image.load(image)
		self.lasers = []
		self.mask = pygame.mask.from_surface(self.image)
		if LEVEL == 1:
			self.velocity = 1
		elif LEVEL == 2:
			self.velocity = 1
		elif LEVEL == 3:
			self.velocity = 2
		elif LEVEL == 4:
			self.velocity = 3
		self.randomness = 5
		self.randomness_choice = random.choice([1,0])
		self.laser_velocity = 5
		self.reload_time = 10
		self.reload_timer = 0

	def move(self):
		self.y += self.velocity

	def move_random(self):
		self.y +=self.velocity
		if self.randomness_choice:
			self.x += self.randomness
			if self.x < 0:
				self.randomness *= -1
			if self.x > WIDTH-64:
				self.randomness *= -1

	def move_lasers(self,object):
		self.reload()
		for laser in self.lasers:
			laser.move()
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			elif laser.collision(object):
				self.lasers.remove(laser)
				object.health -= object.damage
				object.damage_sound.play()

class Laser:
	def __init__(self,x,y,image,velocity):
		self.x = x
		if LEVEL == 3:
			self.x -= 7
		if LEVEL == 4:
			self.x -= 10
		self.y = y
		self.image = image
		self.velocity = velocity
		self.mask = pygame.mask.from_surface(self.image)

	def draw(self):
		WINDOW.blit(self.image,(self.x,self.y))

	def move(self):
		self.y += self.velocity

	def off_screen(self,HEIGHT):
		return not (self.y <= HEIGHT and self.y >=0)

	def collision(self,object):
		return collide(self,object)


def collide(object_1,object_2):
	offset_x = object_2.x - object_1.x
	offset_y = object_2.y - object_1.y
	return object_1.mask.overlap(object_2.mask,(offset_x,offset_y)) != None


def draw():
	WINDOW.fill((0,0,0))
	for enemy in enemies:
		enemy.draw()
	score_label = FONT.render(f"Score {SCORE}",1,(0,255,0))
	level_label = FONT.render(f"Level  {LEVEL}",1,(255,0,0))
	lifes_label = FONT.render(f"Lifes  {LIFES}",1,(255,0,0))
	WINDOW.blit(score_label,(10, 10))
	WINDOW.blit(level_label,(600 - level_label.get_width() - 10, 10))
	WINDOW.blit(lifes_label,(600 - lifes_label.get_width() - 10, level_label.get_height() + 15))
	if level_change:
		LEVEL_CHANGE_FONT = pygame.font.SysFont("comicsans",100)
		level_change_label = LEVEL_CHANGE_FONT.render(f"LEVEL {LEVEL}",1,(0,255,0))
		WINDOW.blit(level_change_label,(WIDTH/2 - (level_change_label.get_width()/2),(HEIGHT/2) - (level_change_label.get_height())))
	if lost:
		LOST_FONT = pygame.font.SysFont("comicsans",100)
		lost_label = LOST_FONT.render(f"YOU LOST !!!",1,(255,0,0))
		FINAL_SCORE_FONT = pygame.font.SysFont("comicsans",80)
		final_score_label = FINAL_SCORE_FONT.render(f"Score {SCORE}",1,(0,255,0))
		WINDOW.blit(lost_label,((WIDTH/2) - (lost_label.get_width()/2), (HEIGHT/2) - (lost_label.get_height())))
		WINDOW.blit(final_score_label,((WIDTH/2) - (final_score_label.get_width()/2), (HEIGHT/2) + 10))
	if win:
		WIN_FONT = pygame.font.SysFont("comicsans",100)
		win_label = WIN_FONT.render(f"WINNER",1,(0,255,0))
		FINAL_SCORE_FONT = pygame.font.SysFont("comicsans",80)
		final_score_label = FINAL_SCORE_FONT.render(f"Score {SCORE}",1,(0,255,0))
		WINDOW.blit(win_label,((WIDTH/2) - (win_label.get_width()/2), (HEIGHT/2) - (win_label.get_height())))
		WINDOW.blit(final_score_label,((WIDTH/2) - (final_score_label.get_width()/2), (HEIGHT/2) + 10))
	player.draw()
	pygame.display.update()

if __name__ == "__main__":

	player = player_ship()
	enemies = []
	wave_length = 0
	wave_length_frequency = 3
	preload_distance = 0
	level_change = False
	die = False
	lost = False
	win = False
	end_timer = 0

	clock = pygame.time.Clock()
	while(RUN):
		clock.tick(FPS)
		draw()
		if LIFES <=0 or player.health<=0:
			lost = True
			end_timer+=1

		if lost:
			if die == False:
				player.die_sound.play()
				die = True
			if end_timer > FPS*4:
				RUN = False
			else:
				continue

		if win:
			if end_timer > FPS*5:
				RUN = False
				continue
			else:
				end_timer+=1
				continue

		if len(enemies) == 0:
			if wave_length_frequency == 3:
				if level_change == False: 
					LEVEL += 1
					level_change = True
					if LEVEL == 1 or LEVEL == 5:
						player.game_sound.play()
					else:
						player.level_clear.play()

				if LEVEL == 5:
					win = True
					level_change = False
					continue

				if level_change == True:
					if end_timer < FPS*3:
						end_timer += 1
						continue
					else:
						level_change = False
						end_timer= 0 

				if LEVEL == 1:
					player.image = pygame.image.load("spaceship_level_1.png")
					player.laser = pygame.image.load("playerlaser_level_1.png")
					player.laser_sound = pygame.mixer.Sound("lasersound_level_1.wav")
					player.velocity = 2
					player.laser_velocity = -3
					player.reload_time = 50
				elif LEVEL == 2:
					player.image = pygame.image.load("spaceship_level_2.png")
					player.laser = pygame.image.load("playerlaser_level_2.png")
					player.laser_sound = pygame.mixer.Sound("lasersound_level_2.wav")
					player.velocity = 4
					player.laser_velocity = -6
					player.reload_time = 25
				elif LEVEL == 3:
					player.image = pygame.image.load("spaceship_level_3.png")
					player.laser = pygame.image.load("playerlaser_level_3.png")
					player.laser_sound = pygame.mixer.Sound("lasersound_level_3.wav")
					player.velocity = 6
					player.laser_velocity = -8
					player.reload_time = 15
				elif LEVEL == 4:
					player.image = pygame.image.load("spaceship_level_4.png")
					player.laser = pygame.image.load("playerlaser_level_4.png")
					player.laser = pygame.transform.rotate(player.laser, 180)
					player.laser_sound = pygame.mixer.Sound("lasersound_level_4.wav")
					player.velocity = 9
					player.laser_velocity = -9
					player.reload_time = 9
				player.health = player.max_health
				wave_length_frequency = 0

			if LEVEL == 1:
				if wave_length_frequency == 0:
					wave_length = 2
				elif wave_length_frequency == 1:
					wave_length = 4
				else:
					wave_length = 8
			elif LEVEL == 2:
				if wave_length_frequency == 0:
					wave_length = 16
				elif wave_length_frequency == 1:
					wave_length = 32
				else:
					wave_length = 64
			elif LEVEL == 3:
				if wave_length_frequency == 0:
					wave_length = 32
				elif wave_length_frequency == 1:
					wave_length = 32
				else:
					wave_length = 64
			else :
				wave_length = 64
			wave_length_frequency += 1
			preload_distance = wave_length*64
			preload_distance = int(preload_distance)
			for i in range(wave_length):
				enemy = enemey_ship(random.randrange(0,WIDTH-64),random.randrange(-100-preload_distance,-100))
				enemies.append(enemy)
			print(LEVEL)
			print(wave_length," ",wave_length_frequency)
			print(preload_distance)
			print()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				RUN = False

		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] and player.x > 0:
			player.move_left()	
		if keys[pygame.K_RIGHT] and player.x < WIDTH-player.image.get_width():
			player.move_right()
		if keys[pygame.K_SPACE]:
			player.shoot()

		for enemy in enemies[:]:
			if LEVEL == 1 or LEVEL == 2:
				enemy.move()
			if LEVEL == 3 or LEVEL == 4:
				enemy.move_random()
			enemy.move_lasers(player)
			if LEVEL == 1:
				pass
			elif LEVEL == 2:
				if random.randrange(0,4*FPS) == 1:
					enemy.shoot()
			elif LEVEL == 3:
				if random.randrange(0,2*FPS) == 1:
					enemy.shoot()
			elif LEVEL == 4:
				if random.randrange(0,1*FPS) == 1:
					enemy.shoot()
			if collide(enemy,player):
				player.health-=10
				enemies.remove(enemy)
				player.collide_sound.play()
			elif enemy.y + enemy.get_height() > HEIGHT:
				LIFES-=1
				player.lost_life.play()
				enemies.remove(enemy)

		SCORE = player.move_lasers(enemies,SCORE)
