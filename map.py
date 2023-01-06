import pygame
from settings import *


class Skyline():
    def __init__(self, screen, block_group):
        self.group = pygame.sprite.Group()

        for i in range(round(screen_w / block_size)):
            self.group.add(
                Block(block_group, (i * block_size, screen_h - block_size * 2), "assets/sky_middle.png"))

        self.group.draw(screen)


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, file_path):
        super().__init__(group)
        self.image = pygame.image.load(file_path).convert()
        self.image = pygame.transform.scale(
            self.image, (block_size, block_size))
        self.rect = self.image.get_rect(topleft=pos)


class Ground():
    def __init__(self, screen, block_group):
        super().__init__()
        self.group = pygame.sprite.Group()
        self.screen = screen

        # create an extra ground to make the animation
        for i in range(round(screen_w / block_size) * 2):
            self.group.add(
                Block(block_group, (i * block_size, screen_h - block_size), "assets/terrain_tiles.png"))

    def render(self):
        # reset pos if first floor nearly reach its ending ([-2] position of the first floor)
        self.group.draw(self.screen)
        ground_sprites = self.group.sprites()
        if(ground_sprites[int(len(ground_sprites) / 2) - 1].rect.right <= 0):
            for i, block in enumerate(self.group.sprites()):
                block.rect.x = i * block_size
        else:
            for block in self.group.sprites():
                block.rect.x -= background_speed
