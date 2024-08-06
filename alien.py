import pygame 
from pygame.sprite import Sprite 
from random import choice 

from settings import Settings 

class Alien(Sprite) :
	"""A class to represent a single alien in the flleet."""

	def __init__(self , ai_game) :
		"""Initialize the alien and set its starting positon."""
		super().__init__()
		paths = ['C:/Users/sujal/Documents/Alien_Invasion/images/image (1).bmp' ,
	 	'C:/Users/sujal/Documents/Alien_Invasion/images/image (2).bmp'
		]
		path = choice(paths)
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		# Load the alien image and set its rect attribute.
		self.image = pygame.image.load(path)
		self.scaled_image = pygame.transform.scale(self.image , (150, 150))
		self.image = self.scaled_image
		self.rect = self.image.get_rect()

		# start each new alien near the top left of the screen
		self.rect.x = 70 
		# This is alien-x-spacing
		self.rect.y = 50
		# This is alien-y-spacing

		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

	def _check_edges(self) :
		"""Return True if alien is at edge of screen."""
		screen_rect = self.screen.get_rect()
		return (self.rect.right > screen_rect.right)  or  (self.rect.left <= 0)

	def update(self) :
		"""Move the alien to the rigth."""
		self.x += self.settings.alien_speed * self.settings.fleet_direction
		self.rect.x =self.x

		