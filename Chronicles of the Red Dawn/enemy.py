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
    def __init__(self, x, y, name, character_scale, animation_cooldown, settings):
        self.settings = settings # this line goes first to access settings for super.init()
        super().__init__(name, hp = self.settings.demon_hp, strength = self.settings.demon_strength, defense = self.settings.demon_defense)
        self.character_scale = character_scale
        self.animation_cooldown = animation_cooldown #frame goes faster the lower the cooldown goes
        #-------------------------------------
        #               Animations
        #-------------------------------------
        """Master List to store all actions"""
        self.animation_list = [
            self._load_animation("Idle", 4),
            self._load_animation("Attack", 4),
            self._load_animation("Hurt", 4),
            self._load_animation("Dead", 4),
        ]
        self.frame_index = 0 # first image plays first [0]
        self.action = 0 # 0 - idle, 1 - attack, 2 - hurt, 3 - dead
        self.update_time = pygame.time.get_ticks()

        # sets the initial image and rect for the character
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.screen = pygame.display.get_surface()
    
    def _load_animation(self, action_folder, frame_count):
        """Method to draw animations and return it to temp_list[]."""
        temp_list = []
        for i in range(frame_count):
            img = pygame.image.load(f'Chronicles of the Red Dawn/img/enemies/demonic_samurai/{action_folder}/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * self.character_scale, img.get_height() * self.character_scale))
            temp_list.append(img)
        return temp_list

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
        # sets variable to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # damage calculation
        self.damage = self.strength - target.defense
        target.hp -= self.damage
        target.hurt() # apply hurt animation to target
        if target.hp <= 0:
            target.hp = 0
            target.is_alive = False
            target.death() # play death animation if target dies
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