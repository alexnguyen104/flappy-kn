import pygame
import sys
import time


screen_w = 1080
screen_h = 800
frame_rate = 60
block_size = 64
speed = 5


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        x = block_size
        y = screen_h/2 - block_size

        self.image = pygame.image.load(
            "assets/animation/player_1.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = 0
        self.gravity = 98
        self.jump_speed = 900

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

    def update(self, dt):
        self.apply_gravity()
        self.get_input()
        self.rect.y += self.direction * dt
        self.check_collide_ground()


class BG(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load("assets/bg2.png").convert()
        scale_factor = screen_h / self.image.get_height()
        self.image = pygame.transform.scale(self.image, (self.image.get_width(
        ) * scale_factor - block_size, self.image.get_height() * scale_factor - block_size))
        self.rect = self.image.get_rect(topleft=(-100, 0))


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.image = pygame.image.load("assets/ground.jpg").convert()
        self.image = pygame.transform.scale(
            self.image, (block_size, block_size))
        self.rect = self.image.get_rect(topleft=pos)


class Ground():
    def __init__(self, screen, block_group, speed):
        super().__init__()
        self.group = pygame.sprite.Group()
        self.screen = screen

        # create an extra ground to make the animation
        for i in range(round(screen_w / block_size) * 2):
            self.group.add(
                Block(block_group, (i * block_size, screen_h - block_size)))

    def render(self):
        # reset pos if first floor nearly reach its ending ([-2] position of the first floor)
        self.group.draw(self.screen)
        ground_sprites = self.group.sprites()
        if(ground_sprites[int(len(ground_sprites) / 2) - 1].rect.right <= 0):
            for i, block in enumerate(self.group.sprites()):
                block.rect.x = i * block_size
        else:
            for block in self.group.sprites():
                block.rect.x -= speed


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption("Flappy KN")
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        self.bg = BG(self.all_sprites)
        self.player = Player(self.all_sprites)
        self.ground = Ground(self.screen, self.all_sprites, speed)

    def run(self):
        last_time = time.time()
        while True:
            dt = time.time() - last_time
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("black")

            self.all_sprites.draw(self.screen)
            self.player.update(dt)
            self.ground.render()

            pygame.display.update()
            self.clock.tick(frame_rate)


if __name__ == "__main__":
    game = Game()
    game.run()
