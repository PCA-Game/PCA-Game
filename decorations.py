import pygame
from settings import *
from tiles import AnimatedTileLava

class Lava:
	def __init__(self, top, level_width):
		lava_start = -screen_width
		lava_tile_width = 400
		tile_x_amount = int((level_width + screen_width * 2) / lava_tile_width)
		self.lava_sprites = pygame.sprite.Group()

		for tile in range(tile_x_amount):
			x = tile * lava_tile_width + lava_start
			y = top
			sprite = AnimatedTileLava(400, x, y, 'assets/levels/graphics/decoration/lava')
			self.lava_sprites.add(sprite)

	def draw(self, surface, shift):
		self.lava_sprites.update(shift)
		self.lava_sprites.draw(surface)		

