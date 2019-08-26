"""Here is the 'Asteroid' class for the "Asteroids" game. This class can be used to create Asteroid objects
which move downwards across the window towards the user's ship. When asteroids come into contact with
the ship, the ship is destroyed. When asteroids come into contact with a laser, the asteroid is destroyed.
Each Asteroid object has a size, a location, and a velocity.
"""

import pygame


class Asteroid:

    @classmethod
    def set_window(cls, window):
        """Sets the window for all Asteroid objects.

        :param window: the pygame support module window object
        """

        cls.window = window

    def __init__(self, size, location, velocity):
        """Initializes an instance of the Asteroid class.

        :param size: an int representing the diameter of the asteroid.
        :param location: a tuple or list containing two ints: the first digit represents the x-coordinate of the
        asteroid while the second digit is for the y-coordinate.
        :param velocity:  a tuple or list containing two ints: the first digit represents the lateral velocity of the
        asteroid while the second digit is for the vertical velocity.
        """

        self.velocity = velocity
        self.asteroid_rect = pygame.Rect(location[0], location[1], size, size)
        self.asteroid_img = pygame.transform.scale(pygame.image.load("images/asteroid.png"), (size, size))

    def move(self):
        """Move the asteroid 'self.velocity[0]' units in the lateral direction, and 'self.velocity[1]' units in the
        vertical direction.
        """

        self.asteroid_rect.move_ip(self.velocity[0], self.velocity[1])

    def draw(self):
        """Draws the asteroid onto the game window."""

        Asteroid.window.get_surface().blit(self.asteroid_img, self.asteroid_rect)

    def get_rect(self):
        """Returns the rectangle object which represents the asteroid.

        :return: a pygame.Rect object
        """

        return self.asteroid_rect

    def check_collide(self, other_rect):
        """ Checks to see if 'other_rect' is overlapping with the rectangle which represents the asteroid.

        :param other_rect: a pygame.Rect object
        :return: returns True if if 'self.asteroid_rect' has overlapped with 'other_rect'. False otherwise.
        """
        return self.asteroid_rect.colliderect(other_rect)
