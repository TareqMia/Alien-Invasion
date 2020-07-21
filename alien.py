import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Class to represent single alien in a fleet"""
    def __init__(self, ai_settings, screen):
        """Iniitalize aliend and set its starting point"""
        super(Alien, self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        
        # load alien sprite and set its rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        # start each alien near top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # store alien's exact location
        self.x = float(self.rect.x)
        
    def blitme(self):
        """Draw alien at current postion"""
        self.screen.blit(self.image, self.rect) 
        
    def update(self):
        """Move alien to the right or left"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        
    def check_edges(self):
        """Returns a boolean if an alien has hit the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right > screen_rect.right:
            return True
        elif self.rect.left < 0:
            return True
        
    
        
