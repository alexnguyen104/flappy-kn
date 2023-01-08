import pygame
from settings import screen_w, screen_h


class Title(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.center_y = 160

        self.image = pygame.image.load("assets/title.png").convert_alpha()
        self.rect = self.image.get_rect(center=(screen_w/2, self.center_y))

        self.is_moving_up = False
        self.animation_speed = 1

    def update(self, is_start):
        self.rect.centery += self.animation_speed

        if self.rect.centery >= self.center_y + 40:
            self.animation_speed = -self.animation_speed
        elif self.rect.centery <= self.center_y:
            self.animation_speed = -self.animation_speed

        if is_start:
            self.kill()


class Text(pygame.sprite.Sprite):
    def __init__(self, group, text, color, pos, size, is_center):
        super().__init__(group)
        self.color = color
        self.font = pygame.font.Font('assets/font/Mario-Kart-DS.ttf', size)
        self.image = self.font.render(text, True, self.color)
        if is_center:
            self.rect = self.image.get_rect(center=pos)
        else:
            self.rect = self.image.get_rect(topleft=pos)

    def update_text(self, text):
        self.image = self.font.render(text, True, self.color)


class All_Text():
    def __init__(self, group):
        credits_text = ["developer - KN", "most graphics - CLEAR CODE"]
        self.credits_group = pygame.sprite.Group()
        for i in range(len(credits_text)):
            self.credits_group.add(
                Text(group, credits_text[i], (255, 255, 255), (10, (screen_h - 50) + i * 20), 20, False))

        self.start_text = pygame.sprite.GroupSingle()
        self.start_text.add(Text(group, "press space to begin",
                            (51, 50, 61), (screen_w / 2, screen_h / 1.35), 30, True))

        self.counter = 0

        self.score_text = pygame.sprite.GroupSingle()
        self.score_text.add(Text(group, "0", (51, 50, 61),
                            (screen_w / 2, screen_h), 70, True))

    def start_text_animation(self):

        self.counter += 0.03
        if int(self.counter) % 2:
            self.start_text.sprite.rect.y = screen_h  # make text off-screen
        else:
            self.start_text.sprite.rect.y = screen_h / 1.35

    def update(self, is_start, score):
        if is_start:
            self.score_text.sprite.rect.centery = screen_h / 2
            self.score_text.sprite.update_text(str(score))
            self.start_text.sprite.rect.y = screen_h  # make text off-screen
        else:
            self.start_text_animation()
