import pygame
from settings import *


class Cloud():
    def __init__(self, screen, block_group):
        self.group = pygame.sprite.Group()
        cloud_dict = {
            0: {
                "file_path": "assets/cloud1.png",
                "pos": [(screen_w / 2, screen_h / 4), (screen_w - 300, screen_h / 2)],
                "num": 2
            },
            1: {
                "file_path": "assets/cloud2.png",
                "pos": [(0, screen_h / 8)],
                "num": 1
            },
            2: {
                "file_path": "assets/cloud3.png",
                "pos": [(screen_w - 450, 10), (200, screen_h / 2)],
                "num": 2
            }
        }
        for i in range(len(cloud_dict)):
            for j in range(cloud_dict[i]["num"]):
                self.group.add(Block(
                    block_group, cloud_dict[i]["pos"][j], cloud_dict[i]["file_path"], True, False))

        self.group.draw(screen)


class Skyline():
    def __init__(self, screen, block_group):
        self.group = pygame.sprite.Group()

        for i in range(round(screen_w / block_size)):
            self.group.add(Block(block_group, (i * block_size,
                           screen_h - block_size * 3), "assets/sky_middle.png", False, True))

        for i in range(round(screen_w / block_size)):
            self.group.add(
                Block(block_group, (i * block_size, screen_h - block_size * 2), "assets/sky_bottom.png", False, True))

        self.group.draw(screen)


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, file_path, is_transparent, is_square):
        super().__init__(group)
        if is_transparent:
            self.image = pygame.image.load(file_path).convert_alpha()
        else:
            self.image = pygame.image.load(file_path).convert()

        if is_square:
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
                Block(block_group, (i * block_size, screen_h - block_size), "assets/terrain_tiles.png", False, True))

    def render(self):
        # reset pos if first floor nearly reach its ending ([-2] position of the first floor)
        self.group.draw(self.screen)
        ground_sprites = self.group.sprites()
        if(ground_sprites[int(len(ground_sprites) / 2) - 1].rect.right <= 0):
            for i, block in enumerate(self.group.sprites()):
                block.rect.x = i * block_size
        else:
            for block in self.group.sprites():
                block.rect.x -= background_speed[0]
