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
        super().__init__(name, hp = 300, strength = 25, defense = 20)

        #-------------------------------------
        #               Animations
        #-------------------------------------
        """Master List to store all actions"""
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 # 0 - idle, 1 - attack, 2 - hurt, 3 - dead
        self.update_time = pygame.time.get_ticks()
        """Idle Animation"""
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/battlers/Brand/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 2.5, img.get_height() * 2.5))
            img = pygame.transform.flip(img, flip_x= 180, flip_y= 0)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.screen = pygame.display.get_surface()

    def update(self):
        #frame goes faster the lower the cooldown goes
        animation_cooldown = 175
        #updates animation frames
        self.image = self.animation_list[self.action][self.frame_index]
        #checks if enough time has passed before it plays the next frame
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
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
    
    def draw(self):
        self.screen.blit(self.image, self.rect)