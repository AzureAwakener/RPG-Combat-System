import pygame
class Settings():
    """Stores all system settings for CRD"""

    def __init__(self):
        pygame.init()
        """game font"""
        self.font = pygame.font.Font('Chronicles of the Red Dawn/font/ThaleahFat.ttf', 26)
        #screen display
        self.screen_width = 1280
        self.screen_height = 720
        