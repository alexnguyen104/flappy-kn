import pygame
import sys
from settings import *
from map import *
from obstacles import Obstacles
from text import *

is_start = False


class BG(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load("assets/sky.jpg").convert()
        scale_factor = screen_h / self.image.get_height()
        self.image = pygame.transform.scale(self.image, (self.image.get_width(
        ) * scale_factor - block_size, self.image.get_height() * scale_factor - block_size))
        self.rect = self.image.get_rect(topleft=(-100, 0))


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        pygame_icon = pygame.image.load(
            'assets/logo.png')

        pygame.display.set_caption("Flappy KN")
        pygame.display.set_icon(pygame_icon)
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        # self.bg = BG(self.all_sprites)
        self.skyline = Skyline(self.all_sprites)
        self.cloud = Cloud(self.all_sprites)
        self.ground = Ground(self.all_sprites)
        self.obstacles = Obstacles(self.all_sprites)

        self.title = Title(self.all_sprites)

    def reset(self):
        background_speed[0] = 3
        self.obstacles.reset()

    def run(self):
        global is_start

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        is_start = True
                        self.obstacles.player.jump()
                    if event.key == pygame.K_v:
                        self.reset()
                        self.__init__()
                        self.run()

            self.screen.fill((221, 198, 161))

            self.all_sprites.draw(self.screen)
            self.ground.render()
            self.obstacles.update(is_start)

            self.title.update(is_start)

            pygame.display.update()
            self.clock.tick(frame_rate)


if __name__ == "__main__":
    game = Game()
    game.run()
