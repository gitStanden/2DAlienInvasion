class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialise the game's static settings."""
        # Screen settings
        self.screenWidth = 1250
        self.screenHeight = 900
        self.bgColour = (230, 230, 230)

        # Ship Settings
        self.shipSpeed = 1.5
        self.shipLimit = 3

        # Bullet Settings
        self.bulletSpeed = 1.5
        self.bulletWidth = 3
        self.bulletHeight = 15
        self.bulletColour = (60, 60, 60)
        self.bulletsAllowed = 3

        # Alien Settings
        self.alienSpeed = 1.0
        self.fleetDropSpeed = 10
        # fleetDirection of 1 represents right; -1 represents left
        self.fleetDirection = 1

        # How quickly the game speeds up
        self.speedupScale = 1.1
        self.initializeDynamicSettings()

        # How quickly the alien point values increase
        self.scoreScale = 1.5

    def initializeDynamicSettings(self):
        """Initialize settings that change throughout the game"""
        self.shipSpeed = 1.5
        self.bulletSpeed = 3.0
        self.alienSpeed = 1.0

        # fleetDirection of 1 represents right, -1 represents left
        self.fleetDirection = 1

        # Scoring
        self.alienPoints = 50

    def increaseSpeed(self):
        """Increase speed settings and alien point values"""
        self.shipSpeed *= self.speedupScale
        self.bulletSpeed *= self.speedupScale
        self.alienSpeed *= self.speedupScale

        self.alienPoints = int(self.alienPoints * self.scoreScale)