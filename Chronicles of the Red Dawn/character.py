import pygame

class Character():
    def __init__(self, name, hp, strength, defense):
        """Basic Attributes"""
        self.name = name
        self.hp = hp #current hp
        self.max_hp = hp #maximum hit points
        self.strength = strength
        self.defense = defense
        self.is_alive = True

class Fighter(Character):
    def __init__(self, x, y, name):
        super().__init__(name, hp = 100, strength = 60, defense = 20)
        #-------------------------------------
        #               Animations
        #-------------------------------------
        """Master List to store all actions"""
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 # 0 - idle, 1 - attack, 2 - hurt, 3 - dead, 4 - dying
        self.update_time = pygame.time.get_ticks()
        """Idle Animation"""
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/battlers/Brand/Idle/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 2.5, img.get_height() * 2.5))
            img = pygame.transform.flip(img, flip_x= 180, flip_y= 0)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        """Attack Animation"""
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/battlers/Brand/Attack/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 2.5, img.get_height() * 2.5))
            img = pygame.transform.flip(img, flip_x= 180, flip_y= 0)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        """Hurt Animation"""
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/battlers/Brand/Hurt/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 2.5, img.get_height() * 2.5))
            img = pygame.transform.flip(img, flip_x= 180, flip_y= 0)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        """Death Animation"""
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/battlers/Brand/Dead/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 2.5, img.get_height() * 2.5))
            img = pygame.transform.flip(img, flip_x= 180, flip_y= 0)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        """Low HP Animation"""
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/battlers/Brand/Dying/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 2.5, img.get_height() * 2.5))
            img = pygame.transform.flip(img, flip_x= 180, flip_y= 0)
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #"""Victory Animation"""
        #temp_list = []
        #for i in range(4):
        #    img = pygame.image.load(f'img/battlers/Brand/Victory/{i}.png').convert_alpha()
        #    img = pygame.transform.scale(img, (img.get_width() * 2.5, img.get_height() * 2.5))
        #    img = pygame.transform.flip(img, flip_x= 180, flip_y= 0)
        #    temp_list.append(img)
        #self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.screen = pygame.display.get_surface()

    def update(self):
        #frame goes faster the lower the cooldown goes
        animation_cooldown = 150
        #updates animation frames
        self.image = self.animation_list[self.action][self.frame_index]
        #checks if enough time has passed before it plays the next frame
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #resets the animtion if there's no next image
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3: #death animation stays on last frame
                self.frame_index = len(self.animation_list[self.action]) - 1
            elif self.action == 4 and self.hp > self.max_hp*0.4:
                self.idle()
            elif self.action != 4:
                self.idle()
            #checks for hp threshold to trigger low hp animation
            if self.hp <= self.max_hp*0.4 and self.action != 3 and self.action != 5: #avoid playing when character is dead
                self.low_health()

    def idle(self):
        #sets variable to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def attack(self, target):
        #damage calculation
        self.damage = self.strength - target.defense
        target.hp -= self.damage
        target.hurt()
        if target.hp <= 0:
            target.hp = 0
            target.is_alive = False
            target.death()
            #self.victory()
        #sets variable to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def low_health(self):
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    #def victory(self):
    #    self.action = 5
    #    self.frame_index = 0
    #    self.update_time = pygame.time.get_ticks()

    def draw(self):
        self.screen.blit(self.image, self.rect)