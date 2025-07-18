class Settings:
    """store settings of game"""
    def __init__(self):
        """static settings"""
        self.screen_width=1200
        self.screen_height=750
        self.bg_color=(230,230,230)
        #ship settings
        self.ship_limit = 3
        #bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 10
        #alien settings
        self.alien_drop_speed = 13
        # How quickly the game speeds up    
        self.speedup_scale = 1.1 
        self.initialize_dynamic_settings()
        # How quickly the alien point values increase 
        self.score_scale = 1.5
    
    def initialize_dynamic_settings(self): 
        """Initialize settings that change throughout the game.""" 
        self.ship_speed = 1.5 
        self.bullet_speed = 2.5 
        self.alien_speed = 1.0 
        # fleet_direction of 1 represents right; -1 represents left. 
        self.fleet_direction = 1
        # Scoring settings 
        self.alien_points = 50
    
    def increase_speed(self): 
        """Increase speed settings and alien points.""" 
        self.ship_speed *= self.speedup_scale 
        self.bullet_speed *= self.speedup_scale 
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
