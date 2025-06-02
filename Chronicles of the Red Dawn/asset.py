import pygame

"""colors"""
red = (220, 20, 60)
green = (139, 190, 27)
white = (240,255,255)
#-------------------------------------
#           Image Database
#-------------------------------------
battle_bg = pygame.image.load('img/battle_bg/dawn.png').convert_alpha()
battle_bg = pygame.transform.scale(battle_bg, 
                                   (battle_bg.get_width() * 0.7, battle_bg.get_height() * 0.68))
icon_frame = pygame.image.load('img/battle_interface/icon border.png')
icon_frame = pygame.transform.scale(icon_frame, 
                                    (icon_frame.get_width() * 2, icon_frame.get_height() * 2))
actor1_icon = pygame.image.load('img/battle_interface/brand_icon.png')
actor1_icon = pygame.transform.scale(actor1_icon, 
                                    (actor1_icon.get_width() * 1.5, actor1_icon.get_height() * 1.5))
play_img = pygame.image.load('img/buttons/Play.png')
exit_img = pygame.image.load('img/buttons/Cross.png')