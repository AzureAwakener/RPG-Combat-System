import pygame

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, ((width * scale), (height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        # check for mouse hover and click
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        # return to false when not clicked or released after a click
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        # draw button to screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action