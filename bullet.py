import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """class to manage bullet fired from a ship"""
    def __init__(self,ai_game):
        """to maintain the current position of the ship"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.bullet_color = self.settings.bullet_color
        #create a bullet at 0,0 and then set the current postion
        self.rect= pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop= ai_game.ship.rect.midtop
        #store the ships postion in float
        self.y = float(self.rect.y)

    def update(self):
        """update the position of bullet"""
        self.y -= self.settings.bullet_speed
        #update the position of the rectangle
        self.rect.y = self.y 
    
    def draw_bullet(self):
        """draw the bullet on the screen"""
        pygame.draw.rect(self.screen,self.bullet_color,self.rect)
        