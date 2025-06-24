import pygame

class Dialogue:
    """Class to handle dialogue display and interaction in the game."""
    def __init__(self, screen_width, screen_height, text_color, font):
        #  Initialize dialogue box dimensions and properties
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.box_color = (0, 0, 0, 150) # Semi-transparent black
        self.text_color = text_color
        self.font = font
    
    def draw_dialogue(self, screen, text):
        # Draws the dialogue box
        box_rect = pygame.Rect(100, self.screen_height - 550, self.screen_width - 200, 100) # Positioned at the top of the screen
        dialogue_surface = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
        dialogue_surface.fill(self.box_color)
        # Draw the text
        rendered_text = self.font.render(text, True, self.text_color)
        dialogue_surface.blit(rendered_text, (20, 30))
        # Blit the dialogue surface onto the screen
        screen.blit(dialogue_surface, (box_rect.x, box_rect.y))