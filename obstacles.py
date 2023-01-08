import pygame
from settings import *
from random import randrange
from player import Player


class pipe(pygame.sprite.Sprite):
    def __init__(self, group, pos, is_down):
        super().__init__(group)
        self.image = pygame.image.load("assets/obstacle.png").convert_alpha()
        if is_down:
            self.rect = self.image.get_rect(topleft=pos)
        else:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect(bottomleft=pos)
        self.mask = pygame.mask.from_surface(self.image)


class Obstacles():
    def __init__(self, group):
        # init player here => able to access to obstacles
        self.player = Player(group)
        self.player_score = 0

        self.pipe_num = 5

        self.group = group

        self.distance = self.player.rect.w * 2.5
        self.gap_height = self.player.rect.h * 4
        self.obstacles_group = pygame.sprite.Group()

        self.max_y = screen_h / 2
        self.min_y = self.max_y - self.gap_height

        self.last_pipe_x = 0  # used to store last pipes that are off-screen

        self.last_index = -1  # used to store last pipe's index that player passed to count score

        self.init_pipes()

    def init_pipes(self):
        for i in range(self.pipe_num):
            up_pipe_y = randrange(self.min_y, self.max_y, block_size)
            down_pipe_y = up_pipe_y + self.gap_height
            self.obstacles_group.add(
                pipe(self.group, (i * self.distance + screen_w, up_pipe_y), False))
            self.obstacles_group.add(
                pipe(self.group, (i * self.distance + screen_w, down_pipe_y), True))

    def redraw_pipes(self, pipe_up, pipe_down):
        up_pipe_y = randrange(self.min_y, self.max_y, block_size)
        down_pipe_y = up_pipe_y + self.gap_height

        pipe_up.rect.bottomleft = (
            self.last_pipe_x + self.distance, up_pipe_y)

        pipe_down.rect.topleft = (
            self.last_pipe_x + self.distance, down_pipe_y)

    def check_collision(self, obstacle_up, obstacle_down):
        if pygame.sprite.collide_mask(self.player, obstacle_up) or pygame.sprite.collide_mask(self.player, obstacle_down):
            self.player.stop_movement()

    def scoring(self, obstacle_up, obstacle_down, index):
        if self.player.rect.left > obstacle_down.rect.right or self.player.rect.left > obstacle_up.rect.right:
            if (index != self.last_index):
                self.player_score += 1
            self.last_index = index

    def update(self, is_start):
        self.player.update(is_start)
        pipe_sprites = self.obstacles_group.sprites()
        if is_start:
            for i in range(0, len(pipe_sprites) - 1, 2):
                self.check_collision(pipe_sprites[i], pipe_sprites[i+1])
                self.scoring(pipe_sprites[i], pipe_sprites[i+1], i)
                print(self.player_score)
                if pipe_sprites[i+1].rect.right <= 0:
                    self.redraw_pipes(pipe_sprites[i], pipe_sprites[i+1])

                pipe_sprites[i].rect.x -= background_speed[0]
                pipe_sprites[i+1].rect.x -= background_speed[0]

                self.last_pipe_x = pipe_sprites[i+1].rect.x
