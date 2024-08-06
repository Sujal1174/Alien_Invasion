import pygame
from pygame.sprite import Sprite

from settings import Settings

class Ship(Sprite) :
	"""A class to manage the ship."""

	def __init__(self , ai_game) :
		"""Initialize the ship and set its starting position"""
		super().__init__()
		
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		# an attribute of AlienInvasion class is settings which is an instance of Settings class

		self.screen_rect = ai_game.screen.get_rect()
		# Note : pygame treats all the game elements like rectangles even if they are not.
		# This approach is efficient because rectangles are simple geometrical shapes.
		# Read about this topic from the book as well
		# screen is a surface object (screen = pygame.display.set_mode()) and get_rect method can be performed 
		# on a surface object. It returns an object that represents dimension and position of surface.
		# This object has certain attributes like top,left,right,bottom ; center ,centerx,centery ;
		# midbottom, midtop,midleft,midright ;x ,y

		self.image = pygame.image.load('C:/Users/sujal/Documents/Alien_Invasion/images/roc1.bmp')
		# pygame.image is a module and load is a function within that
		# This function returns a surface object for the image to be drawn on screen.
		
		self.scaled_image = pygame.transform.scale(self.image , (150 , 150))
		self.image = self.scaled_image
		self.rect = self.image.get_rect()
		# since self.image is an surface object as we  previous code, We can apply get_rect() function on it --
		# that returns an object that represents dimension and position of that surface object.

		self.rect.y = self.settings.screen_height - 150
		self.rect.x = (self.settings.screen_width - 150) / 2
		# I assigned the midbottom attribute value of object that represents the dimension and position of ---
		# surface object that represents entire pygame window to that of --

		# Store a float for the ship's exact position
		self.x = float(self.rect.x)

		self.moving_right = False
		self.moving_left = False
		# Movement flag;start with a ship that's not moving


	def update(self) :
		"""update the position based on the movement flag"""
		if self.moving_right and self.rect.right < self.screen_rect.right :
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0 :
			self.x -= self.settings.ship_speed

		# Update rect object from self.x
		self.rect.x = self.x

	def blitme(self) :
		"""Draw the ship at its current location"""
		self.screen.blit(self.image, self.rect)
		# This blit is applied on a surface object and it takes two arguments ,one argument is the---
		# surface object for the image and and the other argument is the object that represents dimension--
		# and position of that surface object(first argument)
	
	def center_ship(self) :
		"""Center the ship on the screen."""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)
	