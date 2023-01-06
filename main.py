import pygame
import sys
import time


screen_w = 1080
screen_h = 800
frame_rate = 120
block_size = 64
background_speed = 2
isStart = False


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        x = block_size
        y = screen_h/2 - block_size

        self.image = pygame.image.load(
            "assets/animation/player_1.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 0
        self.gravity = 0.5
        self.jump_speed = 12

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.jump()

    def jump(self):
        self.direction = - self.jump_speed

    def check_collide_ground(self):
        if(self.rect.bottom >= screen_h - block_size):
            self.rect.bottom = screen_h - block_size
            self.direction = 0

    def apply_gravity(self):
        self.direction += self.gravity

    def update(self):
        if(isStart):
            self.apply_gravity()
            # self.get_input()
            self.rect.y += self.direction
            self.check_collide_ground()


class BG(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load("assets/sky.jpg").convert()
        scale_factor = screen_h / self.image.get_height()
        self.image = pygame.transform.scale(self.image, (self.image.get_width(
        ) * scale_factor - block_size, self.image.get_height() * scale_factor - block_size))
        self.rect = self.image.get_rect(topleft=(-100, 0))


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


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption("Flappy KN")
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        # self.bg = BG(self.all_sprites)
        self.skyline = Skyline(self.screen, self.all_sprites)
        self.player = Player(self.all_sprites)
        self.ground = Ground(self.screen, self.all_sprites)

    def run(self):
        global isStart

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        isStart = True
                        self.player.jump()
            self.screen.fill((221, 198, 161))

            self.all_sprites.draw(self.screen)
            self.player.update()
            self.ground.render()

            pygame.display.update()
            self.clock.tick(frame_rate)


if __name__ == "__main__":
    game = Game()
    game.run()
