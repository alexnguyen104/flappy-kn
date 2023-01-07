import pygame
from settings import *
from random import randrange


class Tube(pygame.sprite.Sprite):
    def __init__(self, group, pos, is_down):
        super().__init__(group)
        self.image = pygame.surface.Surface((64, 1000))
        if is_down:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect(topleft=pos)
        else:
            self.rect = self.image.get_rect(bottomleft=pos)


class Obstacles():
    def __init__(self, player_height, player_width, group):
        self.distance = player_width * 2.5
        tube_num = 5
        self.gap_height = player_height * 3.5
        self.obstacles_group = pygame.sprite.Group()

        self.max_y = screen_h / 2
        self.min_y = self.max_y - self.gap_height

        self.last_tube_x = 0 # used to store last tubes that are off-screen

        for i in range(tube_num):
            up_tube_y = randrange(self.min_y, self.max_y, block_size)
            down_tube_y = up_tube_y + self.gap_height
            self.obstacles_group.add(
                Tube(group, (i * self.distance + screen_w, up_tube_y), False))
            self.obstacles_group.add(
                Tube(group, (i * self.distance + screen_w, down_tube_y), True))

    def redraw_tubes(self, tube_up, tube_down):
        up_tube_y = randrange(self.min_y, self.max_y, block_size)
        down_tube_y = up_tube_y + self.gap_height
        # if index % 2:  # if the index % 2 == 1 (odd number) => down_tube
        tube_up.rect.topleft = (self.last_tube_x, down_tube_y)
        
        tube_down.rect.bottomleft = (self.last_tube_x + self.distance, up_tube_y)

            

    def update(self, is_start):
        tube_sprites = self.obstacles_group.sprites()
        if is_start:
            # if tube_sprites[0].rect.right <= 0:
            #     for tube in tube_sprites:
            #         tube.rect.x =
            # for i, tube in enumerate(tube_sprites):
            #     if tube.rect.right <= 0:
            #         self.redraw_tubes(tube, i)
            #     tube.rect.x -= background_speed
            #     self.last_tube_x = tube.rect.x
            for i in range(0, len(tube_sprites) - 1, 2 ):
                if tube_sprites[i+1].rect.right <= 0:
                    self.redraw_tubes(tube_sprites[i], tube_sprites[i+1])
                tube_sprites[i].rect.x -= background_speed
                tube_sprites[i+1].rect.x -= background_speed
                self.last_tube_x = tube_sprites[i+1].rect.x

            # self.tube = Tube(self.group, (0, 0), False)
