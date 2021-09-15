import pygame
from support import import_folder

class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self,pos,type):
		super().__init__()
		self.frame_index = 0
		self.animation_speed = 0.5
		if type == 'jump':
			self.frames = import_folder('assets/dust_particles/jump')
		if type == 'land':
			self.frames = import_folder('assets/dust_particles/land')

		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]
	
	def update(self,x_shift):
		self.animate()
		self.rect.x += x_shift

class Death(pygame.sprite.Sprite):
	def __init__(self,pos,type):
		super().__init__()
		self.frame_index = 1
		self.animation_speed = 0.05
		if type == 'death1':
			self.frames = import_folder('assets/levels/enemies/beholder/death')
		if type == 'death2':
			self.frames = import_folder('assets/levels/enemies/hellbound/death')		
		if type == 'death3':
			self.frames = import_folder('assets/levels/enemies/husky/death')
		if type == 'death4':
			self.frames = import_folder('assets/levels/enemies/dark_goblin/death')		
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]
	
	def update(self,x_shift):
		self.animate()
		self.rect.x += x_shift

class Death2(pygame.sprite.Sprite):
	def __init__(self,pos,type):
		super().__init__()
		self.frame_index = 1
		self.animation_speed = 0.1
		if type == 'death1':
			self.frames = import_folder('assets/levels/enemies/beholder/death')
		if type == 'death2':
			self.frames = import_folder('assets/levels/enemies/hellbound/death')		
		if type == 'death3':
			self.frames = import_folder('assets/levels/enemies/husky/death')
		if type == 'death4':
			self.frames = import_folder('assets/levels/enemies/dark_goblin/death')		
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animate(self):
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]
	
	def update(self,x_shift):
		self.animate()
		self.rect.x += x_shift
