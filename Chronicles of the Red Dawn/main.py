import sys
import pygame
import asset
from settings import Settings
from character import Fighter
from enemy import Demonic_Samurai
from healthbar import HealthBar
from combat_manager import Combat_Manager
from button import Button

class Game():
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        """characters"""
        self.fighter = Fighter(300, 555, 'Bravehart')
        self.demon_1 = Demonic_Samurai(950, 555, 'Demon')

        """health bars"""
        self.fighter_health_bar = HealthBar(150, 60, self.fighter.hp, self.fighter.max_hp)
        self.demon_1_health_bar = HealthBar(875, self.demon_1.rect.y, self.demon_1.hp, self.demon_1.max_hp, width= 150, height=8)

        self.combat = Combat_Manager(self.fighter, self.demon_1)
        self.in_combat = False
        self.action_taken = False

        """buttons"""
        self.start_btn = Button(900, 20, asset.play_img, 1.5)
        self.exit_btn = Button(1100, 20, asset.exit_img, 1.5)

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()           

            #combat logic
            if self.in_combat and self.action_taken == False:
                self.combat.player_phase()
                self.action_taken = True
                if self.action_taken == True:
                    self.combat.enemy_ai()
                    self.action_taken = False


    def draw_bg(self):
        self.screen.blit(asset.battle_bg, (0, 0))
    
    def draw_frame(self):
        self.screen.blit(asset.icon_frame, (50, 25))
    
    def draw_portrait(self):
        self.screen.blit(asset.actor1_icon, (62, 38))
    
    def draw_text(self, text, text_color, x, y):
        img = self.settings.font.render(text, True, text_color)
        self.screen.blit(img, (x, y))

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
    
    def _check_keydown_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)
            elif event.key == pygame.K_SPACE:
                pass

    def _update_screen(self):
        self.draw_bg()
        self.draw_frame()
        self.draw_portrait()
        """character"""
        self.fighter.draw()
        self.fighter.update()
        self.draw_text(f'HP: {self.fighter.hp}', asset.white, 150, 35)
        self.draw_text(f'{self.fighter.name}', asset.white, 45, 115)
        self.fighter_health_bar.draw(self.fighter.hp)

        self.demon_1.draw()
        self.demon_1.update()
        self.draw_text(f'{self.demon_1.name}', asset.red, self.demon_1_health_bar.x, 410)
        self.demon_1_health_bar.draw(self.demon_1.hp)

        if self.start_btn.draw(self.screen):
                self.in_combat = True
        if self.exit_btn.draw(self.screen):
            sys.exit()
        pygame.display.flip()

if __name__ == '__main__':
    CRD_game = Game()
    CRD_game.run_game()