import pygame

class HealthBar():
    def __init__(self, x, y, max_hp, bottom_color, top_color, width=200, height=20):
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.width = width      # default width
        self.height = height    # default height
        self.screen = pygame.display.get_surface()
        # define colors
        self.red = bottom_color # color for the bottom layer (damage taken)
        self.green = top_color # color for the top layer (current health)

    def draw(self, hp):
        # current health
        self.hp = hp
        # calculates health ratio
        ratio = self.hp / self.max_hp
        # bottom hp layer to show damage taken
        pygame.draw.rect(self.screen, self.red, (self.x, self.y, self.width, self.height))
        # upper hp layer to show max health
        pygame.draw.rect(self.screen, self.green, (self.x, self.y, self.width * ratio, self.height))
        # draw border
        pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)