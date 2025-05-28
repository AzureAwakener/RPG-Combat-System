import pygame
from character import Fighter
from enemy import Shogun
from settings import Settings
from healthbar import HealthBar

#-------------------------------------
#              Game Loop
#-------------------------------------
class Game():
    #-------------------------------------
    #           Image Database
    #-------------------------------------
    battle_bg = pygame.image.load('img/battle_bg/forest.png')
    battle_bg = pygame.transform.scale(battle_bg, 
                                       (battle_bg.get_width() * 1.75, battle_bg.get_height() * 1.85))
    icon_frame = pygame.image.load('img/battle_interface/icon border.png')
    icon_frame = pygame.transform.scale(icon_frame, 
                                        (icon_frame.get_width() * 2, icon_frame.get_height() * 2))
    brand_icon = pygame.image.load('img/battle_interface/brand_icon.png')
    brand_icon = pygame.transform.scale(brand_icon, 
                                        (brand_icon.get_width() * 1.5, brand_icon.get_height() * 1.5))

    #define colors
    red = (220, 20, 60)
    green = (139, 190, 27)
    white = (240,255,255)

    fullscreen = True

    def __init__(self):
        pygame.init()
        """Call Classes from imports"""
        self.settings = Settings() #settings.py
        #-------------------------------------
        #          Screen Resolution
        #-------------------------------------
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption('Chronicles of the Red Dawn')
        pygame.display.set_icon(Game.brand_icon)

        #define font
        self.font = pygame.font.Font('font/ThaleahFat.ttf', 26)

        """Initializes characters"""
        self.fighter = Fighter(300, 505, 'Brand')
        self.boss = Shogun(900, 445, 'Shogun')
        """Initializes HP Bars"""
        self.fighter_health_bar = HealthBar(150, 60, self.fighter.hp, self.fighter.max_hp)
        self.boss_health_bar = HealthBar(790, 300, self.boss.hp, self.boss.max_hp, width=300, height=5)
    
    #draw texts
    def draw_text(self, text, text_color, x, y):
        img = self.font.render(text, True, text_color)
        self.screen.blit(img, (x, y))

    def run_game(self):
        while True:
            #-------------------------------------
            #           Draw Functions
            #-------------------------------------
            """draws battle background screen"""
            def draw_bg():
                self.screen.blit(Game.battle_bg, (0, 0))
            def draw_frame():
                self.screen.blit(Game.icon_frame, (50, 25))
            def draw_portrait():
                self.screen.blit(Game.brand_icon, (62, 38))
            # battle background and interface
            draw_bg()
            draw_frame()
            draw_portrait()
            # brand
            self.fighter.update()
            self.fighter.draw()
            self.fighter_health_bar.draw(self.fighter.hp)
            self.draw_text(f'{self.fighter.name} HP: {self.fighter.hp}', Game.white, 150, 35)
            # shogun
            self.boss.update()
            self.boss.draw()
            self.boss_health_bar.draw(self.boss.hp)
            self.draw_text(f'{self.boss.name}', Game.red, 900, 280)
            
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    """fullscreen mode"""
                if keys[pygame.K_ESCAPE]:
                    if Game.fullscreen == True:
                        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
                        Game.fullscreen = False # exit fullscreen
                    else:
                        pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)
                        Game.fullscreen = True # return to fullscreen
    
            pygame.display.update()

if __name__ == '__main__':
    crd = Game()
    crd.run_game()