import pygame
from settings import *


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
        self.gravity = 0.1
        self.fall_speed = 0
        self.jump_speed = -15

    def animation(self):
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
        self.fall_speed = 0
        self.y = self.jump_speed

    def rotate(self):
        # need a copy version of the orignal image which is not rotating => not keep rotating
        self.image = pygame.transform.rotate(self.image_copy, -self.y)

    def check_collide_ground(self):
        if(self.rect.bottom >= screen_h - block_size):
            self.rect.bottom = screen_h - block_size
            self.y = 0
            self.fall_speed = 0

    def apply_gravity(self):
        self.y += 0.5*self.gravity + self.fall_speed
        self.fall_speed += self.gravity

    # def stop_movement(self):
    #     self.animation_is_stop = True

    def update(self, is_start):
        self.animation()

        if(is_start):
            self.rotate()
            self.apply_gravity()
            self.rect.y += self.y
            self.check_collide_ground()
