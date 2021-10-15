import pygame
import sys
import random
from settings import *
from level import Level
from overworld import Overworld
from ui import UI


class Game:
    def __init__(self):
        self.max_level = 5
        self.max_health = 22
        self.cur_health = 22

        self.overworld = Overworld(
            0, self.max_level, screen, self.create_level)
        self.status = 'overworld'

        self.ui = UI(screen)

    def create_level(self, current_level):
        self.level = Level(current_level, screen,
                           self.create_overworld, self.change_health)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(
            current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def change_health(self, amount):
        self.cur_health += amount

    def check_game_over(self):
        if self.cur_health <= 0:
            self.cur_health = 22
            self.max_level = 0
            self.overworld = Overworld(
                0, self.max_level, screen, self.create_level)
            self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health, self.max_health)
            self.check_game_over()


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()
fps = 60


def load_snd(name):
    return pygame.mixer.Sound('assets/music/' + name + '.mp3')


pygame.mixer.music.load('assets/music/main.mp3')

pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.45)

background = pygame.image.load(
    'assets/levels/graphics/decoration/sky/Background.png')

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    game.run()

    pygame.display.update()
    clock.tick(60)
