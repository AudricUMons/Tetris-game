import pygame

def load_sounds():
    pygame.mixer.init()
    return {
        "rotate": pygame.mixer.Sound(  "assets/m.wav"),
        "place": pygame.mixer.Sound(   "assets/m.wav"),
        "clear": pygame.mixer.Sound(   "assets/m.wav"),
        "gameover": pygame.mixer.Sound("assets/m.wav")
    }