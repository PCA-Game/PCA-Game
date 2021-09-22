import pygame

class UI:
	def __init__(self, surface):
		self.display_surface = surface

		self.health_bar = pygame.image.load('assets/levels/ui/health_heart.png').convert_alpha()
		self.health_bar_topleft = (84, 32)
		self.bar_max_width = 22
		self.bar_height = 4

		self.coin = pygame.image.load('assets/levels/ui/coin.png').convert_alpha()
		self.coin_rect = self.coin.get_rect(topleft = (130, 20))
		self.font = pygame.font.Font('assets/levels/ui/ARCADEPI.TTF', 25)

	def show_health(self, current, full):
		self.display_surface.blit(self.health_bar,(50, 3))
		current_health_ratio = current / full
		current_bar_width = self.bar_max_width * current_health_ratio
		health_bar_rect = pygame.Rect((self.health_bar_topleft), (current_bar_width, self.bar_height))
		pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)

	def show_coins(self, amount):
		self.display_surface.blit(self.coin, self.coin_rect)
		coin_amount_surf = self.font.render(str(amount), False, 'white')
		coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4, self.coin_rect.centery))
		self.display_surface.blit(coin_amount_surf, coin_amount_rect)