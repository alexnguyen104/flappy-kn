import pygame
from settings import screen_w


class Title(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.y = 200
        self.image = pygame.image.load("assets/title.png").convert_alpha()
        self.rect = self.image.get_rect(center=(screen_w/2, self.y))

    def update(self):
        if(self.rect.y >= self.y + 10):
            self.rect.y -= 1
        self.rect.y += 1
