import pygame

class Settings :
	"""A class to store all the settings for Alien Invasion"""

	def __init__(self , screen_width, screen_height) :
		"""Initialize the game's static settings."""
		# Screen Settings
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.bg_color = (0, 0 , 0)

		# ship setting
		# self.ship_speed = 10
		self.ship_limit = 3

		# Background Settings
		self.background_image = pygame.image.load('C:/Users/sujal/Documents/Alien_Invasion/images/wp3493593.bmp')
		self.scaled_background_image = pygame.transform.scale(self.background_image , (self.screen_width , self.screen_height))
		self.background_rect = self.scaled_background_image.get_rect()

		# Bullet Settings
		# self.bullet_speed = 5.0
		self.bullet_width = 48
		self.bullet_height = 60
		self.bullets_allowed = 7

		# Alien Settings
		# self.alien_speed = 1.0
		self.fleet_drop_speed = 10

		# How quickly the game speeds up
		self.speedup_scale = 1.1
		# How quickly the alien point values increase
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self) :
		"""Initialize settings that can change throughout the game."""
		self.ship_speed = 4
		self.bullet_speed = 4
		self.alien_speed = 1.0

		# fleet direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

		# Scoring settings
		self.alien_points = 50

	def increase_speed(self) :
		"""Increase speed settings."""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)
		
		