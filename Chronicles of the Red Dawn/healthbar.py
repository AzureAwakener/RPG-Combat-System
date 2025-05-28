import pygame

class HealthBar():
    def __init__(self, x, y, hp, max_hp, width=200, height=20):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
        self.width = width      # default width
        self.height = height    # default height
        self.screen = pygame.display.get_surface()
        #define colors
        self.red = (220, 20, 60)
        self.green = (139, 190, 27)

    def draw(self, hp):
        #current health
        self.hp = hp
        #calculates health ratio
        ratio = self.hp / self.max_hp
        #bottom hp layer to show damage taken
        pygame.draw.rect(self.screen, self.red, (self.x, self.y, self.width, self.height))
        #upper hp layer to show max health
        pygame.draw.rect(self.screen, self.green, (self.x, self.y, self.width*ratio, self.height))