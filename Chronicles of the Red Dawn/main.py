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

        # initialize the game screen
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Chronicles of the Red Dawn")
        self.fullscreen = False  # Flag to track fullscreen state

        # initialize the game state
        self.game_state = 'main_menu' # Possible states: main_menu, battle, credits, game_over, victory, exit

        # --- Buttons for the main menu ---
        self.start_btn = Button(675, 300, asset.play_img, 1)
        self.exit_btn = Button(675, 400, asset.exit_img, 1)
        self.credit_btn = Button(675, 500, asset.credits_img, 1)
        self.return_btn = Button(625, 330, asset.return_img, 1)
        self.return_title = Button(10, 650, asset.return_img, 1)

        # battle state components are initially set to None
        # they will be set up by the `inititialize_battle` method
        self.fighter = None
        self.demon_1 = None
        self.fighter_health_bar = None
        self.demon_1_health_bar = None
        self.combat = None
        
        # dialogue flags
        self.dialogue = None
        self.show_dialogue = None
        # midpoint dialogue
        self.dialogue_midpoint = None
        self.show_dialogue_midpoint = None 
        self.midpoint_shown = None 
        # post-battle dialogue
        self.victory_dialogue = False
        self.show_victory_dialogue = False
        self.defeat_dialogue = False
        self.show_defeat_dialogue = False


        # --- Music loader ---
        pygame.mixer.init()  # Initialize the mixer module
        self.battle_theme = asset.battle_theme  # Load the battle theme music
        self.title_theme = asset.title_theme  # Load the title theme music
        self.current_music = None  # Variable to keep track of currently playing music

        # damage text
        self.damage_texts = []  # List to hold active damage texts
        # action display
        self.action_display_text = ""
        self.action_display_time = 0  # seconds for which the action display text is shown
        self.action_display_start = 0  # pygame.time.get_ticks() when the action display starts

    
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
        # initialize the dialogue system
        self.dialogue = Dialogue(self.settings.screen_width, self.settings.screen_height, self.settings.white, self.settings.font)
        self.dialogue_text = ["A demon has appeared!",
                              "Prepare for battle!"]
        self.dialogue_index = 0
        self.show_dialogue = True # Show dialogue at the start of the battle

        # dialogue that appears at the midpoint of the battle
        self.dialogue_midpoint = Dialogue(self.settings.screen_width, self.settings.screen_height, self.settings.white, self.settings.font)
        self.dialogue_midpoint_text = ["You are strong, but I will not go down easily!",
                                       "Prepare for my wrath!"]
        self.dialogue_midpoint_index = 0
        self.midpoint_shown = False  # Flag to track if midpoint dialogue has been shown

        # post battle dialogue
        self.victory_dialogue = Dialogue(self.settings.screen_width, self.settings.screen_height, self.settings.white, self.settings.font)
        self.victory_dialogue_text = ["You have defeated the demon!",
                                      "Return to the main menu to play again!"]
        self.victory_dialogue_index = 0
        self.show_victory_dialogue = False  # Flag to track if victory dialogue should be shown

        self.defeat_dialogue = Dialogue(self.settings.screen_width, self.settings.screen_height, self.settings.white, self.settings.font)
        self.defeat_dialogue_text = ["You have been defeated!",
                                     "Return to the main menu to try again!"]
        self.defeat_dialogue_index = 0
        self.show_defeat_dialogue = False  # Flag to track if defeat dialogue should be shown

        # music setup
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
                if not self.fighter.is_alive:
                    self.show_defeat_dialogue = True
                    self.defeat_dialogue_index = 0
                    self.game_state = 'post_battle'  # Change game state to post_battle
                elif not self.demon_1.is_alive:
                    self.show_victory_dialogue = True
                    self.victory_dialogue_index = 0
                    self.game_state = 'post_battle' # Change game state to post_battle
            elif self.game_state == 'credits':
                self._credit_screen()
            elif self.game_state == 'post_battle':
                self._post_battle_screen()
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
        if not self.show_dialogue and not self.show_dialogue_midpoint:
            # If dialogue is not being shown, draw the battle interface
            self.draw_frame()
            self.draw_portrait()
            self.draw_keys()
            self.draw_text('Attack', self.settings.white, 150, 685)
            self.draw_text('End Turn', self.settings.white, 350, 685)
            self.draw_text('Guard', self.settings.white, 550, 685)
            self.draw_text('Heal', self.settings.white, 750, 685)
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
        
        # If the dialogue is at the midpoint, show the midpoint dialogue
        if self.demon_1.hp <= self.demon_1.max_hp // 2 and not self.show_dialogue_midpoint and not self.midpoint_shown:
            self.dialogue_midpoint_index = 0  # Reset the midpoint dialogue index
            self.show_dialogue_midpoint = True  # Show the midpoint dialogue
            self.midpoint_shown = True # prevents showing the midpoint dialogue again
        
        # Check if the dialogue midpoint should be shown
        if self.show_dialogue_midpoint and self.dialogue_midpoint:
            self.dialogue_midpoint.draw_dialogue(self.screen, self.dialogue_midpoint_text[self.dialogue_midpoint_index])
            return  # Prevents drawing the rest of the UI while dialogue is up

        # Draws the damage texts above the enemy
        for dmg_text in self.damage_texts:
            if dmg_text.is_alive():
                dmg_text.draw(self.screen)
        # Remove damage texts that have expired
        self.damage_texts = [dt for dt in self.damage_texts if dt.is_alive()]

        # Draws the action display text if it is set to be shown
        if self.action_display_text and pygame.time.get_ticks() - self.action_display_start < self.action_display_time:
            text_img = self.settings.font.render(self.action_display_text, True, self.settings.white)
            text_rect = text_img.get_rect(center=(self.settings.screen_width // 2, 200))

            # Draws a semi-transparent overlay behind the action display text
            padding = 30
            # Calculate the size of the overlay based on the text size
            overlay_width, overlay_height = self.settings.screen_width + padding, text_rect.height + padding // 2
            # center the overlay on the text
            overlay_x, overlay_y = text_rect.centerx - overlay_width // 2, text_rect.centery - overlay_height // 2

            overlay_surface = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
            overlay_surface.fill((0, 0, 0, 150))

            # blit the overlay surface
            self.screen.blit(overlay_surface, (overlay_x, overlay_y))
            self.screen.blit(text_img, text_rect)

    def _post_battle_screen(self):
        """Handles the post-battle screen after the player has won or lost."""
        self.draw_bg()
        # Draw characters and their animations even if the battle is over
        self.fighter.update()
        self.fighter.draw()
        # Draw the enemy character and its health bar
        self.demon_1.update()
        self.demon_1.draw()
        # --- post-battle dialogue handling ---
        if self.show_victory_dialogue and self.victory_dialogue:
            # Draws the victory dialogue if it is set to be shown
            self.victory_dialogue.draw_dialogue(self.screen, self.victory_dialogue_text[self.victory_dialogue_index])
            return
        if self.show_defeat_dialogue and self.defeat_dialogue:
            # Draws the defeat dialogue if it is set to be shown
            self.defeat_dialogue.draw_dialogue(self.screen, self.defeat_dialogue_text[self.defeat_dialogue_index])
            return
        
        self.draw_frame()
        self.draw_portrait()
        self.fighter_health_bar.draw(self.fighter.hp)
        self.draw_text(f'HP: {self.fighter.hp}', self.settings.white, 150, 35)
        self.draw_text(f'{self.fighter.name}', self.settings.white, 45, 115)
        self.demon_1_health_bar.draw(self.demon_1.hp)
        self.draw_text(f'{self.demon_1.name}', self.settings.red, self.demon_1_health_bar.x, self.demon_1_health_bar.y - 20)

        if not self.fighter.is_alive:
            # Draws a semi-transparent overlay to dim the background when game is over
            overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0)) # Add a semi-transparent overlay

            # Draws the game over image and text
            self.screen.blit(asset.defeat_img, (460, 150))
            self.draw_text('return to main menu', self.settings.white, 540, 300)
        elif not self.demon_1.is_alive:
            # If the player has won, show victory text
            # Draws a semi-transparent overlay to dim the background when game is over
            overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0)) # Add a semi-transparent overlay

            # Draws the game over image and text
            self.screen.blit(asset.victory_img, (460, 150))
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
        self.screen.blit(asset.key_d_icon, (500, 675))
        self.screen.blit(asset.key_f_icon, (700, 675))
    
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
        
        # --- Midpoint dialogue input handling ---
        if self.show_dialogue_midpoint and self.dialogue_midpoint:
            if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                self.dialogue_midpoint_index += 1
                if self.dialogue_midpoint_index >= len(self.dialogue_midpoint_text):
                    self.show_dialogue_midpoint = False
            return # Prevent other key events from being processed when midpoint dialogue is active
        
        # --- Post-battle victory dialogue ---
        if self.show_victory_dialogue and self.victory_dialogue:
            if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                self.victory_dialogue_index += 1
                if self.victory_dialogue_index >= len(self.victory_dialogue_text):
                    self.show_victory_dialogue = False
            return

        # --- Post-battle defeat dialogue ---
        if self.show_defeat_dialogue and self.defeat_dialogue:
            if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                self.defeat_dialogue_index += 1
                if self.defeat_dialogue_index >= len(self.defeat_dialogue_text):
                    self.show_defeat_dialogue = False
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                # Toggle fullscreen mode
                if not self.fullscreen:
                    pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)
                    self.fullscreen = True
                else:
                    pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
                    self.fullscreen = False
            elif event.key == pygame.K_ESCAPE:
                # Allows the user to return to main menu from any game state
                if self.game_state in ['battle', 'credits', 'post_battle']:
                    pygame.mixer.music.stop()  # Stop the battle music
                    self.game_state = 'main_menu' 

            # Check for key presses only in battle state        
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
                            # set action display text
                            self.action_display_text = "Slash!"
                            self.action_display_time = 1000 # Show action display for 1 second
                            self.action_display_start = pygame.time.get_ticks()  # Start the action display timer
                            print("attack!")
                    elif event.key == pygame.K_s:
                        self.combat.player_pass()
                        self.action_display_text = "Show me what you got!"
                        self.action_display_time = 1000 # Show action display for 1 second
                        self.action_display_start = pygame.time.get_ticks()  # Start the action display timer
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
                            self.action_display_text = "Guard!"
                            self.action_display_time = 1000 # Show action display for 1 second
                            self.action_display_start = pygame.time.get_ticks()  # Start the action display timer
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
                            self.action_display_text = "Warcry!"
                            self.action_display_time = 1000 # Show action display for 1 second
                            self.action_display_start = pygame.time.get_ticks()  # Start the action display timer
                            print("healed!")

if __name__ == '__main__':
    CRD_game = Game()
    CRD_game.run_game()