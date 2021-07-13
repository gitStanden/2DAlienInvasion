class GameStats:
    """Track stats for Alien Invasion."""

    def __init__(self, aiGame):
        """Initialise stats"""
        self.settings = aiGame.settings 
        self.resetStats()
        self.gameActive = False     #Start alien invasion in an active state

        # High score should never be reset
        self.highScore = 0

    def resetStats(self):
        """Initialise stats that can change during the game"""
        self.shipsLeft = self.settings.shipLimit
        self.score = 0
        self.level = 1