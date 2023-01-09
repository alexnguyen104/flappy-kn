import pygame


def play_sound(file_path):
    sound = pygame.mixer.Sound(file_path)
    pygame.mixer.Sound.play(sound)
