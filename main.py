import pygame
import random
import button

pygame.init()

#---caps the game frame rate to 60---
clock = pygame.time.Clock()
fps = 60

#---game music---
pygame.mixer.music.load('Untitled_Game/ost/Cracked Heart.wav')
pygame.mixer.music.play(loops=-1)

#sound effects
male_attack = pygame.mixer.Sound('Untitled_Game/ost/actor_grunt.wav')
sword_slash = pygame.mixer.Sound('Untitled_Game/ost/sword_slash.wav')
longsword_slash = pygame.mixer.Sound('Untitled_Game/ost/longsword_hit.wav')

#---game screen---
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Combat')

#game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 30
clicked = False
game_over = 0

#define font
font = pygame.font.Font('Untitled_Game/font/ThaleahFat.ttf', 26)

#define colors
red = (220, 20, 60)
green = (139, 190, 27)

#---images---
#---combat background---
combat_bg = pygame.image.load('Untitled_Game/img/battle_bg/forest.png').convert_alpha()
#---combat interface---
combat_ui = pygame.image.load('Untitled_Game/img/icons/panel_test.png').convert_alpha()
#---item button---
potion_img = pygame.image.load('Untitled_Game/img/icons/potion.png')
restart_img = pygame.image.load('Untitled_Game/img/icons/restart.png')
#victory/defeat screen
defeat_img = pygame.image.load('Untitled_Game/img/icons/defeat.png')
victory_img = pygame.image.load('Untitled_Game/img/icons/victory.png')
#---combat curson---
sword_img = pygame.image.load('Untitled_Game/img/icons/attack_cursor.png').convert_alpha()

#---function to draw image to screen---
def draw_bg():
    screen.blit(combat_bg, (0, 0))

#draw texts
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

#draw battle ui
def draw_panel():
    #draw ui rectangle
    screen.blit(combat_ui, (0, screen_height - bottom_panel))
    #show character stats
    draw_text(f'{actor_00.name} HP: {actor_00.hp}', font, red, 100, screen_height - bottom_panel + 10)
    #show enemy stats
    for count, i in enumerate(samurai_list):               #y-axis placement            #spacing between each name
        draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 7) + count * 45)

#---character---
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        #Basic Parameters
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        #Master list for all actions
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 # 0=idle 1=attack 3=hurt 4=dead
        self.update_time = pygame.time.get_ticks()
        #Idle
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'Untitled_Game/img/battlers/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.75, img.get_height() *1.75))
            img = pygame.transform.flip(img, flip_x=180, flip_y=0)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Attack
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'Untitled_Game/img/battlers/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.75, img.get_height() *1.75))
            img = pygame.transform.flip(img, flip_x=180, flip_y=0)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Hurt
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'Untitled_Game/img/battlers/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.75, img.get_height() *1.75))
            img = pygame.transform.flip(img, flip_x=180, flip_y=0)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Dead
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'Untitled_Game/img/battlers/{self.name}/Dead/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.75, img.get_height() *1.75))
            img = pygame.transform.flip(img, flip_x=180, flip_y=0)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        animation_cooldown = 200
        #updates animation frames
        self.image = self.animation_list[self.action][self.frame_index]
        #Checks if enough time has passed before it plays the next frame
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #Resets the animation if there's no more frame to play
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        #set variables to attack animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def attack(self, target):
        #deal damage to enemy
        rand = random.randint (-5,5)
        damage = self.strength + rand
        target.hp -= damage
        #triggers hurt animation
        target.hurt()
        #checks if target is alive
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        #set attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        #set hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def death(self):
        #set death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset (self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)

#---playable characters---
actor_00 = Fighter(200, 252, 'actor_00', 3, 30, 3)

class Enemy():
    def __init__(self, x, y, name, max_hp, strength):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.alive = True
        #Master list for all actions
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 # 0=idle 1=attack 3=hurt 4=dead
        self.update_time = pygame.time.get_ticks()
        #Idle
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'Untitled_Game/img/enemies/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.75, img.get_height() *1.75))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Attack
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'Untitled_Game/img/enemies/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.75, img.get_height() *1.75))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Hurt
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'Untitled_Game/img/enemies/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.75, img.get_height() *1.75))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #Dead
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'Untitled_Game/img/enemies/{self.name}/Dead/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.75, img.get_height() *1.75))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        animation_cooldown = 200
        #updates animation frames
        self.image = self.animation_list[self.action][self.frame_index]
        #Checks if enough time has passed before it plays the next frame
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #Resets the animation if there's no more frame to play
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        #set variables to attack animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def attack(self, target):
        #deal damage to enemy
        rand = random.randint (-5,5)
        damage = self.strength + rand
        target.hp -= damage
        #triggers hurt animation
        target.hurt()
        #checks if target is alive
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        #set attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        #set hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def death(self):
        #set death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset (self):
        self.alive = True
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)

#---Enemy List---
samurai_00 = Enemy(500, 255, 'samurai', 2, 9)
samurai_01 = Enemy(700, 255, 'samurai', 2, 9)

samurai_list = []
samurai_list.append(samurai_00)
samurai_list.append(samurai_01)

#hp bar
class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        #current health
        self.hp = hp
        #calculates health ratio
        ratio = self.hp / self.max_hp
        #bottom hp layer to show damage taken
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        #upper hp layer to show max health
        pygame.draw.rect(screen, green, (self.x, self.y, 150*ratio, 20))

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect =self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    def update(self):
        #move damage text up
        self.rect.y -= 1
        #delete text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()

damage_text_group = pygame.sprite.Group()

actor_00_healthbar = HealthBar(100, screen_height - bottom_panel + 40, actor_00.hp, actor_00.max_hp)
samurai_00_healtbar = HealthBar(550, screen_height - bottom_panel + 30, samurai_00.hp, samurai_00.max_hp)
samurai_01_healtbar = HealthBar(550, screen_height - bottom_panel + 75, samurai_01.hp, samurai_01.max_hp)

#create buttons
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

#---while loop to keep the game running---
running = True
while running: 
    #---game fps---
    clock.tick(fps)

    #---draw the bg from draw_bg() function---
    draw_bg()

    #---draw combat ui---
    draw_panel()
    actor_00_healthbar.draw(actor_00.hp)
    samurai_00_healtbar.draw(samurai_00.hp)
    samurai_01_healtbar.draw(samurai_01.hp)

    #---draw combatants---
    actor_00.update()
    actor_00.draw()

    #---draw enemies---
    for samurai in samurai_list:
        samurai.update()
        samurai.draw()

    #draw damage text
    damage_text_group.update()
    damage_text_group.draw(screen)

    #control player actions
    #reset action variables
    attack = False
    potion = False
    target = None
    #mouse visibility
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, samurai in enumerate(samurai_list):
        if samurai.rect.collidepoint(pos):
            #hide mouse
            pygame.mouse.set_visible(False)
            #show the sword icon in place
            screen.blit(sword_img, pos)
            if clicked == True and samurai.alive == True:
                attack = True
                target = samurai_list[count]
    if potion_button.draw():
        potion = True
    #show potion capacity
    draw_text(str(actor_00.potions), font, red, 150, screen_height - bottom_panel + 70)

    if game_over == 0:
        #player action
        if actor_00.alive == True:
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #look for player action
                    #attack
                    if attack == True and target != None:
                        actor_00.attack(target)
                        pygame.mixer.Sound.play(male_attack)
                        pygame.mixer.Sound.play(sword_slash)
                        current_fighter += 1
                        action_cooldown = 0
                    #potion
                    if potion == True:
                        if actor_00.potions > 0:
                            #check if potion will go beyond max health
                            if actor_00.max_hp - actor_00.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = actor_00.max_hp - actor_00.hp
                            actor_00.hp += heal_amount
                            actor_00.potions -= 1
                            damage_text = DamageText(actor_00.rect.centerx, actor_00.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
        else:
            game_over = -1

        #enemy action
        for count, samurai in enumerate(samurai_list):
            if current_fighter == 2 + count:
                if samurai.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        #attack
                        samurai.attack(actor_00)
                        pygame.mixer.Sound.play(male_attack)
                        pygame.mixer.Sound.play(longsword_slash)
                        current_fighter += 1
                        action_cooldown = 0
                else:
                    current_fighter += 1
        
        #reset after everyone takes a turn
        if current_fighter > total_fighters:
            current_fighter = 1

    #checks if enemies are alive
    enemy_alive = 0
    for samurai in samurai_list:
        if samurai.alive == True:
            enemy_alive += 1
    if enemy_alive == 0:
        game_over = 1

    #checks for game over
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))
        if game_over == -1:
            screen.blit(defeat_img, (290, 50))
        if restart_button.draw():
            actor_00.reset()
            for samurai in samurai_list:
                samurai.reset()
            current_fighter = 1
            action_cooldown
            game_over = 0

    #---used to quit the game instance---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False
    
    #---refresh the screen/fps---
    pygame.display.update()

pygame.quit()