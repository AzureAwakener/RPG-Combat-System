import pygame
class Settings():
    """Stores all system settings for CRD"""

    def __init__(self):
        pygame.init()
        # game font
        self.font = pygame.font.Font('Chronicles of the Red Dawn/font/ThaleahFat.ttf', 26)
        # system colors
        self.red = (220, 20, 60)
        self.green = (139, 190, 27)
        self.white = (240,255,255)
        # screen display
        self.screen_width = 1280
        self.screen_height = 720
        # animation settings
        self.fighter_cooldown = 150
        self.demon_cooldown = 165
        # animation scale
        self.character_scale = 2.5 # scale for character animations
        # damage text settings
        self.text_duration = 0.8 # seconds
        # healing settings
        self.heal_amount = 20 # amount of health restored