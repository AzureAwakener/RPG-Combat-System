import pygame

class Enemy():
    def __init__(self, name, hp, strength, defense):
        """Basic Attributes"""
        self.name = name
        self.hp = hp #current hp
        self.max_hp = hp #maximum hit points
        self.strength = strength
        self.defense = defense
        self.is_alive = True

class Demonic_Samurai(Enemy):
    def __init__(self, x, y, name, character_scale, animation_cooldown):
        super().__init__(name, hp = 200, strength = 48, defense = 10)
    
        #-------------------------------------
        #               Animations
        #-------------------------------------
        """Master List to store all actions"""
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 # 0 - idle, 1 - attack, 2 - hurt, 3 - dead
        self.character_scale = character_scale
        self.animation_cooldown = animation_cooldown #frame goes faster the lower the cooldown goes
        self.update_time = pygame.time.get_ticks()
        """Idle Animation"""
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'Chronicles of the Red Dawn/img/enemies/demonic_samurai/Idle/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * self.character_scale, img.get_height() * self.character_scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        """Attack Animation"""
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'Chronicles of the Red Dawn/img/enemies/demonic_samurai/Attack/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * self.character_scale, img.get_height() * self.character_scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        """Hurt Animation"""
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'Chronicles of the Red Dawn/img/enemies/demonic_samurai/Hurt/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * self.character_scale, img.get_height() * self.character_scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        """Death Animation"""
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'Chronicles of the Red Dawn/img/enemies/demonic_samurai/Dead/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * self.character_scale, img.get_height() * self.character_scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.screen = pygame.display.get_surface()

    def update(self):
        #updates animation frames
        self.image = self.animation_list[self.action][self.frame_index]
        #checks if enough time has passed before it plays the next frame
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #resets the animtion if there's no next image
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        #sets variable to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        #damage calculation
        self.damage = self.strength - target.defense
        target.hp -= self.damage
        target.hurt() # apply hurt animation to target
        if target.hp <= 0:
            target.hp = 0
            target.is_alive = False
            target.death()
        #sets variable to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        return self.damage # damage dealt

    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def draw(self):
        self.screen.blit(self.image, self.rect)