import sys
import pygame
import asset
from settings import Settings
from character import Fighter
from enemy import Demonic_Samurai
from healthbar import HealthBar
from combat_manager import Combat_Manager
from button import Button
from dialogue import Dialogue
from damage_text import DamageText

class Game():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        """initialize the game window"""
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Chronicles of the Red Dawn")

        """Game States"""
        self.game_state = 'main_menu' # Possible states: main_menu, battle, credits, game_over, victory, exit

        self.action_taken = False

        """buttons"""
        self.start_btn = Button(675, 300, asset.play_img, 1)
        self.exit_btn = Button(675, 400, asset.exit_img, 1)
        self.credit_btn = Button(675, 500, asset.credits_img, 1)
        self.return_btn = Button(625, 330, asset.return_img, 1)
        self.return_title = Button(10, 650, asset.return_img, 1)

        # Battle state components are initially set to None
        # they will be set up by the `inititialize_battle` method
        self.fighter = None
        self.demon_1 = None
        self.fighter_health_bar = None
        self.demon_1_health_bar = None
        self.combat = None
        self.dialogue = None
        self.show_dialogue = False

        # --- Music loader ---
        pygame.mixer.init()  # Initialize the mixer module
        self.battle_theme = asset.battle_theme  # Load the battle theme music
        self.title_theme = asset.title_theme  # Load the title theme music
        self.current_music = None  # Variable to keep track of currently playing music

        # damage text
        self.damage_texts = []  # List to hold active damage texts

    
    def _initialize_battle(self):
        """Initializes or resets the battle state for a new game or after a defeat."""

        """characters"""
        self.fighter = Fighter(300, 555, 'Bravehart', self.settings.character_scale, self.settings.fighter_cooldown)
        self.demon_1 = Demonic_Samurai(950, 555, 'Demon', self.settings.character_scale, self.settings.demon_cooldown)

        """health bars"""
        self.fighter_health_bar = HealthBar(150, 60, self.fighter.hp, self.fighter.max_hp, self.settings.red, self.settings.green)
        self.demon_1_health_bar = HealthBar(self.demon_1.rect.x + 120, self.demon_1.rect.y - 20, self.demon_1.hp, self.demon_1.max_hp, self.settings.red, self.settings.green, width= 150, height=8)

        # pass the fighter and enemy instances to the combat manager
        self.combat = Combat_Manager(self.fighter, self.demon_1)
        # Initialize the dialogue system
        self.dialogue = Dialogue(self.settings.screen_width, self.settings.screen_height, self.settings.white, self.settings.font)
        self.dialogue_text = ["A demon has appeared!",
                              "Prepare for battle!"]
        self.dialogue_index = 0
        self.show_dialogue = True # Show dialogue at the start of the battle

        pygame.mixer.music.stop()  # Stop any currently playing music
        pygame.mixer.music.load(self.battle_theme)  # Load the battle theme music
        pygame.mixer.music.play(-1)
        self.current_music = 'battle_theme'  # Set the current music to battle theme


    def run_game(self):
        """Main game loop that runs and updates the game state."""
        while True:
            self._check_events() # check for user input

            if self.game_state == 'main_menu':
                self._main_menu()
            elif self.game_state == 'battle':
                self._battle_screen()
                self._update_battle_logic()
                if not self.fighter.is_alive: # if the fighter is dead, change game state to game_over
                    self.game_state = 'game_over'
            elif self.game_state == 'credits':
                self._credit_screen()
            elif self.game_state == 'game_over':
                self._game_over_screen()
            elif self.game_state == 'victory':
                pass
            elif self.game_state == 'exit':
                sys.exit()
            
            pygame.display.flip()
            self.clock.tick(60) # Caps frame rate to 60 FPS

    def _main_menu(self):
        """Main menu screen with buttons to start the game, view credits, or exit."""
        self.draw_title_screen() # Draws the title screen background
        if not pygame.mixer.music.get_busy() or self.current_music != 'title_theme': # If music is not playing, play the title theme
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.title_theme) # Load the title theme music
            pygame.mixer.music.play(-1)
            self.current_music = 'title_theme' # Update current music to title theme

        # Draws a semi-transparent overlay to dim the background
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 25))
        self.screen.blit(overlay, (0, 0)) # Add a semi-transparent overlay

        # Check for button clicks
        if self.start_btn.draw(self.screen):
            self._initialize_battle()
            self.game_state = 'battle' # Change game state to battle
        elif self.exit_btn.draw(self.screen):
            self.game_state = 'exit' # Change game state to exit
        elif self.credit_btn.draw(self.screen):
            self.game_state = 'credits' # Change game state to credits

    def _credit_screen(self):
        """Credits screen displaying the names of contributors and assets used."""
        # Draws the credits screen background and text
        self.screen.fill((0, 0, 0))
        self.draw_text('Credits', self.settings.white, 600, 100) # title
        self.draw_text(
        'Dream Mix \n'
        'Prinbles \n'
        'JDSherbert, AnthonyTTurtlez \n'
        'saukgp \n'
        'Rem Chronicle \n'
        'russ123 \n'
        'Tiny Worlds \n'
        'Mounir Tohami \n'
        'vibrato08', self.settings.white, 500, 150
        ) # Owners of some of the assets I used
        
        if self.return_title.draw(self.screen): # returns to main menu when clicked
            self.game_state = 'main_menu'
    
    def _battle_screen(self):
        """Renders the battle screen with the player and enemy characters, health bars, and combat interface."""
        # Draws all static elements of the battle screen
        self.draw_bg()
        if not self.show_dialogue:
            # If dialogue is not being shown, draw the battle interface
            self.draw_frame()
            self.draw_portrait()
            self.draw_keys()
            self.draw_text('Attack', self.settings.white, 150, 685)
            self.draw_text('End Turn', self.settings.white, 350, 685)
            # Draws the player's health and name
            self.draw_text(f'HP: {self.fighter.hp}', self.settings.white, 150, 35)
            self.draw_text(f'{self.fighter.name}', self.settings.white, 45, 115)
            self.fighter_health_bar.draw(self.fighter.hp)
            # Draws the enemy's health and name
            self.draw_text(f'{self.demon_1.name}', self.settings.red, self.demon_1_health_bar.x, self.demon_1_health_bar.y - 20)
            self.demon_1_health_bar.draw(self.demon_1.hp)

        # Player character
        self.fighter.draw()
        self.fighter.update()
        # Enemy character
        self.demon_1.draw()
        self.demon_1.update()

        # Draws the dialogue box if it is set to be shown
        if self.show_dialogue and self.dialogue:
            self.dialogue.draw_dialogue(self.screen, self.dialogue_text[self.dialogue_index])

        # Draws the damage texts above the enemy
        for dmg_text in self.damage_texts:
            if dmg_text.is_alive():
                dmg_text.draw(self.screen)
        # Remove damage texts that have expired
        self.damage_texts = [dt for dt in self.damage_texts if dt.is_alive()]

    def _game_over_screen(self):
        """Displays the game over screen with an option to return to the main menu."""
        self.draw_bg()
        self.draw_frame()
        self.draw_portrait()
        # Draw characters and their animations even if the player has lost
        self.fighter.update()
        self.fighter.draw()
        self.fighter_health_bar.draw(self.fighter.hp)
        self.draw_text(f'HP: {self.fighter.hp}', self.settings.white, 150, 35)
        self.draw_text(f'{self.fighter.name}', self.settings.white, 45, 115)
        # Draw the enemy character and its health bar
        self.demon_1.update()
        self.demon_1.draw()
        self.demon_1_health_bar.draw(self.demon_1.hp)
        self.draw_text(f'{self.demon_1.name}', self.settings.red, self.demon_1_health_bar.x, self.demon_1_health_bar.y - 20)
        
        # Draws a semi-transparent overlay to dim the background when game is over
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0)) # Add a semi-transparent overlay
        
        # Draws the game over image and text
        self.screen.blit(asset.defeat_img, (460, 150))
        self.draw_text('return to main menu', self.settings.white, 540, 300)

        # Check if the return button is clicked to go back to the main menu
        if self.return_btn.draw(self.screen):
            pygame.mixer.music.stop() # Stop the battle music when returning to the main menu
            self.game_state = 'main_menu'
    
    def _update_battle_logic(self):
        """Handles turn based progression in the battle."""
        if self.combat:
            if self.combat.is_player_turn():
                self.combat.update_player_phase() # Allows the player's turn to take actions when ready
            elif self.combat.is_enemy_turn():
                damage = self.combat.update_enemy_phase() # Allows the enemy's turn to take actions when ready
                if damage is not None:
                    # Show damage text above the player
                    self.damage_texts.append(
                        DamageText(f"-{damage}",
                                   self.fighter.rect.centerx,
                                   self.fighter.rect.y,
                                   self.settings.red,
                                   self.settings.font,
                                   self.settings.text_duration)
                    )
                    print("enemy attack!")

    # --- Methods for drawing static UI elements on the screen ---
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
        """Processes all events in the game loop."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = 'exit'  # Exit the game
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
    
    def _check_keydown_events(self, event):
        """Handles keydown events for the game."""
        # --- Dialogue input handling ---
        if self.show_dialogue and self.dialogue:
            if event.key in [pygame.K_RETURN, pygame.K_SPACE]: # If the user presses Enter or Space
                # If the dialogue is being shown, advance to the next line or hide it
                self.dialogue_index += 1
                if self.dialogue_index >= len(self.dialogue_text):
                    self.show_dialogue = False
            return # Prevent other key events from being processed when dialogue is active
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
            elif event.key == pygame.K_ESCAPE:
                # Allows the user to return to main menu from any game state
                if self.game_state in ['battle', 'credits', 'game_over']:
                    pygame.mixer.music.stop()  # Stop the battle music
                    self.game_state = 'main_menu' 
            elif self.game_state == 'battle': # Check for key presses only in battle state
                if self.combat and self.combat.is_player_turn():
                    # Check for player actions based on key presses
                    # Player can attack, pass turn, or guard
                    if event.key == pygame.K_a:
                        damage = self.combat.player_attack()
                        if damage is not None:
                            # Show damage text above the enemy
                            self.damage_texts.append(
                                DamageText(f"-{damage}",
                                           self.demon_1.rect.centerx,
                                           self.demon_1.rect.y,
                                           self.settings.red,
                                           self.settings.font,
                                           self.settings.text_duration)
                            )
                            print("attack!")
                    elif event.key == pygame.K_s:
                        self.combat.player_pass()
                        print("pass turn!")
                    elif event.key == pygame.K_d:
                        guard = self.combat.player_guard()
                        if guard is not None:
                            self.damage_texts.append(
                                DamageText("Increased Defense!",
                                           self.fighter.rect.centerx - 100,
                                           self.fighter.rect.y,
                                           self.settings.white,
                                           self.settings.font,
                                           self.settings.text_duration)
                            )
                        print("increased defense!")  
                    elif event.key == pygame.K_f:
                        healed = self.combat.player_heal(self.settings.heal_amount)     
                        if healed is not None:
                            # Show healing text above the player
                            self.damage_texts.append(
                                DamageText(f"+{healed}",
                                           self.fighter.rect.centerx,
                                           self.fighter.rect.y,
                                           self.settings.green,
                                           self.settings.font,
                                           self.settings.text_duration)
                            )
                            print("healed!")

if __name__ == '__main__':
    CRD_game = Game()
    CRD_game.run_game()