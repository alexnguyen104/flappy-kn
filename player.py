import pygame
from settings import *
from sound import play_sound
from time import sleep


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.x = block_size
        self.y = screen_h/2 - block_size

        self.current_animation = 0
        self.animation_steps = 3
        self.animation_list = [
            "assets/animation/player_" + str(i + 1) + ".png" for i in range(self.animation_steps)]
        self.animation_speed = 0.1
        self.animation_is_stop = False

        self.image = pygame.image.load(
            self.animation_list[0]).convert_alpha()
        self.image_copy = self.image  # used for rotating player

        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.gravity = 0.05
        self.jump_speed = -9
        self.fall_speed = 0

        self.mask = pygame.mask.from_surface(self.image)

        self.allow_jump = True
        self.allow_rotate = True

        self.is_game_over = False

        self.first_loop_when_game_over = 0

    def animation(self):
        if not self.animation_is_stop:
            self.current_animation += self.animation_speed

            if self.current_animation >= self.animation_steps:
                self.current_animation = 0

            self.image = pygame.image.load(self.animation_list[int(
                self.current_animation)]).convert_alpha()

            self.image_copy = self.image  # used for rotating player

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.jump()

    def jump(self):
        if self.allow_jump:
            self.fall_speed = 0
            self.y = self.jump_speed
            play_sound("assets/sound/jump_sound.wav")

    def rotate(self):
        if self.allow_rotate:
            # need a copy version of the orignal image which is not rotating => not keep rotating
            self.image = pygame.transform.rotate(self.image_copy, -self.y)
            self.mask = pygame.mask.from_surface(self.image)

    def check_collide_ground(self):
        if(self.rect.bottom >= screen_h - block_size):
            self.rect.bottom = screen_h - block_size
            self.stop_movement()

    def apply_gravity(self):
        self.y += 0.5*self.gravity + self.fall_speed
        self.fall_speed += self.gravity

    def stop_movement(self):
        global background_speed
        self.animation_is_stop = True
        self.allow_jump = False
        self.allow_rotate = False
        self.y = 0
        self.fall_speed = 0
        self.is_game_over = True
        self.first_loop_when_game_over += 1
        if self.first_loop_when_game_over == 1:
            play_sound("assets/sound/hit_sound.wav")
            play_sound("assets/sound/game_over.wav")
        background_speed[0] = 0

    def update(self, is_start):
        self.animation()
        if(is_start):
            self.rotate()
            self.apply_gravity()
            self.rect.y += self.y
            self.check_collide_ground()

            if self.rect.bottom < 0:  # check if player fly to high
                self.allow_jump = False
            elif not self.is_game_over:
                self.allow_jump = True
