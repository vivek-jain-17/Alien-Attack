import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """handles the fleet of aliens"""
    def __init__(self, ai_game):
        super().__init__()        
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        #load the alien image as a rectangle
        self.image = pygame.image.load('images/alien.bmp').convert_alpha()
        self.rect = self.image.get_rect()

        #start each alien near the top left of the sceen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #calculate the exact horizontal location
        self.x = float(self.rect.x)
    
    def check_edges(self): 
        """Return True if alien is at edge of screen.""" 
        screen_rect = self.screen.get_rect()          
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0) 
    def update(self): 
        """Move the alien right or left.""" 
        self.x += self.settings.alien_speed*self.settings.fleet_direction 
        self.rect.x = self.x
    
    