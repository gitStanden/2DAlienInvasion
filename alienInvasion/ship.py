import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, aiGame):
        """Initilise the ship and set its starting position."""
        super().__init__()
        self.screen = aiGame.screen
        self.screenRect = aiGame.screen.get_rect()
        self.settings = aiGame.settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load("Images/playership.bmp")
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screenRect.midbottom
    
        # Store a devimal vlaue for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement Flag
        self.movingRight = False
        self.movingLeft = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect.
        if self.movingRight and self.rect.right < self.screenRect.right:
            self.x += self.settings.shipSpeed
        if self.movingLeft and self.rect.left > 0:
            self.x -= self.settings.shipSpeed

        # Update rect object from self.x
        self.rect.x = self.x

    def centerShip(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screenRect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)