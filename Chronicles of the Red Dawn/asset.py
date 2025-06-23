import pygame
import settings

setting = settings.Settings()
pygame.display.init()
display = pygame.display.set_mode((setting.screen_width, setting.screen_height))
"""colors"""
red = (220, 20, 60)
green = (139, 190, 27)
white = (240,255,255)
#-------------------------------------
#           Image Database
#-------------------------------------
"""Background"""
title_img = pygame.image.load('Chronicles of the Red Dawn/img/bg_screen/Title_Screen.png').convert_alpha()
battle_bg = pygame.image.load('Chronicles of the Red Dawn/img/bg_screen/dawn.png').convert_alpha()
battle_bg = pygame.transform.scale(battle_bg, 
                                   (battle_bg.get_width() * 0.7, battle_bg.get_height() * 0.68))
"""Battle UI"""
icon_frame = pygame.image.load('Chronicles of the Red Dawn/img/battle_interface/icon border.png').convert_alpha()
icon_frame = pygame.transform.scale(icon_frame, 
                                    (icon_frame.get_width() * 2, icon_frame.get_height() * 2))
actor1_icon = pygame.image.load('Chronicles of the Red Dawn/img/battle_interface/brand_icon.png').convert_alpha()
actor1_icon = pygame.transform.scale(actor1_icon, 
                                    (actor1_icon.get_width() * 1.5, actor1_icon.get_height() * 1.5))
key_a_icon = pygame.image.load('Chronicles of the Red Dawn/img/battle_interface/key_a_icon.png').convert_alpha()
key_a_icon = pygame.transform.scale(key_a_icon, 
                                    (key_a_icon.get_width() * 3, key_a_icon.get_height() * 3))
key_s_icon = pygame.image.load('Chronicles of the Red Dawn/img/battle_interface/key_s_icon.png').convert_alpha()
key_s_icon = pygame.transform.scale(key_s_icon, 
                                    (key_s_icon.get_width() * 3, key_s_icon.get_height() * 3))
"""Battle State"""
defeat_img = pygame.image.load('Chronicles of the Red Dawn/img/battle_interface/Defeat.png').convert_alpha()
defeat_img = pygame.transform.scale(defeat_img,
                                    (defeat_img.get_width() * 2, defeat_img.get_height() * 2))
"""Buttons"""
play_img = pygame.image.load('Chronicles of the Red Dawn/img/buttons/Play.png').convert_alpha()
exit_img = pygame.image.load('Chronicles of the Red Dawn/img/buttons/Exit.png').convert_alpha()
credits_img = pygame.image.load('Chronicles of the Red Dawn/img/buttons/Credits.png').convert_alpha()
return_img = pygame.image.load('Chronicles of the Red Dawn/img/buttons/Home.png').convert_alpha()