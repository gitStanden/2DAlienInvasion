import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, aiGame):
        super().__init__()
        self.screen = aiGame.screen
        self.settings = aiGame.settings

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load("Images/alien.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def checkEdges(self):
        """Return True if alien is at edge of screen."""
        screenRect = self.screen.get_rect()

        if self.rect.right >= screenRect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien to the right."""
        self.x += (self.settings.alienSpeed * self.settings.fleetDirection)
        self.rect.x = self.x