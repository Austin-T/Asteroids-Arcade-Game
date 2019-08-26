"""Here is the 'Star' class for the "Asteroids" game. This class can be used to create Star objects
which move downwards across the window during game play. The star objects give the illusion that the user's
ship is moving through space. Each Star has a size, a location, and a velocity.
"""

import pygame


class Star:

    @classmethod
    def set_window(cls, window):
        """Sets the window for all Star objects.

        :param window: the pygame support module window object
        """

        cls.window = window

    def __init__(self, size, location, velocity):
        """Initializes an instance of the Star class.

        :param size: an int representing the diameter of the star.
        :param location: a tuple or list containing two ints: the first digit represents the x-coordinate of the
        star while the second digit is for the y-coordinate.
        :param velocity: an int representing the downward speed of the star.
        """

        self.velocity = velocity
        self.star_rect = pygame.Rect(location[0], location[1], size, size)

    def move(self):
        """Moves the star by 'self.velocity[0]' units in the lateral direction, and 'self.velocity[1]' units in the
        vertical direction."""

        self.star_rect.move_ip(self.velocity[0], self.velocity[1])

    def draw(self):
        """Draws the star onto the game window."""

        pygame.draw.rect(Star.window.get_surface(), pygame.Color("white"), self.star_rect)

    def get_rect(self):
        """Returns the rectangle object which represents the asteroid.

        :return: a pygame.Rect object
        """

        return self.star_rect

