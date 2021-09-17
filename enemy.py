import pygame
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
	def __init__(self, size, x, y):
		super().__init__(size, x, y, 'assets/levels/enemies/beholder/run')
		self.rect.y += size - self.image.get_size()[1]
		self.speed = randint(2,3)

	def move(self):
		self.rect.x += self.speed

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image, True, False)

	def reverse(self):
		self.speed *= -1			

	def update(self, shift):
		self.rect.x += shift
		self.animate()
		self.move()	
		self.reverse_image()

class Enemy1(AnimatedTile):
	def __init__(self, size, x, y):
		super().__init__(size, x, y, 'assets/levels/enemies/hellbound/run')
		self.rect.y += size - self.image.get_size()[1]
		self.speed = randint(3,3)

	def move(self):
		self.rect.x += self.speed

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image, True, False)

	def reverse(self):
		self.speed *= -1			

	def update(self, shift):
		self.rect.x += shift
		self.animate()
		self.move()	
		self.reverse_image()

class Enemy2(AnimatedTile):
	def __init__(self, size, x, y):
		super().__init__(size, x, y, 'assets/levels/enemies/husky/run')
		self.rect.y += size - self.image.get_size()[1]
		self.speed = randint(1,1)

	def move(self):
		self.rect.x += self.speed

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image, True, False)

	def reverse(self):
		self.speed *= -1			

	def update(self, shift):
		self.rect.x += shift
		self.animate()

class Enemy3(AnimatedTile):
	def __init__(self, size, x, y):
		super().__init__(size, x, y, 'assets/levels/enemies/dark_goblin/run')
		self.rect.y += size - self.image.get_size()[1]
		self.speed = randint(2,3)

	def move(self):
		self.rect.x += self.speed

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image, True, False)

	def reverse(self):
		self.speed *= -1			

	def update(self, shift):
		self.rect.x += shift
		self.animate()
		self.move()	
		self.reverse_image()


class Enemy4(AnimatedTile):
	def __init__(self, size, x, y):
		super().__init__(size, x, y, 'assets/levels/enemies/mage/run')
		self.rect.y += size - self.image.get_size()[1]
		self.speed = randint(1,5)

	def move(self):
		self.rect.x += self.speed

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image, True, False)

	def reverse(self):
		self.speed *= -1			

	def update(self, shift):
		self.rect.x += shift
		self.animate()
		self.move()	
		self.reverse_image()	