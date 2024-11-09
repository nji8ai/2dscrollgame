import pygame
from pygame.locals import *

clock = pygame.time.Clock()
FPS = 30
pygame.init()
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('2DSCROLLGAME')



#定数
tile_size = screen_width/20
WHITE = (255, 255, 255)
SKY = (144, 215, 236)
YELLOW = (255, 255, 0)
game_over = 0


def draw_grid():

	for line in range(0, 20):
		pygame.draw.line(screen, WHITE, (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, WHITE, (line * tile_size, 0), (line * tile_size, screen_height))

class World():

	def __init__(self, data):
			self.tile_list = []

			#load images
			dirt_img = pygame.image.load('dirt.png')
			grass_img = pygame.image.load('grass.png')
			row_count = 0
			for row in data:
					col_count = 0
					for tile in row:
						if tile == 1:
								img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
								img_rect = img.get_rect()
								img_rect.x = col_count * tile_size
								img_rect.y = row_count * tile_size
								tile = (img, img_rect)
								self.tile_list.append(tile)

						if tile == 2:
								img = pygame.transform.scale(grass_img, (tile_size, tile_size))
								img_rect = img.get_rect()
								img_rect.x = col_count * tile_size
								img_rect.y = row_count * tile_size
								tile = (img, img_rect)
								self.tile_list.append(tile)

						if tile == 3:
								enemy = Enemy(col_count * tile_size, row_count * tile_size + 5)
								enemy_group.add(enemy)
						if tile == 6:
								magma = Magma(col_count * tile_size, row_count * tile_size )
								magma_group.add(magma)
						col_count += 1

					row_count += 1



	def draw(self):

		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
			pygame.draw.rect(screen, WHITE, tile[1], 1)

#プレイヤーの描写

class Player():

	def __init__(self, x, y):

			player_img = pygame.image.load('man_suit.png')
			dead_img = pygame.image.load('dead.png')
			self.image = pygame.transform.scale(player_img, (24, 48))
			self.dead_image = pygame.transform.scale(dead_img, (tile_size, tile_size))
			self.rect = self.image.get_rect()
			self.rect.x = x
			self.rect.y = y
			self.width = self.image.get_width()
			self.height = self.image.get_height()
			self.vel_x = 0
			self.vel_y = 0
			self.gravity = 1
			self.on_Ground = True

	def update(self, game_over):
			dx = 0
			dy = 0
			for tile in world.tile_list:
				if tile[1].colliderect(self.rect.x , self.rect.y, self.width, self.height):
						if tile[1].top == self.rect.bottom:
								self.on_Ground == True
        
			if game_over == 0:
				#get keypresses
				key = pygame.key.get_pressed()
				if key[pygame.K_SPACE] and self.on_Ground == True:
					self.vel_y = -15
					self.on_Ground = False
				# if key[pygame.K_SPACE] == False:
				# 	self.jumped = False
				if key[pygame.K_LEFT]:
					dx -= 5
					self.counter += 1
				if key[pygame.K_RIGHT]:
					dx += 5
					self.counter += 1
				if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
					self.counter = 0
					self.index = 0

				#重力
				self.vel_y += self.gravity
				if self.vel_y > 10:
					self.vel_y = 10
				dy += self.vel_y

				#衝突判定
				for tile in world.tile_list:
					#check for collision in x direction
					if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
						dx = 0
					#check for collision in y direction
					if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
						#check if below the ground i.e. jumping
						if self.vel_y < 0:
							dy = tile[1].bottom - self.rect.top
							self.vel_y = 0
						#check if above the ground i.e. falling
						elif self.vel_y >= 0:
							dy = tile[1].top - self.rect.bottom
							self.vel_y = 0
							self.on_Ground = True
       
			elif game_over == -1:
					self.image = self.dead_image
					screen.blit(self.image, self.rect)
					pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

			#敵との衝突判定
			if pygame.sprite.spritecollide(self, enemy_group, False):
					game_over = -1

			#マグマとの衝突判定
			if pygame.sprite.spritecollide(self, magma_group, False):
					game_over = -1
					print(game_over)

			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy

			if self.rect.bottom > screen_height:
				self.rect.bottom = screen_height
				dy = 0

			#draw player onto screen
			screen.blit(self.image, self.rect)
			pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

			return game_over

class Enemy(pygame.sprite.Sprite):
		def __init__(self, x, y):
				pygame.sprite.Sprite.__init__(self)
				enemy_image = pygame.image.load('enemy.png')
				self.image = pygame.transform.scale(enemy_image, (tile_size, tile_size))
				self.rect = self.image.get_rect()
				self.rect.x = x
				self.rect.y = y
				self.move_direction = 1
				self.move_counter = 0
				screen.blit(self.image, self.rect)

		def update(self):
				# 移動距離をカウント
				self.rect.x += self.move_direction
				self.move_counter += 1

        # 移動距離が一定値を超えたら向きを変える (前の処理との重複回避)
				if abs(self.move_counter) > 50:
						self.move_direction *= -1
						self.move_counter *= -1

        # 描画
				screen.blit(self.image, self.rect)

class Magma(pygame.sprite.Sprite):
		def __init__(self, x, y):
				pygame.sprite.Sprite.__init__(self)
				magma_image = pygame.image.load('magma.png')
				self.image = pygame.transform.scale(magma_image, (tile_size, tile_size))
				self.rect = self.image.get_rect()
				self.rect.x = x
				self.rect.y = y
				screen.blit(self.image, self.rect)

world_data = [

[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 2, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]




player = Player(60, screen_height-78)
enemy_group = pygame.sprite.Group()
magma_group = pygame.sprite.Group()
world = World(world_data)
run = True
while run:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
						run = False
						break
				if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
								run = False
								break
      
		screen.fill(SKY)
		pygame.draw.circle(screen, YELLOW, (50,50) ,30, 30)
		world.draw()
  
  
		enemy_group.update()
		enemy_group.draw(screen)
		magma_group.draw(screen)
		dt = clock.tick(FPS) / 1000
		game_over = player.update(game_over)
		draw_grid()
		pygame.display.update()
pygame.quit()