import pygame
class Settings():
    """Stores all system settings for CRD"""

    def __init__(self):
        pygame.init()
        """System Settings"""
        # game font
        self.font = pygame.font.Font('Chronicles of the Red Dawn/font/ThaleahFat.ttf', 26)
        # system colors
        self.red = (220, 20, 60)
        self.green = (139, 190, 27)
        self.white = (240,255,255)
        self.black = (0, 0, 0)
        # screen overlay
        self.title_overlay = (0, 0, 0, 25)
        self.bg_overlay = (0, 0, 0, 150)
        # screen display
        self.screen_width = 1280
        self.screen_height = 720

        """Key Bindings"""
        self.key_attack = pygame.K_a
        self.key_pass = pygame.K_s
        self.key_guard = pygame.K_d
        self.key_heal = pygame.K_f

        """Credit Screen Settings"""
        self.credits_title_x = 600
        self.credits_title_y = 100 
        self.credits_text_x = 500
        self.credits_text_y = 150

        """Game Interface"""
        # title buttons
        self.button_width = 675
        self.button_height = 300
        self.button_offset_y = 100
        # return buttons
        self.return_btn_x = 625
        self.return_btn_y = 330
        self.return_title_x = 10
        self.return_title_y = 650
        # post-battle images
        self.game_over_pos = (460, 150)
        self.game_over_text_pos = (540, 300)
        # command text  display
        self.keys_width = 150
        self.keys_height = 685
        self.keys_spacing = 200
        # command icon display
        self.keys_icon_x = 100
        self.keys_icon_y = 675
        # player hp text
        self.hp_x = 150
        self.hp_y = 35
        # player name text
        self.player_name_x = 45
        self.player_name_y = 115
        # player icon
        self.icon_frame_x = 50
        self.icon_frame_y = 25
        # player portrait
        self.player_icon_x = 62
        self.player_icon_y = 38
        # player health bar
        self.fighter_healthbar_x = 150
        self.fighter_healthbar_y = 60
        # enemy status
        self.demon_healthbar_width = 150
        self.demon_healthbar_height = 8
        self.demon_healthbar_offset_x = 120
        self.demon_healthbar_offset_y = 20
        self.demon_name_offset_y = 20      

        """Character Settings"""
        # ground 
        self.character_y = 555
        # fighter pos
        self.fighter_x = 300
        # enemy pos
        self.enemy_x = 950

        """Character Stats"""
        # fighter
        self.fighter_hp = 250
        self.fighter_strength = 60
        self.fighter_defense = 24
        # demon
        self.demon_hp = 375
        self.demon_strength = 48
        self.demon_defense = 17

        """Animation Settings"""
        # animation speed
        self.fighter_cooldown = 150
        self.demon_cooldown = 165
        # animation scale
        self.character_scale = 2.5 # scale for character animations

        """Battle Settings"""
        # damage text settings
        self.text_duration = 0.8 # seconds
        # action display settings
        self.action_display_duration = 1000 # milliseconds/1 second
        self.text_rect_height = 200
        self.text_padding = 30
        # guard settings
        self.guard_text_offset_x = 100
        # healing settings
        self.heal_amount = 20 # amount of health restored
        # dialogue settings
        self.hp_threshold = 0.5