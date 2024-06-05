import pygame
import random
from enemy import Enemy

class Goblin(Enemy):
    def __init__(self, position, window):
        """
        Initializes the Goblin object, inheriting from Enemy.

        Args:
            position (list): The initial position of the goblin [x, y].
            window (pygame.Surface): The game window surface.
        """
        super().__init__("AT2/assets/goblin.png", position, window)

    def move(self):
        """
        Moves the goblin randomly within a specified range and keeps it within the window bounds.
        """
        self.position[0] += random.randint(-10, 10)
        self.position[1] += random.randint(-10, 10)
        self.position[0] = max(0, min(self.window.get_width() - self.image.get_width(), self.position[0]))
        self.position[1] = max(0, min(self.window.get_height() - self.image.get_height(), self.position[1]))
