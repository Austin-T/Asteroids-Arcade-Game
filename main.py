"""Here is the 'main' file for the "ASTEROIDS" game. In the game, A ship must avoid asteroids by moving left,
right, and by firing lasers which will destroy incoming asteroids. The Game continues until an incoming asteroid
crashes into the ship. The user is awarded points based on the amount of asteroids they have destroyed. This file
must be run as the entry point to the program.

Version: 1
Last Update: 2019/08/21
Contributors: Austin Tralnberg
"""

from graphic_support_mod import Window
from game import Game


def main():
    """Creates Window object, creates Game object, and executes one round of the
    Asteroids game.
    """

    window = Window('Asteroids', 700, 700)
    game = Game(window)
    game.play()
    window.close()


if __name__ == '__main__':
    main()
