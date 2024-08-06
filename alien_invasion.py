import sys 
from time import sleep
# we will use sys module to exit the game when the player exits. ---
# (player clicks on wrong button in pygame window)
# I imported this module because remember book says to import module or libraries that are standard
# (standard means these modules and libraries comes with the installation package of python)
# Plus i Put blank line and then imported a third party library (package) because the book says
# Even if i have to import my module and standard library(or module) , i would have to do the same.

import pygame 
from random import randint

from settings import Settings 
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion :
	"""
	This class represents the entire game.
	It manages all the game elements and settings
	"""

	def __init__(self) :
		"""initialize the game and create game resources"""

		pygame.init()
		# This method sets up all the module and prepares them to be ready to be used
		# In Book language , It intializes the background settings that pygame needs to work properly
		# In every pygame project ,you have to use this method
		
		self.bullet_counter = 0
		self.screen = pygame.display.set_mode( (0,0) , pygame.FULLSCREEN )
		self.settings = Settings(self.screen.get_rect().width , self.screen.get_rect().height )
		# I defined an attribute which is assigned an object/instance that represents a surface.
		# That surface is entire pygame window . Its size  is fullscreen.
		# pygame is a library, pygame.display is a module and set_mode is a function in this module.
		# This functions returns an object that represents a pygame window of particular dimension
		# dimension is passed as argument. Dimension is expressed in the form of tupple.

		# create an instance to store game statistics,
		# and create a scoreboard.
		self.stats = GameStats(self)
		self.sb = Scoreboard(self) 

		pygame.display.set_caption('Alien Invasion')
		# This is yet another function (set_caption) that takes in a Caption(a string) as argument and 
		# displays it in pygame window top

		self.clock = pygame.time.Clock()
		# pygame.time is a module and Clock is a class in it.
		# we created a clock object . On this clock object, I will use tick method and keep it in while loop.
		# That tick method takes and argument frame rate which you want.(say argument = 60)
		# It returns the time elapsed  since the last time it was called . 
		# If the argument = 60 , while loop is iterated 60 times per second and so 60 frames are generated --
		# with pygame.display.flip() function , if  returned value of tick method is 1/60 sec , then its perfect.
		# but if it returns value less than 1/60 sec , it means loop iterates faster and it introduces some pause time
		# before while loop is iterated next time . so as to run the animations at consistent rate.
		# if it less than 1/60 sec , it can't do anything as it depends on processing speed on the machine in --
		# which we are running program

		self.bg_color = self.settings.bg_color
		# I defined an tuple as attribute . Because This will be used to represent RGB color values in pygame.
		# Then, I will apply 'fill method' on surface object representing entire pygame window (here , screen) --
		# that will set bg color with the argument as self.bg_color

		self.check_bullet_fire = False
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self._create_fleet()

		# Start Alien Invasion in an active state.
		self.game_active = False

		# Make the play button.
		self.play_button = Button(self , "Play")


	def run_game(self) :
		"""start the main loop for the game """
		
		while True :
			# This while loop contains an event loop and code that manges screen updation
			# and  continuosly rendering graphics. It continuosly draws new frame.
			# event loop is used to respond to event that occur during  program
			# Event loop code has been refactored into new method (_check_events()).
			# all the code related to screen updation is stored in _update_screen() method
			
			self._check_events()

			if self.game_active :
				self.ship.update()
				if self.bullet_counter % 10 == 0 :
					self._fire_bullet()
				if self.check_bullet_fire :
					self.bullet_counter += 1
				# Just think on this why i wrote this.
				# Alternatively, I could have used pygame.time.get_ticks() function as suggested by chatgpt
				self._update_bullets()
				self._update_aliens()	

			self._update_screen()
			self.clock.tick(60)
			
	def _check_events(self) :
		"""Respond to keypresses and mouse events"""
		for event in pygame.event.get() :
			# pygame.event is a module and get is a explicit function from this module
			# This get function returns a list of  objects of class pygame.event.Event that
			# has a attribute type .
			# I can create my own Event object like this : 
			# key_down_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)
			# The second argument of this function is key code for different keys in pygame .
			# This event has type  attribute value = pygame.KEYDOWN and it will be recognised by pressing 'a' key
			# This event has to be posted in the event queue if  you wnated this to be recognised by get function.
			# Code to post it : pygame.event.post(key_down_event)

				if event.type == pygame.QUIT :
					# pygame.QUIT is an attribute value of event object . Basically, it specifies type of event
					sys.exit()
					# sys is a module and exit is a function from it. This closes the pygame window
				elif event.type == pygame.KEYDOWN :
					self._check_keydown_events(event)
				elif event.type == pygame.KEYUP :
					self._check_keyup_events(event)
				elif event.type == pygame.MOUSEBUTTONDOWN :
					mouse_pos = pygame.mouse.get_pos()
					self._check_play_button(mouse_pos)

	def _check_play_button(self , mouse_pos) :
		"""Start a new game when the player clicks play"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.game_active :
			# Reset the game settings.
			self.settings.initialize_dynamic_settings()

			# Reset the game Statistics
			self.stats.reset_stats()
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()
			self.game_active = True 

			# Get rid of any remaining bullets and Aliens.
			self.bullets.empty()
			self.aliens.empty()

			# Create a new fleet and center the ship.
			self._create_fleet()
			self.ship.center_ship()

			# Hide the mouse cursor 
			pygame.mouse.set_visible(False)

	def _check_keydown_events(self, event ) : 
		"""respond to keypresses"""
		if event.key == pygame.K_RIGHT :
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT :
			self.ship.moving_left = True	
		elif event.key == pygame.K_q :
			sys.exit()	
		elif event.key == pygame.K_SPACE :
			self.check_bullet_fire = True

	def _check_keyup_events(self, event ) :
		"""respond to key releases"""
		if event.key == pygame.K_RIGHT :
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT :
			self.ship.moving_left = False
		elif event.key == pygame.K_SPACE :
			self.check_bullet_fire = False
			self.bullet_counter = 0

	def _create_fleet(self) :
		"""create a fleet of aliens."""
		# make a alien
		alien = Alien(self)
		# alien_x_spacing , alien_y_spacing = alien.rect.x , alien.rect.y

		current_x , current_y = randint(40 , 80), 100
		while current_y < self.settings.screen_height - 3 * alien.rect.height :
			while current_x < self.settings.screen_width -  alien.rect.width :
				self._create_aliens(current_x , current_y)
				current_x += randint(50 , 150) + alien.rect.width
			
			# Finished a row, reset x value, and increment y value
			current_x = randint(40,100)  
			# current_y += randint(0 , 30) + alien.rect.height
			current_y +=  alien.rect.height

	def _create_aliens(self , x_position , y_position ) :
		"""Create an Alien and place it in the row."""
		new_alien = Alien(self) 
		new_alien.x = x_position
		new_alien.y = y_position
		new_alien.rect.x = x_position
		new_alien.rect.y = y_position
		self.aliens.add(new_alien)

	def _check_fleet_edges(self) :
		"""respond approproately if any aliens have reached an edge."""
		for alien in self.aliens.sprites() :
			if alien._check_edges() :
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self) :
		"""drop the entire fleet and change the fleet's direction."""
		for alien in self.aliens.sprites() :
			alien.rect.y += self.settings.fleet_drop_speed
			# we could have defined this method in alien class and call that method on alien group
			# That would make changes to all alien attributes siultaneously
			# but we need to inherit Sprite class to Alien class before doing this .
		self.settings.fleet_direction *= -1

	def _update_screen(self) :
		"""update images on the screen, and flip to the new screen."""
		self.screen.fill(self.bg_color)
		self.screen.blit(self.settings.scaled_background_image , self.settings.background_rect )
		for bullet in self.bullets.sprites() :
			bullet.draw_bullet()	
		self.ship.blitme()
		self.aliens.draw(self.screen)
		# for alien in self.aliens.copy() :
		# 	self.screen.blit(alien.scaled_image , alien.rect)

		# Draw the score information.
		self.sb.show_score()

		if not self.game_active :
			self.play_button.draw_button()

		# Make the recently drawn frame or screen visible 
		# for each pygame window, I have to perform this function seperately
		# Note : Flip() is not a method of the class of instance returned by pygame.display.set_mode() function
		# so, you can't apply flip method like this : screen.flip() {see above , screen = pygame.display.set_mode()}
		pygame.display.flip()
		# pygame.display is a module and flip is a function that updates the frames only once , 
		# after continuos iteration through while loop , it continuosly manages screen updation with new frames 
		# and renders motion of graphics element (game elements)

	def _fire_bullet(self) :
		if self.check_bullet_fire and len(self.bullets) < self.settings.bullets_allowed :
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self) :
		"""Update position of bullets and get rid of old bullets."""
		# update bullet positions.
		self.bullets.update()

		# get rid f bullets that have disappeared
		for bullet in self.bullets.sprites() :
			# I have a doubt here, Copy  method is'nt a built in method in pygame for grooups 
			# If this function ret
			if bullet.rect.bottom <= 0 :
				self.bullets.remove(bullet)
		
		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self) :
		"""respond to bullet-alien collisions."""
		# Remove any bullets and aliens that have collided.
		collisions = pygame.sprite.groupcollide(
			self.bullets , self.aliens , True , True)
		
		if collisions :
			for alien in collisions.values() :
				self.stats.score += self.settings.alien_points * len(alien)
			# Note collision is a dictionary whose keys are bullets and value are aliens 
			# Here , each bullet has one alien associated with it as after each bullet-alien collision,
			# bullet and alien disappers due to True argument for third and fourth parameter in
			# groupcollide function.But in future, For testing if we set the third arguement to False ,
			#In that case , each bullet will have a list of alien as value 
			# That's why i wrote the code like this .
			self.sb.prep_score()
			self.sb.check_high_score()
		
		if not self.aliens :
			# Destroy existing bullets and create new fleet.
			self.bullets.empty()
			self._create_fleet()
			self.ship.center_ship()
			# self.increase_level()
			# I have used this method here before the book introduced following method 
			self.settings.increase_speed()

			# Increase level.
			self.stats.level += 1
			self.sb.prep_level()

	def _update_aliens(self) :
		"""check if the fleet is at an edge, then update positions."""
		self._check_fleet_edges()
		self.aliens.update()

		# Look for alien-ship collisions.
		if pygame.sprite.spritecollideany(self.ship , self.aliens) :
			self._ship_hit()
		
		# Look for aliens hitting the bottom of the screen.
		self._check_aliens_bottom()

	def _ship_hit(self) :
		"""Respond to the ship being hit by an alien."""
		if self.stats.ships_left > 0 :
			# Decrement ships_left, and update scoreboard.
			self.stats.ships_left  -= 1
			self.sb.prep_ships()

			# Get rid of any remaining bullets and aliens
			self.bullets.empty()
			self.aliens.empty()

			# Create a new fleet and center the ship.
			self._create_fleet()
			self.ship.center_ship()

			# Pause 
			sleep(0.5)
		else :
			self.game_active = False
			pygame.mouse.set_visible(True)

	def _check_aliens_bottom(self) :
		"""Check if any aliens have reached the bottom of the screen."""
		for alien in self.aliens.sprites() :
			if alien.rect.bottom >= self.settings.screen_height :
				# Treat this the same as if the ship got hit.
				self._ship_hit()
				break

	# def _increase_level(self ) :
	# 	"""Increment the difficulty level of the game as one fleet is destroyed"""
	# 	self.settings.alien_speed += 0.5
	# 	self.settings.fleet_drop_speed += 5

	
if __name__ == '__main__' :
	# search on chatgpt what does above conditional test means.
	# make a game instance and run the game
	ai = AlienInvasion()
	ai.run_game()