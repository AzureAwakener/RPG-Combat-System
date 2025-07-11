import pygame

class Character():
    def __init__(self, name, hp, strength, defense):
        """Basic Attributes."""
        self.name = name
        self.hp = hp #current hp
        self.max_hp = hp #maximum hit points
        self.strength = strength
        self.defense = defense
        self.base_defense = defense # base defense value for the character
        self.is_alive = True

class Fighter(Character):
    def __init__(self, x, y, name, character_scale, animation_cooldown, settings):
        self.settings = settings # this line goes first to access settings for super.init()
        super().__init__(name, hp = self.settings.fighter_hp, strength= self.settings.fighter_strength, defense = self.settings.fighter_defense)
        self.character_scale = character_scale
        self.animation_cooldown = animation_cooldown # frame goes faster the lower the cooldown goes
        #-------------------------------------
        #               Animations
        #-------------------------------------
        """Master List to store all actions"""
        self.animation_list = [
            self._load_animation("Idle", 4),
            self._load_animation("Attack", 4),
            self._load_animation("Hurt", 4),
            self._load_animation("Guard", 4),
            self._load_animation("Heal", 4),
            self._load_animation("Dead", 4),
            self._load_animation("Dying", 4),
        ]
        self.frame_index = 0 #first image plays first [0]
        self.action = 0 # 0 = idle, 1 = attack, 2 = hurt, 3 = guard, 4 = heal, 5 = dead, 6 = dying
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
            img = pygame.image.load(f'Chronicles of the Red Dawn/img/battlers/Brand/{action_folder}/{i}.png').convert_alpha()
            img = pygame.transform.flip(img, flip_x=180, flip_y=0)
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
        
        frames = len(self.animation_list[self.action])
        #resets the animtion if there's no next image
        if self.frame_index >= frames:
            if self.action in [3, 5]: # Stays on last frame for guard and death animations
                self.frame_index = frames - 1
            # checks for hp threshold to trigger low hp animation
            elif self.hp <= self.max_hp*0.4 and self.action != 5: #avoid playing when character is dead
                self.low_health()
            elif self.action == 6 and self.hp > self.max_hp*0.4: # if low health animation is playing and hp is above threshold, reset to idle
                self.idle()
            else:
                self.idle() # reset to idle

    def idle(self):
        # sets variable to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def attack(self, target):
        # damage calculation
        self.damage = self.strength - target.defense
        target.hp -= self.damage
        target.hurt()
        if target.hp <= 0:
            target.hp = 0
            target.is_alive = False
            target.death() # play death animation if target dies
        # sets variable to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        return self.damage # amount of damage dealt
    
    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def guard(self):
        self.defense = round(self.defense * 1.5) # Increase defense by 50%
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def heal(self, amount):
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
        # Restore health
        old_hp = self.hp
        self.hp += amount
        if self.hp > self.max_hp: # cap health at max
            self.hp = self.max_hp
        return self.hp - old_hp # amount of health healed
    
    def death(self):
        self.action = 5
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def low_health(self):
        self.action = 6
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        self.screen.blit(self.image, self.rect)