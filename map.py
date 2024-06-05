import random
import pygame
from assets import GAME_ASSETS
from enemy import Enemy
from character import Warrior  # Import the Warrior class

class Map:
    def __init__(self, window):
        self.window = window
        self.map_image = pygame.image.load(GAME_ASSETS["dungeon_map"]).convert_alpha()
        self.map_image = pygame.transform.scale(self.map_image, (self.window.get_width(), self.window.get_height()))
        self.player_images = {
            'Warrior': pygame.image.load(GAME_ASSETS['warrior']).convert_alpha(),
            'Mage': pygame.image.load(GAME_ASSETS['mage']).convert_alpha(),
            'Rogue': pygame.image.load(GAME_ASSETS["rogue"]).convert_alpha()
        }
        self.player = None
        self.enemies = [
            Enemy(GAME_ASSETS["goblin"], [50, 50], self.window),
            Enemy(GAME_ASSETS["orc"], [self.window.get_width() - 120, 50], self.window),
            Enemy(GAME_ASSETS["skeleton"], [50, self.window.get_height() - 120], self.window),
            Enemy(GAME_ASSETS["skeleton"], [self.window.get_width() - 120, self.window.get_height() - 120], self.window)
        ]
        self.in_combat = False
        self.current_enemy = None
        self.blue_orb = None
        self.game_over = False

    def load_player(self, character_type):
        if character_type == 'Warrior':
            self.player = Warrior('Hero', 100)
        self.player_image = self.player_images[character_type]
        self.player_image = pygame.transform.scale(self.player_image, (int(self.player_image.get_width() * 0.15), int(self.player_image.get_height() * 0.15)))
        self.player.position = [self.window.get_width() / 2, self.window.get_height() / 2]

    def handle_events(self):
        if self.game_over:
            return 'quit'

        keys = pygame.key.get_pressed()
        move_speed = 2
        if keys[pygame.K_LEFT]:
            self.player.move('left', move_speed)
        if keys[pygame.K_RIGHT]:
            self.player.move('right', move_speed)
        if keys[pygame.K_UP]:
            self.player.move('up', move_speed)
        if keys[pygame.K_DOWN]:
            self.player.move('down', move_speed)

        if not self.in_combat:
            self.current_enemy = self.player.check_for_combat(self.enemies)
            if self.current_enemy:
                self.in_combat = True

        if self.in_combat:
            if self.player.handle_combat(self.current_enemy):
                self.in_combat = False

        if self.blue_orb and pygame.math.Vector2(self.player.position).distance_to(self.orb_position) < 25:
            self.game_over = True
            print("YOU WIN")
            return 'quit'

    def draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.map_image, (0, 0))
        self.window.blit(self.player_image, (self.player.position[0], self.player.position[1]))
        for enemy in self.enemies:
            enemy.draw()
        if self.blue_orb:
            self.window.blit(self.blue_orb, self.orb_position)
        pygame.display.flip()
