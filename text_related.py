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


class Score_Board(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.image = pygame.image.load(
            "assets/score_board.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)


class All_Text():
    def __init__(self, group):
        self.group = group

        credits_text = ["developer - KN", "most graphics - CLEAR CODE"]
        self.credits_group = pygame.sprite.Group()
        for i in range(len(credits_text)):
            self.credits_group.add(
                Text(self.group, credits_text[i], (255, 255, 255), (10, (screen_h - 50) + i * 20), 20, False))

        self.start_text = pygame.sprite.GroupSingle()
        self.start_text.add(Text(self.group, "press space to begin",
                            (245, 241, 222), (screen_w / 2, screen_h / 1.35), 40, True))

        self.counter = 0

        self.score_text = pygame.sprite.GroupSingle()
        self.score_text.add(Text(self.group, "0", (51, 50, 61),
                            (screen_w / 2, screen_h + 100), 70, True))  # make text off-screen

        self.game_over_board = pygame.sprite.Group()
        self.game_over_board.add(Score_Board(
            self.group, (screen_w / 2 - 5, screen_h + 200)))  # make board off-screen
        self.game_over_board.add(Text(self.group, str(
            "0"), (245, 241, 222), (screen_w / 2, screen_h + 100), 90, True))  # make text off-screen
        self.game_over_board.add(
            Text(self.group, "press enter to play again", (51, 50, 61), (screen_w / 2, screen_h + 100), 25, True))  # make text off-screen

    def start_text_animation(self):

        self.counter += 0.03
        if int(self.counter) % 2:
            self.start_text.sprite.rect.y = screen_h  # make text off-screen
        else:
            self.start_text.sprite.rect.y = screen_h / 1.35

    def game_over(self, score):
        self.game_over_board.sprites()[0].rect.centery = screen_h / 2
        self.game_over_board.sprites()[1].rect.centery = screen_h / 1.75
        self.game_over_board.sprites()[1].update_text(str(score))
        self.game_over_board.sprites()[2].rect.centery = screen_h / 1.5

    def update(self, is_start, score):
        if is_start:
            self.score_text.sprite.rect.centery = screen_h / 2
            self.score_text.sprite.update_text(str(score))
            self.start_text.sprite.rect.y = screen_h  # make text off-screen
            for i in self.credits_group.sprites():  # make text off-screen
                i.rect.y = screen_h
        else:
            self.start_text_animation()
