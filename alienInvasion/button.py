import pygame.font

class Button:
    def __init__(self, aiGame, msg):
        """Initialise button attributes."""
        self.screen = aiGame.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimension and properties of the button
        self.width, self.height = 200, 50
        self.buttonColour = (0, 255, 0)
        self.textColour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The Button message needs to be prepped only once
        self._prepMsg(msg)

    def _prepMsg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msgImage = self.font.render(msg, True, self.textColour, self.buttonColour)
        self.msgImageRect = self.msgImage.get_rect()
        self.msgImageRect.center = self.rect.center
    
    def drawButton(self):
        # Draw blank button and then draw message
        self.screen.fill(self.buttonColour, self.rect)
        self.screen.blit(self.msgImage, self.msgImageRect)

