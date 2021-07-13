import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, aiGame):
        """Initialize scorekeeping attributes"""
        self.aiGame = aiGame
        self.screen = aiGame.screen
        self.screenRect = self.screen.get_rect()
        self.settings = aiGame.settings
        self.stats = aiGame.stats
        self.prepShips()

        # Font settings for scoring information
        self.textColour = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the intial score image
        self.prepScore()
        self.prepHighScore()
        self.prepLevel()

    def prepScore(self):
        """Turn the score into a rendered image"""
        scoreStr = str(self.stats.score)
        self.scoreImage = self.font.render(scoreStr, True, self.textColour, self.settings.bgColour)

        # Display the score at the top right of the screen
        self.scoreRect = self.scoreImage.get_rect()
        self.scoreRect.right = self.screenRect.right - 20
        self.scoreRect.top = 20
        
    def prepHighScore(self):
        highScore = round(self.stats.highScore - 1)
        highScoreStr = "{:,}".format(highScore)
        self.highScoreImage = self.font.render(highScoreStr, True, self.textColour, self.settings.bgColour)

        # Center the high score at the top of the screen
        self.highScoreRect = self.highScoreImage.get_rect()
        self.highScoreRect.centerx = self.screenRect.centerx
        self.highScoreRect.top = self.scoreRect.top

    def checkHighScore(self):
        """Check to see if there's a new high score"""
        if self.stats.score > self.stats.highScore:
            self.stats.highScore = self.stats.score
            self.prepHighScore()

    def prepLevel(self):
        """Turn the level into a rendered image"""
        levelStr = str(self.stats.level)
        self.levelImage = self.font.render(levelStr, True, self.textColour, self.settings.bgColour)

        # Position the level below the score
        self.levelRect = self.levelImage.get_rect()
        self.levelRect.right = self.scoreRect.right
        self.levelRect.top = self.scoreRect.bottom + 10

    def prepShips(self):
        """Show how many ships are left"""
        self.ships = Group()
        for shipNumber in range(self.stats.shipsLeft):
            ship = Ship(self.aiGame)
            ship.rect.x = 10 + shipNumber * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def showScore(self):
        """Draw scores, level and ships to the screen"""
        self.screen.blit(self.scoreImage, self.scoreRect)
        self.screen.blit(self.highScoreImage, self.highScoreRect)
        self.screen.blit(self.levelImage, self.levelRect)
        self.ships.draw(self.screen)