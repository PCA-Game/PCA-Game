import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite):
	def __init__(self,size,x,y):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.rect = self.image.get_rect(topleft = (x,y))	

	def update(self, shift):
		self.rect.x += shift

class StaticTile(Tile):
	def __init__(self, size, x, y, surface):
		super().__init__(size,x,y)
		self.image = surface	

class AnimatedTile(Tile):
	def __init__(self, size, x, y, path):
		super().__init__(size, x, y)
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

	def animate(self):
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self, shift):
		self.animate()
		self.rect.x += shift

class AnimatedTileLava(Tile):
	def __init__(self, size, x, y, path):
		super().__init__(size, x, y)
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

	def animate(self):
		self.frame_index += 0.08
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self, shift):
		self.animate()
		self.rect.x += shift		

class Flag(AnimatedTile):
	def __init__(self, size, x, y, path, offset):
		super().__init__(size, x, y, path)
		offset_y = y - offset
		self.rect.topleft = (x, offset_y)		

	def animate(self):
		self.frame_index += 0.1
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

class Trees(AnimatedTile):

	def __init__(self, size, x, y, path, offset):
		super().__init__(size, x, y, path)
		offset_y = y - offset
		self.rect.topleft = (x, offset_y)