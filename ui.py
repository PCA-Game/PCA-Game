import pygame


class UI:
    def __init__(self, surface):
        self.display_surface = surface

        self.health_bar = pygame.image.load(
            'assets/levels/ui/health_heart.png').convert_alpha()
        self.health_bar_topleft = (84, 32)
        self.bar_max_width = 22
        self.bar_height = 4
        self.font = pygame.font.Font('assets/levels/ui/ARCADEPI.TTF', 25)

    def show_health(self, current, full):
        self.display_surface.blit(self.health_bar, (50, 3))
        current_health_ratio = current / full
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(
            (self.health_bar_topleft), (current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)
