import sys
from time import sleep
import pygame
from settings import Settings
from gameStats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screenWidth, self.settings.screenHeight))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bgColour = (230, 230, 230) #RGB
        self._createFleet()
        self.stats = GameStats(self)
        self.playButton = Button(self, "Play")
        self.sb = Scoreboard(self)

    def runGame(self):
        """Start the main loop for the game."""
        while True:
            self._checkEvents()

            if self.stats.gameActive:
                self.ship.update()
                self._updateBullets()
                self._updateAliens()

            self._updateScreen()

    def _checkEvents(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._checkKeydownEvents(event)
                elif event.type == pygame.KEYUP:
                    self._checkKeyupEvents(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    self._checkPlayButton(mousePos)

    def _checkKeydownEvents(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_d: # Move Right
            self.ship.movingRight = True
        elif event.key == pygame.K_a:   # Move Left
            self.ship.movingLeft = True
        elif event.key == pygame.K_ESCAPE: # Quit the game
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fireBullet()
        elif event.key == pygame.K_p:
            self._startGame()

    def _checkKeyupEvents(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_d:
            self.ship.movingRight = False
        elif event.key == pygame.K_a:
            self.ship.movingLeft = False

    def _checkPlayButton(self, mousePos):
        """Start a new game when the player clicks Play."""
        buttonClicked = self.playButton.rect.collidepoint(mousePos)
        if buttonClicked and not self.stats.gameActive:
            # Reset the game settings
            self.settings.initializeDynamicSettings()
            pygame.mouse.set_visible(False)     #Hide mouse cursor
            self.stats.resetStats()     #Reset game stats
            self._startGame()
            self.sb.prepScore()
            self.sb.prepLevel()
            self.sb.prepShips()

    def _startGame(self):
        # Start game
        self.stats.gameActive = True

        # Get rid of any remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship
        self._createFleet()
        self.ship.centerShip()

    def _fireBullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bulletsAllowed:
            newBullet = Bullet(self)
            self.bullets.add(newBullet)

    def _createFleet(self):
        """Create the fleet of aliens."""
        # Make an Alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alienWidth, alienHeight = alien.rect.size
        availableSpaceX = self.settings.screenWidth - (2 * alienWidth)
        numberAliensX = availableSpaceX // (2 * alienWidth)

        # Determine the number of rows of aliens that fit on the screen
        shipHeight = self.ship.rect.height
        availableSpaceY = (self.settings.screenHeight - (3 * alienHeight) - shipHeight)
        numberRow = availableSpaceY // (2 * alienHeight)

        # Create a full fleet of aliens
        for rowNumber in range(numberRow):  
            for alienNumber in range (numberAliensX):
                self._createAlien(alienNumber, rowNumber)
    
    def _checkFleetEdges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.checkEdges():
                self._changeFleetDirection()
                break

    def _changeFleetDirection(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleetDropSpeed
        self.settings.fleetDirection *= -1

    def _createAlien(self, alienNumber, rowNumber):
        """Create an alien and place it in the row"""
        alien = Alien(self)
        alienWidth, alienHeight = alien.rect.size
        alien.x = alienWidth + 2 * alienWidth * alienNumber
        alien.rect.x = alien.x
        alien.rect.y = alienHeight + 2 * alienHeight * rowNumber
        self.aliens.add(alien)

    def _updateAliens(self):
        """Check if the fleet is at an edge, then update the positions of all aliens in the fleet."""
        self._checkFleetEdges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._shipHit()

        # Look for aliens hitting the bottom of the screen
        self._checkAliensBottom()

    def _checkAliensBottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screenRect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screenRect.bottom:
                # Treat this the same as if the ship got hit
                self._shipHit()
                break

    def _updateBullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._checkBulletAlienCollisions()
    
    def _checkBulletAlienCollisions(self):
        """Respond to bullet-alien collisions"""
        #Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alienPoints * len(aliens)
            self.sb.prepScore()
            self.sb.checkHighScore()
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._createFleet()
            self.settings.increaseSpeed()

            # Increase level
            self.stats.level += 1
            self.sb.prepLevel()

    def _updateScreen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bgColour)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.drawBullet()
        self.aliens.draw(self.screen)

        # Draw the score information
        self.sb.showScore()

        # Draw the play button if the game is inactive
        if not self.stats.gameActive:
            self.playButton.drawButton()

        pygame.display.flip()

    def _shipHit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.shipsLeft > 0:
            # Decrement shipsLeft and update scoreboard
            self.stats.shipsLeft -= 1
            self.sb.prepShips()
            
            # Get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._createFleet()
            self.ship.centerShip()

            # Pause
            sleep(0.5)
        else:
            self.stats.gameActive = False
            pygame.mouse.set_visible(True)

if __name__ == "__main__":
# Make the game instance, and run the game
    ai = AlienInvasion()
    ai.runGame()