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
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption("Chronicles of the Red Dawn")

        """characters"""
        self.fighter = Fighter(300, 555, 'Bravehart')
        self.demon_1 = Demonic_Samurai(950, 555, 'Demon')

        """health bars"""
        self.fighter_health_bar = HealthBar(150, 60, self.fighter.hp, self.fighter.max_hp)
        self.demon_1_health_bar = HealthBar(875, self.demon_1.rect.y, self.demon_1.hp, self.demon_1.max_hp, width= 150, height=8)

        self.combat = Combat_Manager(self.fighter, self.demon_1)
        self.action_taken = False

        """buttons"""
        self.start_btn = Button(675, 300, asset.play_img, 1)
        self.exit_btn = Button(675, 400, asset.exit_img, 1)
        self.credit_btn = Button(675, 500, asset.credits_img, 1)
        self.return_btn = Button(625, 330, asset.return_img, 1)
        self.return_title = Button(10, 650, asset.return_img, 1)

    def run_game(self):
        while True:
            self._check_events()
            self._battle_screen()
            self.clock.tick(60)           

            #turn logic
            if self.action_taken == False:
                self.combat.player_phase()
                self.action_taken = True
            if self.action_taken == True:
                self.combat.enemy_phase()
                self.action_taken = False

    def _battle_screen(self):
        """combat interface"""
        self.draw_bg()
        self.draw_frame()
        self.draw_portrait()
        self.draw_keys()
        self.draw_text('Attack', self.settings.white, 150, 685)
        self.draw_text('End Turn', self.settings.white, 350, 685)
        """character"""
        self.fighter.draw()
        self.fighter.update()
        self.draw_text(f'HP: {self.fighter.hp}', self.settings.white, 150, 35)
        self.draw_text(f'{self.fighter.name}', self.settings.white, 45, 115)
        self.fighter_health_bar.draw(self.fighter.hp)
        """enemies"""
        self.demon_1.draw()
        self.demon_1.update()
        self.draw_text(f'{self.demon_1.name}', self.settings.red, self.demon_1_health_bar.x, 410)
        self.demon_1_health_bar.draw(self.demon_1.hp)
        
        #checks for game over
        if self.fighter.is_alive == False:
            self.screen.blit(asset.defeat_img, (460, 150))
            # draws the return button to main menu
            self.draw_text('return to main menu', self.settings.white, 540, 300)
            if self.return_btn.draw(self.screen):
                self.main_menu()

        pygame.display.flip()

    def main_menu(self):
        while True:
            self.draw_title_screen()
            if self.start_btn.draw(self.screen):
                self.run_game()
            elif self.exit_btn.draw(self.screen):
                sys.exit()
            elif self.credit_btn.draw(self.screen):
                self.credit_screen()

            self._check_events()
            pygame.display.flip()

    def credit_screen(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.draw_text('Credits', self.settings.white, 600, 100) # title
            self.draw_text(
            'Dream Mix \n'
            'Prinbles \n'
            'JDSherbert, AnthonyTTurtlez \n'
            'saukgp \n'
            'russ123 \n'
            'tak_mfk \n'
            'Tiny Worlds \n'
            'Mounir Tohami \n'
            'vibrato08', self.settings.white, 500, 150) # Owners of some of the assets I used
            if self.return_title.draw(self.screen): # returns to main menu when clicked
                self.main_menu()
            self._check_events()
            pygame.display.flip()

    def draw_bg(self):
        self.screen.blit(asset.battle_bg, (0, 0))
    
    def draw_title_screen(self):
        self.screen.blit(asset.title_img, (0, 0))
    
    def draw_frame(self):
        self.screen.blit(asset.icon_frame, (50, 25))
    
    def draw_portrait(self):
        self.screen.blit(asset.actor1_icon, (62, 38))
    
    def draw_keys(self):
        self.screen.blit(asset.key_a_icon, (100, 675))
        self.screen.blit(asset.key_s_icon, (300, 675))
    
    def draw_text(self, text, text_color, x, y):
        img = self.settings.font.render(text, True, text_color)
        self.screen.blit(img, (x, y))

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
    
    def _check_keydown_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
            elif event.key == pygame.K_ESCAPE:
                self.main_menu()
            elif event.key == pygame.K_a:
                self.combat.player_attack()
                print("attack!")
            elif event.key == pygame.K_s:
                self.combat.player_pass()
                print("pass turn!")
            elif event.key == pygame.K_d:
                self.combat.player_guard()
                print("increased defense!")       

if __name__ == '__main__':
    CRD_game = Game()
    CRD_game.main_menu()