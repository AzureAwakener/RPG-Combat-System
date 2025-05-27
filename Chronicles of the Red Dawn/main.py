import pygame
from character import Fighter

#-------------------------------------
#          Screen Resolution
#-------------------------------------
ui_panel = 150
width, height = 1280, 570 + ui_panel

screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption('Chronicles of the Red Dawn')

#-------------------------------------
#           Image Database
#-------------------------------------
battle_bg = pygame.image.load('img/battle_bg/forest.png')
battle_bg = pygame.transform.scale(battle_bg, (battle_bg.get_width() * 1.75, battle_bg.get_height() * 1.85)).convert_alpha()

#-------------------------------------
#           Draw Functions
#-------------------------------------
Fighter(200, 250, 'Brand')

#draws battle background screen
def draw_bg():
    screen.blit(battle_bg, (0, 0))

#-------------------------------------
#              Game Loop
#-------------------------------------
class Game():
    def __init__(self):
        pygame.init()
        
    def run_game():
        while True:
            draw_bg()

            Fighter.update()
            Fighter.draw()
            
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if keys[pygame.K_ESCAPE]:
                    pygame.quit()
    
            pygame.display.update()

if __name__ == '__main__':
    Game.run_game()