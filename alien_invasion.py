import sys
import pygame
from settings import Settings
from time import sleep
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """overall class to manage game behvaiour and assets"""
    def __init__(self):
        """intialize the game and create game resources"""
        pygame.init()
        self.settings=Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))        
        pygame.display.set_caption("Alien Invasion")
        self.clock = pygame.time.Clock()
        # Create an instance to store game statistics. 
        self.stats = GameStats(self) 
        #create scoreboard instance
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()  #create a fleet of aliens
        # Start Alien Invasion in an inactive state. 
        self.game_active = False
        # Make the Play button. 
        self.play_button = Button(self, "Play")
    
    def run_game(self):
        """start the main loop of game"""
        while True:
            """look for keyboard or mouse events"""
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._bullet_update() 
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)        #loop will run 60 times per second

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)    #redraw screen everytime we pass thriugh loop
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.ship.blitme()
        self.sb.show_score()
        # Draw the play button if the game is inactive. 
        if not self.game_active: 
            self.play_button.draw_button()
        pygame.display.flip()      #make the recently drawn screen visible


    def _check_aliens_bottom(self): 
        """Check if any aliens have reached the bottom of the screen.""" 
        for alien in self.aliens.sprites(): 
            if alien.rect.bottom >= self.settings.screen_height: 
                # Treat this the same as if the ship got hit. 
                self._ship_hit() 
                break

    def _ship_hit(self): 
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0: 
            # Decrement ships_left. 
            self.stats.ships_left -= 1 
            # Get rid of any remaining bullets and aliens. 
            self.bullets.empty() 
            self.aliens.empty() 
            # Create a new fleet and center the ship. 
            self._create_fleet() 
            self.ship.center_ship() 
            # Pause. 
            sleep(0.5)
            self.stats.ships_left -= 1
            self.sb.prep_ships()
        else:
            self.game_active = False

    def _check_fleet_edges(self): 
        """Respond appropriately if any aliens have reached an edge.""" 
        for alien in self.aliens.sprites(): 
            if alien.check_edges(): 
                self._change_fleet_direction() 
                break 

    def _change_fleet_direction(self): 
        """Drop the entire fleet and change the fleet's direction.""" 
        for alien in self.aliens.sprites(): 
            alien.rect.y += self.settings.alien_drop_speed 
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """update the position of aliens"""
        self._check_fleet_edges()
        self.aliens.update()
        #check for collision between ship and aliens
        if pygame.sprite.spritecollideany(self.ship, self.aliens): 
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen. 
        self._check_aliens_bottom()

    def _create_fleet(self):
        """ceate a fleet of aliens"""
        alien = Alien(self)
        #create an alien and keep adding aliens
        #space between 2 aliens is one alien width
        alien_width,alien_height = alien.rect.size
        current_y = alien_height
        current_x = alien_width
        while current_y <  (self.settings.screen_height - 3*alien_height) :
            while current_x < (self.settings.screen_width - 2 * alien_width): 
                self._create_alien(current_x,current_y) 
                current_x += 2*alien_width
            current_x = alien_width
            current_y += 2*alien_height           
        
    def _create_alien(self, x_position,y_position): 
        """Create an alien and place it in the row.""" 
        new_alien = Alien(self) 
        new_alien.x = x_position 
        new_alien.rect.x = x_position 
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _bullet_update(self):
        """update the position of bullets and delete old bullets"""
        self.bullets.update()
        for bullet in self.bullets.copy(): 
            if bullet.rect.bottom <= 0: 
                self.bullets.remove(bullet) 
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self): 
        """Respond to bullet-alien collisions.""" 
        # Remove any bullets and aliens that have collided. 
        collisions = pygame.sprite.groupcollide( self.bullets, self.aliens, True, True) 
        if collisions: 
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points*len(alien)
                self.sb.prep_score() 
                self.sb.check_high_score() 
        if not self.aliens: 
            # Destroy existing bullets and create new fleet. 
            self.bullets.empty() 
            self._create_fleet()
            self.settings.increase_speed()
            #increase level
            self.stats.level +=1
            self.sb.prep_level()
    
    def _check_events(self): 
        """Respond to keypresses and mouse events.""" 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.KEYDOWN: 
                self._check_keydown_events(event) 
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                mouse_pos = pygame.mouse.get_pos() 
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos): 
        """Start a new game when the player clicks Play.""" 
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:            # Reset the game statistics. 
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats() 
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True 
            # Get rid of any remaining bullets and aliens. 
            self.bullets.empty() 
            self.aliens.empty() 
            # Create a new fleet and center the ship. 
            self._create_fleet() 
            self.ship.center_ship()
            # Hide the mouse cursor. 
            pygame.mouse.set_visible(False)
        else:
            self.game_active=True
            pygame.mouse.set_visible(True)


    def _check_keydown_events(self,event):
        """respond to key press"""
        if event.key == pygame.K_RIGHT: 
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT: 
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """firing bullets"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        
    def _check_keyup_events(self,event):
        """respond to key release"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT: 
            self.ship.moving_left = False


if __name__ =="__main__":
    ai = AlienInvasion()
    ai.run_game()