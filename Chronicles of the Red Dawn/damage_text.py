import time

class DamageText:
    def __init__(self, text, x, y, color, font, duration):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font = font
        self.start_time = time.time()
        self.duration = duration
    
    def is_alive(self):
        """Check if the damage text is still alive based on its duration."""
        return (time.time() - self.start_time) < self.duration
    
    def draw(self, screen):
        """Draw the damage text on the screen."""
        img = self.font.render(self.text, True, self.color)
        screen.blit(img, (self.x, self.y))