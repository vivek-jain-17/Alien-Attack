class GameStats: 
    """Track statistics for Alien Invasion.""" 
    def __init__(self, ai_game): 
        """Initialize statistics.""" 
        self.settings = ai_game.settings 
        # High score should never be reset. 
        self.high_score = 0
        self.reset_stats() 
    def reset_stats(self): 
        """Initialize statistics that can change during the game.""" 
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1 