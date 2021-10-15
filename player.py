import pygame
from support import import_folder
from math import sin


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, change_health):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.06
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.attacking = False
        self.attack_frame = 0

        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.10
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 0
        self.gravity = 0.8
        self.jump_speed = -13
        self.collision_rect = pygame.Rect(self.rect.topleft,(25,self.rect.height))

        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        self.change_health = change_health
        self.invicible = False
        self.invicibility_duration = 800
        self.hurt_time = 0

        self.jump_sound = pygame.mixer.Sound('assets/music/jump.wav')
        self.hit_sound = pygame.mixer.Sound('assets/music/hit.wav')

    def import_character_assets(self):
        character_path = 'assets/characters/'
        self.animations = {'idle': [], 'run': [],
                           'jump': [], 'fall': [], 'attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('assets/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invicible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(25, 37)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(25, 37)
                flipped_dust_particle = pygame.transform.flip(
                    dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()

    def get_damage(self):
        if not self.invicible:
            self.hit_sound.play()
            self.change_health(-7.5)
            self.invicible = True
            self.hurt_time = pygame.time.get_ticks()

    def invicibility_timer(self):
        if self.invicible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invicibility_duration:
                self.invicible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.invicibility_timer()
        self.wave_value()
#		self.attack()
