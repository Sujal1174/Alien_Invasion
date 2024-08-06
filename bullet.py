import pygame 
from pygame.sprite import Sprite

class Bullet(Sprite) :
	"""A class to manage bullets fired from the ship"""
	
	def __init__(self, ai_game) :
		"""create bullet object at the ship's current location."""
		super().__init__() 
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		
		# create a bullet surface object and then set the correct position
		self.bullet_image = pygame.image.load('C:/Users/sujal/Documents/Alien_Invasion/images/bullet.bmp')
		self.scaled_bullet_image = pygame.transform.scale(
			self.bullet_image , (self.settings.bullet_width , self.settings.bullet_height)
			)
		self.rect = self.scaled_bullet_image.get_rect()

		self.rect.midtop = ai_game.ship.rect.midtop
		 
		# store the bullet y atttribute as a float
		self.y = float(self.rect.y)

	def  update(self) :
		"""Move the bullet up the screen."""
		# update the exact  position of the bullet
		self.y -= self.settings.bullet_speed
		# update the rect position
		self.rect.y = self.y

	def draw_bullet(self) :
		"""draw the bullet to the screen."""
		self.screen.blit(self.scaled_bullet_image , self.rect)
		