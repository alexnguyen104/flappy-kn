import pygame
import sys
from settings import *
from map import *
from obstacles import Obstacles
from text_related import *


is_start = False


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
        global is_start
        background_speed[0] = 3
        is_start = False

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
                    if event.key == pygame.K_RETURN and self.obstacles.player.is_game_over:
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
