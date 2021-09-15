import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, AnimatedTile, Flag, Trees
from enemy import Enemy, Enemy1, Enemy2, Enemy3
from decorations import Lava
from player import Player
from particles import ParticleEffect, Death, Death2
from game_data import levels

class Level:
	def __init__(self, current_level, surface, create_overworld, change_coins, change_health):
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None

		self.create_overworld = create_overworld
		self.current_level = current_level
		level_data = levels[self.current_level]
		self.new_max_level = level_data['unlock']

		player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_layout, change_health)

		self.change_coins = change_coins

		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

		self.death_sprites = pygame.sprite.Group()

		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

		trees_layout = import_csv_layout(level_data['trees'])
		self.trees_sprites = self.create_tile_group(trees_layout, 'trees')
		trees1_layout = import_csv_layout(level_data['trees1'])
		self.trees1_sprites = self.create_tile_group(trees1_layout, 'trees1')
		trees2_layout = import_csv_layout(level_data['trees2'])
		self.trees2_sprites = self.create_tile_group(trees2_layout, 'trees2')
		trees3_layout = import_csv_layout(level_data['trees3'])
		self.trees3_sprites = self.create_tile_group(trees3_layout, 'trees3')

		grass_layout = import_csv_layout(level_data['grass'])
		self.grass_sprites = self.create_tile_group(grass_layout, 'grass')
		grass1_layout = import_csv_layout(level_data['grass1'])
		self.grass1_sprites = self.create_tile_group(grass1_layout, 'grass1')

		coin_layout = import_csv_layout(level_data['coins'])
		self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

		fg_flag_layout = import_csv_layout(level_data['flag'])
		self.fg_flag_sprites = self.create_tile_group(fg_flag_layout, 'flag')

		enemy_layout = import_csv_layout(level_data['enemies'])
		self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')
		enemy1_layout = import_csv_layout(level_data['enemies1'])
		self.enemy1_sprites = self.create_tile_group(enemy1_layout, 'enemies1')
		enemy2_layout = import_csv_layout(level_data['enemies2'])
		self.enemy2_sprites = self.create_tile_group(enemy2_layout, 'enemies2')
		enemy3_layout = import_csv_layout(level_data['enemies3'])
		self.enemy3_sprites = self.create_tile_group(enemy3_layout, 'enemies3')		

		crate_layout = import_csv_layout(level_data['crates'])
		self.crate_sprites = self.create_tile_group(crate_layout,'crates')

		constraint_layout = import_csv_layout(level_data['constraints'])
		self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')

		level_width = len(terrain_layout[0]) * tile_size
		self.lava = Lava(screen_height - 70, level_width)

	def create_tile_group(self,layout,type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('assets/levels/graphics/terrain/terrain_tiles.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)	

					if type == 'grass':
						grass_tile_list = import_cut_graphics('assets/levels/graphics/decoration/grass/1.png')
						tile_surface = grass_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)
					if type == 'grass1':
						grass1_tile_list = import_cut_graphics('assets/levels/graphics/decoration/grass/4.png')
						tile_surface = grass1_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)

					if type == 'crates':
						sprite = Crate(tile_size,x,y)

					if type == 'coins':
						sprite = AnimatedTile(tile_size, x, y, 'assets/levels/graphics/coins')

					if type == 'flag':
						sprite = Flag(tile_size, x, y, 'assets/levels/graphics/terrain/flag', 32)

					if type == 'trees':
						sprite = Trees(tile_size, x, y, 'assets/levels/graphics/terrain/trees', 32)
					if type == 'trees1':
						sprite = Trees(tile_size, x, y, 'assets/levels/graphics/terrain/trees1', 32)
					if type == 'trees2':
						sprite = Trees(tile_size, x, y, 'assets/levels/graphics/terrain/trees2', 32)
					if type == 'trees3':
						sprite = Trees(tile_size, x, y, 'assets/levels/graphics/terrain/trees3', 32)																						

					if type == 'enemies':
						sprite = Enemy(tile_size, x, y)
					if type == 'enemies1':
						sprite = Enemy1(tile_size, x, y)
					if type == 'enemies2':
						sprite = Enemy2(tile_size, x, y)
					if type == 'enemies3':
						sprite = Enemy3(tile_size, x, y)

					if type == 'constraints':
						sprite = Tile(tile_size, x, y)					

					sprite_group.add(sprite)

		return sprite_group 

	def create_jump_particles(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(1,18)
		else:
			pos += pygame.math.Vector2(1,-18)
		jump_particle_sprite = ParticleEffect(pos,'jump')
		self.dust_sprite.add(jump_particle_sprite)		

	def player_setup(self, layout, change_health):
		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val == '0':
					sprite = Player((x,y), self.display_surface, self.create_jump_particles, change_health)
					self.player.add(sprite)
				if val == '1':
					skull_surface = pygame.image.load('assets/characters/skull.png').convert_alpha()
					sprite = StaticTile(tile_size, x, y, skull_surface)
					self.goal.add(sprite)					

	def enemy_collision_reverse(self):
		for enemy in self.enemy_sprites.sprites():
			if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
				enemy.reverse()

	def enemy_collision_reverse1(self):
		for enemy in self.enemy1_sprites.sprites():
			if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
				enemy.reverse()

	def enemy_collision_reverse2(self):
		for enemy in self.enemy2_sprites.sprites():
			if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
				enemy.reverse()

	def enemy_collision_reverse3(self):
		for enemy in self.enemy3_sprites.sprites():
			if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
				enemy.reverse()												

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.terrain_sprites.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for sprite in self.terrain_sprites.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0: 
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False				

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 5
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -5
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 5			

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
		 	self.player_on_ground = False

	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(0,20)
			else:
				offset = pygame.math.Vector2(-0,20)

			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
			self.dust_sprite.add(fall_dust_particle)			

	def check_death(self):
		if self.player.sprite.rect.top > screen_height:
			self.create_overworld(self.current_level, 0)
			
	def check_win(self):
		if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
			self.create_overworld(self.current_level, self.new_max_level)			

	def check_coin_collisions(self):
		collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
		if collided_coins:
			for coin in collided_coins:
				self.change_coins(1)

	def check_enemy_collisions(self):
		enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

		if enemy_collisions:
			for enemy in enemy_collisions:
				enemy_center = enemy.rect.centery
				enemy_top = enemy.rect.top
				player_bottom = self.player.sprite.rect.bottom
				if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
					self.player.sprite.direction.y = -15
					death_sprite = Death2(enemy.rect.midbottom, 'death1')
					self.death_sprites.add(death_sprite)					
					enemy.kill()
				else:
					self.player.sprite.get_damage()

	def check_enemy1_collisions(self):
		enemy1_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy1_sprites, False)

		if enemy1_collisions:
			for enemy1 in enemy1_collisions:
				enemy1_center = enemy1.rect.centery
				enemy1_top = enemy1.rect.top
				player_bottom = self.player.sprite.rect.bottom
				if enemy1_top < player_bottom < enemy1_center and self.player.sprite.direction.y >= 0:
					self.player.sprite.direction.y = -15
					death_sprite = Death2(enemy1.rect.midbottom, 'death2')
					self.death_sprites.add(death_sprite)
					enemy1.kill()
				else:
					self.player.sprite.get_damage()

	def check_enemy2_collisions(self):
		enemy2_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy2_sprites, False)

		if enemy2_collisions:
			for enemy2 in enemy2_collisions:
				enemy2_center = enemy2.rect.centery
				enemy2_top = enemy2.rect.top
				player_bottom = self.player.sprite.rect.bottom
				if enemy2_top < player_bottom < enemy2_center and self.player.sprite.direction.y >= 0:
					self.player.sprite.direction.y = -15
					death_sprite = Death(enemy2.rect.midbottom, 'death3')
					self.death_sprites.add(death_sprite)
					enemy2.kill()
				else:
					self.player.sprite.get_damage()

	def check_enemy3_collisions(self):
		enemy3_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy3_sprites, False)

		if enemy3_collisions:
			for enemy3 in enemy3_collisions:
				enemy3_center = enemy3.rect.centery
				enemy3_top = enemy3.rect.top
				player_bottom = self.player.sprite.rect.bottom
				if enemy3_top < player_bottom < enemy3_center and self.player.sprite.direction.y >= 0:
					self.player.sprite.direction.y = -15
					death_sprite = Death2(enemy3.rect.midbottom, 'death4')
					self.death_sprites.add(death_sprite)
					enemy3.kill()
				else:
					self.player.sprite.get_damage()

	def run(self):
		self.crate_sprites.update(self.world_shift)
		self.crate_sprites.draw(self.display_surface)
		
		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.display_surface)

		self.trees_sprites.update(self.world_shift)
		self.trees_sprites.draw(self.display_surface)
		self.trees1_sprites.update(self.world_shift)
		self.trees1_sprites.draw(self.display_surface)
		self.trees2_sprites.update(self.world_shift)
		self.trees2_sprites.draw(self.display_surface)
		self.trees3_sprites.update(self.world_shift)
		self.trees3_sprites.draw(self.display_surface)

		self.grass_sprites.update(self.world_shift)
		self.grass_sprites.draw(self.display_surface)
		self.grass1_sprites.update(self.world_shift)
		self.grass1_sprites.draw(self.display_surface)

		self.coin_sprites.update(self.world_shift)
		self.coin_sprites.draw(self.display_surface)

		self.fg_flag_sprites.update(self.world_shift)
		self.fg_flag_sprites.draw(self.display_surface)

		self.enemy_sprites.update(self.world_shift)
		self.enemy_sprites.draw(self.display_surface)
		self.enemy1_sprites.update(self.world_shift)
		self.enemy1_sprites.draw(self.display_surface)
		self.enemy2_sprites.update(self.world_shift)
		self.enemy2_sprites.draw(self.display_surface)
		self.enemy3_sprites.update(self.world_shift)
		self.enemy3_sprites.draw(self.display_surface)

		self.constraint_sprites.update(self.world_shift)
		self.enemy_collision_reverse()
		self.enemy_collision_reverse1()
		self.enemy_collision_reverse2()
		self.enemy_collision_reverse3()
		self.death_sprites.update(self.world_shift)
		self.death_sprites.draw(self.display_surface)

		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.display_surface)

		self.player.update()
		self.horizontal_movement_collision()

		self.get_player_on_ground()
		self.vertical_movement_collision()
		self.create_landing_dust()

		self.scroll_x()
		self.player.draw(self.display_surface)
		self.goal.update(self.world_shift)
		self.goal.draw(self.display_surface)

		self.check_death()
		self.check_win()

		self.check_coin_collisions()
		self.check_enemy_collisions()
		self.check_enemy1_collisions()
		self.check_enemy2_collisions()
		self.check_enemy3_collisions()

		self.lava.draw(self.display_surface, self.world_shift)

