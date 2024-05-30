import pygame

class Enemy:
    def __init__(self, image_path, position, window, max_health=100):
        """
        Initializes the Enemy object.

        Args:
            image_path (str): Path to the enemy image.
            position (list): The initial position of the enemy [x, y].
            window (pygame.Surface): The game window surface.
            max_health (int): The maximum health of the enemy.
        """
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.75), int(self.image.get_height() * 0.75)))
        self.position = position
        self.window = window
        self.max_health = max_health
        self.current_health = max_health

    def take_damage(self, damage):
        """
        Reduces the enemy's health by the specified damage amount.

        Args:
            damage (int): The amount of damage to inflict on the enemy.

        Returns:
            bool: True if the enemy's health is <= 0, indicating it is defeated.
        """
        self.current_health -= damage
        return self.current_health <= 0

    def draw(self):
        """
        Draws the enemy and its health bar on the game window.
        """
        adjusted_position = [
            max(0, min(self.window.get_width() - self.image.get_width(), self.position[0])),
            max(0, min(self.window.get_height() - self.image.get_height(), self.position[1]))
        ]
        self.window.blit(self.image, adjusted_position)
        self.draw_health_bar(adjusted_position)

    def draw_health_bar(self, position):
        """
        Draws the health bar above the enemy.

        Args:
            position (list): The position where the enemy is drawn [x, y].
        """
        health_bar_width = self.image.get_width()
        health_bar_height = 5
        health_bar_x = position[0]
        health_bar_y = position[1] - health_bar_height - 5  # 5 pixels above the enemy image

        health_ratio = self.current_health / self.max_health
        current_health_bar_width = int(health_bar_width * health_ratio)

        pygame.draw.rect(self.window, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(self.window, (0, 255, 0), (health_bar_x, health_bar_y, current_health_bar_width, health_bar_height))
