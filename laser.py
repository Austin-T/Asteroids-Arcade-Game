"""Here is the 'Laser' class for the "Asteroids" game. This class can be used to create Laser objects
which are fired towards incoming asteroids by the user. Each Laser has a size, a location, and a velocity.
"""

import pygame


class Laser:

    @classmethod
    def set_window(cls, window):
        """Sets the window for all Laser objects.

        :param window: the pygame support module window object
        """

        cls.window = window

    def __init__(self, size, location, velocity):
        """Initializes an instance of the Laser class.

        :param size: a tuple or list containing two ints: the first digit represents the width of the laser
        while the second digit is for the height.
        :param location: a tuple or list containing two ints: the first digit represents the x-coordinate of the
        laser while the second digit is for the y-coordinate.
        :param velocity: an int representing the upward speed of the laser.
        """

        self.velocity = velocity
        self.laser_rect = pygame.Rect(location[0], location[1], size[0], size[1])
        self.laser_img = pygame.transform.scale(pygame.image.load("images/ship_laser.png"), (size[0], size[1]))

    def move(self):
        """Moves the laser by 'self.velocity' units in the upward direction."""

        self.laser_rect.move_ip(0, -self.velocity)

    def draw(self):
        """Draws the Laser onto the game window."""

        Laser.window.get_surface().blit(self.laser_img, self.laser_rect)

    def get_rect(self):
        """Returns the rectangle object which represents the Laser.

        :return: a pygame.Rect object
        """

        return self.laser_rect
