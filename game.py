"""This file contains the 'Game' class for the "ASTEROIDS" game. This class controls all game play and game
objects. Once the Game object has been initialized, the game can be run by making a call to the Game.play()
method.
"""

import time
import random
import pygame
from pygame.locals import *
from laser import Laser
from asteroid import Asteroid
from star import Star


class Game:

    def __init__(self, window):
        """Initializes an instance of the Game class.

        :param window: the pygame support module window object
        """

        # Static class attributes
        self.window = window
        self.surface = window.get_surface()
        self.close_clicked = False
        self.continue_game = True
        self.pressed = None
        self.ship_exploded = False
        self.laser_list = []  # A list to contain all Laser Objects
        self.asteroid_list = []   # A list to contain all Asteroid Objects
        self.star_list = []   # A list to contain all Star Objects
        self.last_fire = 0
        self.clock = 0
        self.game_end_clock = 0
        self.last_spawn = 0
        self.score = 0

        # Adjustable class attributes
        self.header_1_size = 50
        self.header_2_size = 20
        self.left_margin = 100
        
        self.ship_size = (50, 50)
        self.ship_lateral_speed = 8
        self.ship_height = 615  # The fixed distance from the top of the window where the ship will be
        
        self.asteroid_buffer = 20 # Initial buffer only
        self.asteroid_buffer_decrease = 0.05
        self.asteroid_speed = 2  # Initial speed only
        self.asteroid_speed_increase = 0.05
        self.asteroid_size = 50
        self.asteroid_margin_x = 200  # The lateral distance beside the window in which an asteroid may spawn
        self.asteroid_margin_y = 100  # The vertical distance above the window in which an asteroid may spawn
        
        self.laser_buffer = 15
        self.laser_buffer_intro = 20  # Adjust this to change the amount of lasers that fire before the game begins
        self.laser_size = (30, 50)
        self.laser_offset = 15  # May be adjusted to center the laser over the ship when firing
        self.laser_speed = 20

        self.star_population_size = 500  # The amount of stars that should initially populate the screen
        self.star_size = 2
        self.star_velocity = (0, 1)

        self.pause_time = 0.02  # Smaller number is faster game

        # Create image/Rect objects for space ship animation
        self.ship_img_1 = pygame.transform.scale(pygame.image.load("images/ship_1.png"), self.ship_size)
        self.ship_img_2 = pygame.transform.scale(pygame.image.load("images/ship_2.png"), self.ship_size)
        self.explosion_1 = pygame.transform.scale(pygame.image.load("images/explosion_1.png"), self.ship_size)
        self.explosion_2 = pygame.transform.scale(pygame.image.load("images/explosion_2.png"), self.ship_size)
        self.explosion_3 = pygame.transform.scale(pygame.image.load("images/explosion_3.png"), self.ship_size)
        self.explosion_4 = pygame.transform.scale(pygame.image.load("images/explosion_4.png"), self.ship_size)
        self.explosion_5 = pygame.transform.scale(pygame.image.load("images/explosion_5.png"), self.ship_size)
        self.explosion_6 = pygame.transform.scale(pygame.image.load("images/explosion_6.png"), self.ship_size)
        self.ship_rect = pygame.Rect(self.window.get_width()/2, self.ship_height, self.ship_size[0], self.ship_size[1])

        # Set the window for Star, Laser, and Asteroid Objects
        Star.set_window(self.window)
        Laser.set_window(self.window)
        Asteroid.set_window(self.window)

    def play(self):
        """Executes one full round of the Asteroids game. The game begins with an introductory message.
        Then game play begins. Once a player's ship has been destroyed, the game is over, and a game-
        over message is displayed
        """

        self.game_intro()
        self.game_play()
        self.game_over()

    def game_play(self):
        """Executes the game while the player has not lost, and the close box has not been clicked."""

        while not self.close_clicked and self.continue_game:
            self.handle_event()
            self.update()
            self.draw()
            self.check_collision()
            self.clock += 1
            time.sleep(self.pause_time)

    def handle_event(self):
        """Checks to see if the window has been close-clicked. Updates 'self.pressed' to contain
        the set of keys that are currently pressed.
        """

        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True

        self.pressed = pygame.key.get_pressed()

    def handle_event_intro(self):
        """Allows the user to close-click the window. Checks to see if the user has pressed the
        enter key.

        :return: Returns true if the user has pressed the 'enter' key. False otherwise.
        """

        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True

        return pygame.key.get_pressed()[K_RETURN]

    def draw(self):
        """Draws all game objects to the surface of the window. Alternates between ship images in order to
        animate the ship's thrusters.
        """

        self.window.clear()

        score_x_position = self.window.get_width() - self.window.get_string_width(str(self.score))
        self.window.draw_string(str(self.score), score_x_position, 0)

        if self.clock % 2 == 0:
            self.surface.blit(self.ship_img_1, self.ship_rect)
        else:
            self.surface.blit(self.ship_img_2, self.ship_rect)

        self.draw_lasers()
        self.draw_stars()
        self.draw_asteroids()

        self.window.update()

    def draw_intro(self):
        """Draws all game objects to the surface of the window. Draws a set of pre-game instructions to the
         surface of the window. Alternates between ship images in order to give animation to the ship's thrusters.
        """

        self.window.clear()

        self.window.set_font_size(self.header_1_size)
        self.window.draw_string("ASTEROIDS", self.left_margin, 100)

        self.window.set_font_size(self.header_2_size)
        self.window.draw_string("Use the left and right arrows to control your space ship.", self.left_margin, 250)
        self.window.draw_string("Click your space bar to fire lasers and destroy asteroids.", self.left_margin, 280)
        self.window.draw_string("Destroy asteroids to Earn Points.", self.left_margin, 310)

        self.window.set_font_size(self.header_1_size)
        self.window.draw_string("PRESS 'ENTER' TO BEGIN", self.left_margin, 400)

        score_x_position = self.window.get_width() - self.window.get_string_width(str(self.score))
        self.window.draw_string(str(self.score), score_x_position, 0)

        if self.clock % 2 == 0:
            self.surface.blit(self.ship_img_1, self.ship_rect)
        else:
            self.surface.blit(self.ship_img_2, self.ship_rect)

        self.draw_stars()
        self.draw_lasers()

        self.window.update()

    def update(self):
        """Updates all game objects."""

        # asteroids
        self.create_asteroids()
        self.move_asteroids()
        self.remove_asteroids()
        
        # stars
        self.create_stars()
        self.move_stars()
        self.remove_stars()
        
        # lasers
        if self.pressed[K_SPACE]:
            self.create_laser()
        self.move_lasers()
        self.remove_lasers()

        # ship
        if self.pressed[K_RIGHT] and self.ship_rect.centerx < self.window.get_width():
            self.ship_rect.move_ip(self.ship_lateral_speed, 0)
        if self.pressed[K_LEFT] and self.ship_rect.centerx > 0:
            self.ship_rect.move_ip(-self.ship_lateral_speed, 0)

    def update_intro(self):
        """Updates all game objects during intro."""

        if self.ship_rect.centerx < self.window.get_width():
            self.ship_rect.move_ip(1, 0)
        else:
            self.ship_rect.move_ip(-self.window.get_width(), 0)
        if self.clock % self.laser_buffer_intro == 0:
            self.create_laser()
        if not self.star_list:
            self.fill_screen_w_stars()
        self.create_stars()
        self.move_stars()
        self.remove_stars()
        self.move_lasers()
        self.remove_lasers()

    def check_collision(self):
        """Checks to see if any asteroid has collided with the ship, and the game has ended. Checks to see
        if any laser has collided with an asteroid; if so, destroys the asteroid.
        """

        asteroid_index = 0
        for asteroid in self.asteroid_list:

            if asteroid.check_collide(self.ship_rect):
                self.continue_game = False

            laser_index = 0
            for laser in self.laser_list:
                kill = asteroid.check_collide(laser.get_rect())
                if kill:
                    del self.laser_list[laser_index]
                    del self.asteroid_list[asteroid_index]
                    self.score += 1
                laser_index += 1

            asteroid_index += 1

    def game_intro(self):
        """Displays the intro while the player has not pressed enter, and the close box has not been clicked."""

        while not self.close_clicked and not self.handle_event_intro():
            self.draw_intro()
            self.update_intro()
            self.clock += 1
            time.sleep(self.pause_time)

    def game_over(self):
        """Displays the game-over message while the player has not pressed enter, and the close box has
        not been clicked.
        """

        while not self.close_clicked and not self.handle_event_game_over():
            self.draw_game_over()
            self.update_game_over()
            self.game_end_clock += 1
            time.sleep(self.pause_time)

    def draw_game_over(self):
        """Draws all game objects onto the window. Draws a 'Game Over' message. Animates the explosion of the
        ship. Explosion sprites are drawn based on the amount of time which has passed since the game
        ended (i.e. asteroid collided with ship).
        """

        self.window.clear()

        self.window.set_font_size(self.header_1_size)
        self.window.draw_string("GAME OVER", self.left_margin, 100)
        self.window.draw_string("YOUR SCORE WAS" + " " + str(self.score), self.left_margin, 200)
        self.window.draw_string("PRESS 'ENTER' TO EXIT", self.left_margin, 270)

        if not self.ship_exploded:
            if self.game_end_clock < 5:
                self.surface.blit(self.explosion_1, self.ship_rect)
            elif self.game_end_clock < 10:
                self.surface.blit(self.explosion_2, self.ship_rect)
            elif self.game_end_clock < 15:
                self.surface.blit(self.explosion_3, self.ship_rect)
            elif self.game_end_clock < 20:
                self.surface.blit(self.explosion_4, self.ship_rect)
            elif self.game_end_clock < 25:
                self.surface.blit(self.explosion_5, self.ship_rect)
            elif self.game_end_clock < 30:
                self.surface.blit(self.explosion_6, self.ship_rect)
            else:
                self.ship_exploded = True

        self.draw_stars()
        self.draw_lasers()
        self.draw_asteroids()

        self.window.update()

    def update_game_over(self):
        """Updates all game objects during 'game over'."""

        self.create_stars()
        self.move_stars()
        self.remove_stars()

        self.move_lasers()
        self.remove_lasers()

        self.move_asteroids()
        self.remove_asteroids()

    def handle_event_game_over(self):
        """Allows the user to close-click the window. Checks to see if the user has pressed the
        enter key.

        :return: Returns true if the user has pressed the 'enter' key. False otherwise.
        """

        event = pygame.event.poll()
        if event.type == QUIT:
            self.close_clicked = True

        return pygame.key.get_pressed()[K_RETURN]

    def create_laser(self):
        """Checks to see if enough time has elapsed since the last Laser has been fired. If so, creates a
        new Laser object.
        """

        if self.clock > self.last_fire + self.laser_buffer:
            new_laser_position = (self.ship_rect.centerx - self.laser_offset, self.ship_height - self.laser_offset)
            new_laser = Laser(self.laser_size, new_laser_position, self.laser_speed)
            self.laser_list.append(new_laser)
            self.last_fire = self.clock

    def move_lasers(self):
        """Moves each Laser object to its new position."""

        for laser in self.laser_list:
            laser.move()

    def draw_lasers(self):
        """Draws each Laser object to the surface of the window."""

        for laser in self.laser_list:
            laser.draw()

    def remove_lasers(self):
        """Deletes Laser objects which have exited the top of the game window."""

        index = 0
        for laser in self.laser_list:
            if laser.get_rect().centery < 0:
                del self.laser_list[index]
            index += 1

    def create_asteroids(self):
        """Creates a new Asteroid object if enough time has elapsed since the creation of the last Asteroid.
        Selects a random direction for the asteroid to move in. Decreases the amount of time between the
        creation of each Asteroid object, so Asteroids are created more rapidly as the game progresses. Increases
        the speed of each Asteroid that is created.
        """

        x_pos = random.randint(-self.asteroid_margin_x, self.window.get_width() + self.asteroid_margin_x)
        if self.clock > self.last_spawn + self.asteroid_buffer:
            move_chose = random.randint(0, 3)
            if move_chose == 0:
                x_mov = random.randint(-1, 1)
            else:
                x_mov = 0
            self.last_spawn = self.clock
            self.asteroid_buffer -= self.asteroid_buffer_decrease
            new_asteroid = Asteroid(self.asteroid_size, [x_pos, -self.asteroid_margin_y], [x_mov, self.asteroid_speed])
            self.asteroid_list.append(new_asteroid)
            self.asteroid_speed += self.asteroid_speed_increase

    def move_asteroids(self):
        """Moves each Asteroid object to its new position."""

        for asteroid in self.asteroid_list:
            asteroid.move()

    def draw_asteroids(self):
        """Draws each Asteroid object to the game window."""

        for asteroid in self.asteroid_list:
            asteroid.draw()

    def remove_asteroids(self):
        """Deletes Asteroid object which have exited the bottom of the game window."""

        index = 0
        for asteroid in self.asteroid_list:
            if asteroid.get_rect().centery > self.window.get_height():
                del self.asteroid_list[index]
            index += 1

    def create_stars(self):
        """Creates a new Star object in random position."""

        x_pos = random.randint(0, self.window.get_width())
        self.star_list.append(Star(self.star_size, [x_pos, 0], self.star_velocity))

    def fill_screen_w_stars(self):
        """Populates the screen with Star objects in random positions."""

        for i in range(self.star_population_size):
            x_pos = random.randint(0, self.window.get_width())
            y_pos = random.randint(0, self.window.get_height())
            self.star_list.append(Star(self.star_size, [x_pos, y_pos], self.star_velocity))

    def move_stars(self):
        """Moves each Star object to its new position."""

        for star in self.star_list:
            star.move()

    def draw_stars(self):
        """Draws each Star object to the game window."""

        for star in self.star_list:
            pygame.draw.rect(self.surface, Color("white"), star.get_rect())

    def remove_stars(self):
        """Deletes Star objects which have exited the bottom of the game window."""

        index = 0
        for star in self.star_list:
            if star.get_rect().centery > self.window.get_height():
                del self.star_list[index]
            index += 1
