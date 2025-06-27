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
        self.start_btn = Button(self.settings.button_width, self.settings.button_height, asset.play_img, 1)
        self.exit_btn = Button(self.settings.button_width, self.settings.button_height + self.settings.button_offset_y, asset.exit_img, 1)
        self.credit_btn = Button(self.settings.button_width, self.settings.button_height + 2 * self.settings.button_offset_y, asset.credits_img, 1)
        self.return_btn = Button(self.settings.return_btn_x, self.settings.return_btn_y, asset.return_img, 1)
        self.return_title = Button(self.settings.return_title_x, self.settings.return_title_y, asset.return_img, 1)
        
        # dialogue flags
        self.show_dialogue = False
        # midpoint dialogue
        self.show_dialogue_midpoint = False 
        self.midpoint_shown = False 
        # post-battle dialogue
        self.show_victory_dialogue = False
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
        self.fighter = Fighter(self.settings.fighter_x, self.settings.character_y, 'Bravehart', self.settings.character_scale, self.settings.fighter_cooldown, self.settings)
        self.demon_1 = Demonic_Samurai(self.settings.enemy_x, self.settings.character_y, 'Ren', self.settings.character_scale, self.settings.demon_cooldown, self.settings)

        """health bars"""
        self.fighter_health_bar = HealthBar(self.settings.fighter_healthbar_x, self.settings.fighter_healthbar_y, 
                                            self.fighter.max_hp, self.settings.red, self.settings.green)
        self.demon_1_health_bar = HealthBar(self.demon_1.rect.x + self.settings.demon_healthbar_offset_x, self.demon_1.rect.y - self.settings.demon_healthbar_offset_y,
                                            self.demon_1.max_hp, self.settings.red, self.settings.green, 
                                            width= self.settings.demon_healthbar_width, height= self.settings.demon_healthbar_height) # custom w/h for enemy

        # pass the fighter and enemy instances to the combat manager
        self.combat = Combat_Manager(self.fighter, self.demon_1)
        # initialize the dialogue system
        self.dialogue = Dialogue(self.settings.screen_width, self.settings.screen_height, self.settings.white, self.settings.font)
        self.dialogue_text = ["Bravehart: A village transformed into demons overnight.",
                              "Bravehart: Whoever did this has been plotting this for a long time.",
                              "Bravehart: Speak of the devil.",
                              "Ren: As expected of the Crimson Knight. Seems like drugs doesn't work on you anymore.",
                              "Bravehart: That name already died alongside my kingdom.",
                              "Ren: A man of your caliber shouldn't be working as a mere mercenary.",
                              "Ren: Come and join us.",
                              "Bravehart: I refuse.",
                              "Ren: A pity.",
                              "Ren: Guess I'll just have to kill you!",
                              "Prepare for battle!"]
        self.dialogue_index = 0
        self.show_dialogue = True # Show dialogue at the start of the battle

        # dialogue that appears at the midpoint of the battle
        self.dialogue_midpoint = Dialogue(self.settings.screen_width, self.settings.screen_height, self.settings.white, self.settings.font)
        self.dialogue_midpoint_text = ["Ren: fufu",
                                        "Ren: Impressive.",
                                       "Ren: Show me everything you got!"]
        self.dialogue_midpoint_index = 0
        self.midpoint_shown = False  # Flag to track if midpoint dialogue has been shown

        # post battle dialogue
        self.victory_dialogue = Dialogue(self.settings.screen_width, self.settings.screen_height, self.settings.white, self.settings.font)
        self.victory_dialogue_text = ["Ren: Playtime's over",
                                      "Ren: I'd love to fight a bit longer, but the Maestro is not gonna be happy with that.",
                                      "Ren: Ta-ta~",
                                      "Bravehart: Tch! How did I not realize I was fighting a fake body.",
                                      "Bravehart: I have to move quick, maybe I can still save some people."
                                      "Battle Over!",
                                      "Thank you for playing my combat demo!"]
        self.victory_dialogue_index = 0
        self.show_victory_dialogue = False  # Flag to track if victory dialogue should be shown

        self.defeat_dialogue = Dialogue(self.settings.screen_width, self.settings.screen_height, self.settings.white, self.settings.font)
        self.defeat_dialogue_text = ["Ren: How disappointing.",
                                     "Return to the main menu to try again!"]
        self.defeat_dialogue_index = 0
        self.show_defeat_dialogue = False  # Flag to track if defeat dialogue should be shown

        # music setup
        self.play_music(self.battle_theme) # Start playing the battle theme music


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
        self.play_music(self.title_theme) # Start playing the title theme music

        # Draws a semi-transparent overlay to dim the background
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
        overlay.fill((self.settings.title_overlay))
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
        self.screen.fill(self.settings.black)
        self.draw_text('Credits', self.settings.white, self.settings.credits_title_x, self.settings.credits_title_y) # title
        self.draw_text(
        'Dream Mix \n'
        'Prinbles \n'
        'JDSherbert, AnthonyTTurtlez \n'
        'saukgp \n'
        'Rem Chronicle \n'
        'russ123 \n'
        'Tiny Worlds \n'
        'Mounir Tohami \n'
        'vibrato08', self.settings.white, self.settings.credits_text_x, self.settings.credits_text_y
        ) # Owners of some of the assets I used
        
        if self.return_title.draw(self.screen): # returns to main menu when clicked
            self.game_state = 'main_menu'
    
    def _battle_screen(self):
        """Renders the battle screen with the player and enemy characters, health bars, and combat interface."""
        # Draws battle background and characters
        self.draw_bg()
        self.draw_character()

        if not self.show_dialogue and not self.show_dialogue_midpoint:
            # If dialogue is not being shown, draw the battle interface
            self.draw_user_interface()

        # Draws the dialogue box if it is set to be shown
        if self.show_dialogue and self.dialogue:
            self.dialogue.draw_dialogue(self.screen, self.dialogue_text[self.dialogue_index])
        
        # If the dialogue is at the midpoint, show the midpoint dialogue
        if self.demon_1.hp <= self.demon_1.max_hp * self.settings.hp_threshold and not self.show_dialogue_midpoint and not self.midpoint_shown:
            self.dialogue_midpoint_index = 0  # Reset the midpoint dialogue index
            self.show_dialogue_midpoint = True  # Show the midpoint dialogue
            self.midpoint_shown = True # prevents showing the midpoint dialogue again
        
        # Check if the dialogue midpoint should be shown
        if self.show_dialogue_midpoint and self.dialogue_midpoint:
            self.dialogue_midpoint.draw_dialogue(self.screen, self.dialogue_midpoint_text[self.dialogue_midpoint_index])
            return  # Prevents drawing the rest of the UI while dialogue is up

        # Draws the active damage texts above the enemy
        self.draw_damage_texts()

        # Draws the action display text if it is set to be shown
        if self.action_display_text and pygame.time.get_ticks() - self.action_display_start < self.action_display_time:
            self.draw_action_display()

    def _post_battle_screen(self):
        """Handles the post-battle screen after the player has won or lost."""
        self.draw_bg()
        # Draw characters and their animations even if the battle is over
        self.draw_character() # Draws the player and enemy characters

        # --- post-battle dialogue handling ---
        if self.show_victory_dialogue and self.victory_dialogue:
            # Draws the victory dialogue if it is set to be shown
            self.victory_dialogue.draw_dialogue(self.screen, self.victory_dialogue_text[self.victory_dialogue_index])
            return
        if self.show_defeat_dialogue and self.defeat_dialogue:
            # Draws the defeat dialogue if it is set to be shown
            self.defeat_dialogue.draw_dialogue(self.screen, self.defeat_dialogue_text[self.defeat_dialogue_index])
            return
        
        self.draw_user_interface() # Draws the user interface elements on the battle screen

        if not self.fighter.is_alive:
            self.draw_overlay() # Draws a semi-transparent overlay to dim the background when game is over

            # Draws the game over image and text
            self.screen.blit(asset.defeat_img, self.settings.game_over_pos)
            self.draw_post_battle_texts()
        elif not self.demon_1.is_alive:
            # If the player has won, show victory text
            self.draw_overlay() # Draws a semi-transparent overlay to dim the background when game is over

            # Draws the game over image and text
            self.screen.blit(asset.victory_img, self.settings.game_over_pos)
            self.draw_post_battle_texts()
            

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
                    self.set_action_display("Attack!") # display action text for enemy attack
                    # Show damage text above the player
                    self.add_damage_text(f"-{damage}", self.fighter.rect.centerx, self.fighter.rect.y, self.settings.red)

    # --- Helper methods ---
    def draw_bg(self):
        self.screen.blit(asset.battle_bg, (0, 0))
    
    def draw_title_screen(self):
        self.screen.blit(asset.title_img, (0, 0))
    
    def draw_overlay(self):
        """Draws a semi-transparent overlay to dim the background when game is over."""
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
        overlay.fill(self.settings.bg_overlay)
        self.screen.blit(overlay, (0, 0)) # Add a semi-transparent overlay
    
    def draw_frame(self):
        self.screen.blit(asset.icon_frame, (self.settings.icon_frame_x, self.settings.icon_frame_y))
    
    def draw_portrait(self):
        self.screen.blit(asset.actor1_icon, (self.settings.player_icon_x, self.settings.player_icon_y))
    
    def draw_keys(self):
        """Draws all command image."""
        spacing = self.settings.keys_spacing
        x, y = self.settings.keys_icon_x, self.settings.keys_icon_y
        self.screen.blit(asset.key_a_icon, (x, y))
        self.screen.blit(asset.key_s_icon, (x + spacing, y))
        self.screen.blit(asset.key_d_icon, (x + 2 * spacing, y))
        self.screen.blit(asset.key_f_icon, (x + 3 * spacing, y))
    
    def draw_text(self, text, text_color, x, y):
        """General method to draw text."""
        img = self.settings.font.render(text, True, text_color)
        self.screen.blit(img, (x, y))
    
    def draw_damage_texts(self):
        """Draws all active damage texts on the screen."""
        self.damage_texts = [dt for dt in self.damage_texts if dt.is_alive() and not dt.draw(self.screen)]
    
    def add_damage_text(self, text, x, y, color):
        """Adds a floating damage text to the screen."""
        self.damage_texts.append(
            DamageText(text, x, y, color, self.settings.font, self.settings.text_duration))
        
    def draw_post_battle_texts(self):
        self.draw_text('return to main menu', self.settings.white, *self.settings.game_over_text_pos)
    
    def draw_action_display(self):
        """Draws the image for the action"""
        text_img = self.settings.font.render(self.action_display_text, True, self.settings.white)
        text_rect = text_img.get_rect(center=(self.settings.screen_width // 2, self.settings.text_rect_height))
        # Draws a semi-transparent overlay behind the action display text
        padding = self.settings.text_padding
        # Calculate the size of the overlay based on the text size
        overlay_width, overlay_height = self.settings.screen_width + padding, text_rect.height + padding // 2
        # center the overlay on the text
        overlay_x, overlay_y = text_rect.centerx - overlay_width // 2, text_rect.centery - overlay_height // 2
        overlay_surface = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
        overlay_surface.fill(self.settings.bg_overlay)
        # blit the overlay surface
        self.screen.blit(overlay_surface, (overlay_x, overlay_y))
        self.screen.blit(text_img, text_rect)
    
    def set_action_display(self, text):
        """Displays the name of the action when performed."""
        self.action_display_text = text
        self.action_display_time = self.settings.action_display_duration  # Set the duration for which the action display text is shown
        self.action_display_start = pygame.time.get_ticks()  # Start the action display timer
    
    def draw_character(self):
        """Centralized method to draw all character components."""
        # Draws the player character
        self.fighter.update()
        self.fighter.draw()
        # Draws the enemy character
        self.demon_1.update()
        self.demon_1.draw()
    
    def draw_user_interface(self):
        """Centralized method to draw all UI components."""
        white = self.settings.white
        keys_width, keys_height = self.settings.keys_width, self.settings.keys_height
        spacing = self.settings.keys_spacing
        hp_x, hp_y = self.settings.hp_x, self.settings.hp_y
        player_name_x, player_name_y = self.settings.player_name_x, self.settings.player_name_y
        # Draws the user interface elements on the battle screen.
        self.draw_frame()
        self.draw_portrait()
        self.draw_keys()
        self.draw_text('Attack', white, keys_width, keys_height)
        self.draw_text('End Turn', white, keys_width + spacing, keys_height)
        self.draw_text('Guard', white, keys_width + 2 * spacing, keys_height)
        self.draw_text('Heal', white, keys_width + 3 * spacing, keys_height)
        # Draws the player's health and name
        self.draw_text(f'HP: {self.fighter.hp}', white, hp_x, hp_y)
        self.draw_text(f'{self.fighter.name}', white, player_name_x, player_name_y)
        self.fighter_health_bar.draw(self.fighter.hp)
        # Draws the enemy's health and name
        self.draw_text(f'{self.demon_1.name}', self.settings.red, self.demon_1_health_bar.x, self.demon_1_health_bar.y - self.settings.demon_name_offset_y)
        self.demon_1_health_bar.draw(self.demon_1.hp)
    
    def play_music(self, music, loop=-1):
        """Plays the specified music track."""
        if self.current_music != music:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(loop)
            self.current_music = music  # Update current music to the new track

    def _check_events(self):
        """Processes all events in the game loop."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = 'exit'  # Exit the game
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
    
    def _advance_dialogue(self, event, flag_name, index_name, text_list):
        """Advances the dialogue based on key events."""
        if getattr(self, flag_name) and getattr(self, index_name) is not None:
            if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                # If the dialogue is being shown, advance to the next line
                setattr(self, index_name, getattr(self, index_name) + 1)
                if getattr(self, index_name) >= len(getattr(self, text_list)):
                    # If the index exceeds the text list length, hide the dialogue
                    setattr(self, flag_name, False)
            return True
        return False

    def _check_keydown_events(self, event):
        """Handles keydown events for the game."""
        # --- Dialogue Input Handling ---
        if self._advance_dialogue(event, 'show_dialogue', 'dialogue_index', 'dialogue_text'): return
        if self._advance_dialogue(event, 'show_dialogue_midpoint', 'dialogue_midpoint_index', 'dialogue_midpoint_text'): return
        if self._advance_dialogue(event, 'show_victory_dialogue', 'victory_dialogue_index', 'victory_dialogue_text'): return
        if self._advance_dialogue(event, 'show_defeat_dialogue', 'defeat_dialogue_index', 'defeat_dialogue_text'): return
        
        # --- General Input Commands ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                self._handle_fullscreen_toggle()
            elif event.key == pygame.K_ESCAPE:
                self._handle_escape()
            elif self.game_state == 'battle': # Check for key presses only in battle state
                self._handle_battle_keys(event) 

    def _handle_fullscreen_toggle(self):
        """Toggles fullscreen mode."""
        if not self.fullscreen:
            pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.FULLSCREEN)
            self.fullscreen = True # trigeer fullscreen
        else:
            pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
            self.fullscreen = False # return to windowed mode
    
    def _handle_escape(self):
        """Allows the user to return to main menu from any game state."""
        if self.game_state in ['battle', 'credits', 'post_battle']:
            self.game_state = 'main_menu' # return to main menu
    
    def _handle_battle_keys(self, event):
        """Handles key commands in battle screen."""
        if self.combat and self.combat.is_player_turn():
            # Check for player actions based on key presses
            # Player can attack, pass turn, or guard
            if event.key == self.settings.key_attack:
                damage = self.combat.player_attack()
                if damage is not None:
                    # Show damage text above the enemy
                    self.add_damage_text(f"-{damage}", self.demon_1.rect.centerx, self.demon_1.rect.y, self.settings.red)
                    self.set_action_display("Slash!") # display action text for player attack
            elif event.key == self.settings.key_pass:
                self.combat.player_pass()
                self.set_action_display("Pass Turn!")
            elif event.key == self.settings.key_guard:
                guard = self.combat.player_guard()
                if guard is not None:
                    # Show guard text above the player
                    self.add_damage_text("Increased Defense!", self.fighter.rect.centerx - self.settings.guard_text_offset_x, self.fighter.rect.y, self.settings.white)
                    self.set_action_display("Guard!")
            elif event.key == self.settings.key_heal:
                healed = self.combat.player_heal(self.settings.heal_amount)     
                if healed is not None:
                    # Show healing text above the player
                    self.add_damage_text(f"+{healed}", self.fighter.rect.centerx, self.fighter.rect.y, self.settings.green)
                    self.set_action_display("Warcry!")


if __name__ == '__main__':
    CRD_game = Game()
    CRD_game.run_game()