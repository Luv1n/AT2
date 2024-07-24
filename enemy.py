import pygame
import random

class Enemy:
    def __init__(self, image_path, position, window, max_health=100):
        self.image_path = image_path  # Store the image path
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.75), int(self.image.get_height() * 0.75)))
        self.position = position
        self.window = window
        self.max_health = max_health
        self.current_health = max_health

        # Movement parameters
        self.speed = 0.4  # Speed at which the enemy moves
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()  # Random initial direction

    def take_damage(self, damage):
        self.current_health -= damage
        return self.current_health <= 0

    def move(self):
        # Update position based on direction and speed
        self.position[0] += self.direction.x * self.speed
        self.position[1] += self.direction.y * self.speed

        # Bounce off the edges of the screen
        if self.position[0] < 0 or self.position[0] > self.window.get_width() - self.image.get_width():
            self.direction.x *= -1
        if self.position[1] < 0 or self.position[1] > self.window.get_height() - self.image.get_height():
            self.direction.y *= -1

    def draw(self):
        self.move()  # Update position before drawing
        adjusted_position = [
            max(0, min(self.window.get_width() - self.image.get_width(), self.position[0])),
            max(0, min(self.window.get_height() - self.image.get_height(), self.position[1]))
        ]
        self.window.blit(self.image, adjusted_position)
        self.draw_health_bar(adjusted_position)

    def draw_health_bar(self, position):
        health_bar_width = self.image.get_width()
        health_bar_height = 5
        health_bar_x = position[0]
        health_bar_y = position[1] - health_bar_height - 5  # 5 pixels above the enemy image

        health_ratio = self.current_health / self.max_health
        current_health_bar_width = int(health_bar_width * health_ratio)

        pygame.draw.rect(self.window, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(self.window, (0, 255, 0), (health_bar_x, health_bar_y, current_health_bar_width, health_bar_height))

