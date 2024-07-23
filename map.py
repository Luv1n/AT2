import random
import pygame
from assets import GAME_ASSETS
from enemy import Enemy
from character import Character

class Map:
    pygame.init()
    pygame.mixer.init()

    # Initialize the music volume
    pygame.mixer.music.set_volume(0.3)

    def __init__(self, window):
        self.window = window
        self.map_image = pygame.image.load(GAME_ASSETS["dungeon_map"]).convert_alpha()
        self.map_image = pygame.transform.scale(self.map_image, (self.window.get_width(), self.window.get_height()))
        self.player_images = {
            'Warrior': pygame.image.load(GAME_ASSETS['warrior']).convert_alpha(),
            'Mage': pygame.image.load(GAME_ASSETS['mage']).convert_alpha(),
            'Rogue': pygame.image.load(GAME_ASSETS["rogue"]).convert_alpha()
        }
        self.player_type = None
        self.player_position = [self.window.get_width() / 2, self.window.get_height() / 2]
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
        self.player_character = None
        self.selected_character = None

        # New attribute to track highlighted enemies
        self.highlighted_enemies = []

        # New attributes to track last movement direction
        self.last_direction = pygame.math.Vector2(0, 0)
        self.warrior_boost_active = False
        self.boost_start_time = 0

    def load_player(self, character_type):
        self.player_type = character_type
        self.player_image = self.player_images[character_type]
        self.player_image = pygame.transform.scale(self.player_image, (int(self.player_image.get_width() * 0.15), int(self.player_image.get_height() * 0.15)))
        self.player_character = Character("Hero", character_type, armor=5)
        self.selected_character = self.player_type

    def check_for_combat(self):
        for enemy in self.enemies:
            if pygame.math.Vector2(enemy.position).distance_to(self.player_position) < 50:  
                self.in_combat = True
                self.current_enemy = enemy
                return True
            elif 250 > pygame.math.Vector2(enemy.position).distance_to(self.player_position) > 50 and self.selected_character == "Mage":
                self.in_combat = True
                self.current_enemy = enemy
                return True
        return False

    def handle_combat(self):
        if self.in_combat and self.current_enemy:
            player_damage = random.randint(1, 2) * (1.25 ** self.player_character.level) * 0
            print(self.selected_character)
            self.player_character.gain_experience(5)
            enemy_defeated = self.current_enemy.take_damage(player_damage)
            print(f"Player attacks! Deals {player_damage} damage to the enemy.")
            if enemy_defeated:
                print("Enemy defeated!")
                self.enemies.remove(self.current_enemy)
                self.in_combat = False
                self.current_enemy = None

                if not self.enemies:
                    self.spawn_blue_orb()
            else:
                enemy_damage = random.randint(5, 10)
                self.player_character.take_damage(enemy_damage)
                print(f"Enemy attacks back! Deals {enemy_damage} damage to the player.")

    def spawn_blue_orb(self):
        self.blue_orb = pygame.image.load(GAME_ASSETS["blue_orb"]).convert_alpha()
        self.blue_orb = pygame.transform.scale(self.blue_orb, (50, 50))
        self.orb_position = [self.window.get_width() / 2 - 25, self.window.get_height() / 2 - 25]

    def check_orb_collision(self):
        if self.blue_orb and pygame.math.Vector2(self.orb_position).distance_to(self.player_position) < 25:
            self.game_over = True
            print("YOU WIN")
            return True
        return False

    def dash(self):
        if self.selected_character == "Rogue":
            # Use the last direction for dashing
            if self.last_direction.length() == 0:
                return  # No movement direction available

            dash_distance = 75
            dash_vector = self.last_direction * dash_distance

            # Update player position
            self.player_position[0] += dash_vector.x
            self.player_position[1] += dash_vector.y
            print(f"New Player Position: {self.player_position}")

            # Deal damage to the enemy
            if self.in_combat and self.current_enemy:
                self.current_enemy.take_damage(30) * (1.25 ** self.player_character.level)
                pygame.mixer.music.load("Slash8-Bit.ogg")
                pygame.mixer.music.play(1)

    def rapid_fire(self):
        if self.in_combat and self.current_enemy:
            for _ in range(5):  # 5 rapid attacks
                pygame.time.wait(100)  # Short delay between attacks
                player_damage = random.randint(1, 2) * (1.25 ** self.player_character.level)
                self.current_enemy.take_damage(player_damage)
                print(f"Warrior attacks! Deals {player_damage} damage to the enemy.")
            pygame.mixer.music.load("SmallExplosion8-Bit.ogg")
            pygame.mixer.music.play(5)

    def handle_events(self):
        if self.game_over:
            return 'quit'
        keys = pygame.key.get_pressed()
        move_speed = 2
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_position[0] -= move_speed
            self.last_direction = pygame.math.Vector2(-1, 0)  # Left direction
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_position[0] += move_speed
            self.last_direction = pygame.math.Vector2(1, 0)  # Right direction
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player_position[1] -= move_speed
            self.last_direction = pygame.math.Vector2(0, -1)  # Up direction
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player_position[1] += move_speed
            self.last_direction = pygame.math.Vector2(0, 1)  # Down direction

        if keys[pygame.K_q]:
            if self.selected_character == "Mage":
                if self.in_combat and self.current_enemy:
                    self.current_enemy.take_damage(40) * (1.25 ** self.player_character.level)
                    pygame.mixer.music.load("ChargedLightningAttack8-Bit.ogg")
                    pygame.mixer.music.play(1)
                    # Highlight the current enemy
                    self.highlighted_enemies.append((self.current_enemy, pygame.time.get_ticks()))
            elif self.selected_character == "Rogue":
                if self.in_combat and self.current_enemy:
                    self.dash()
            elif self.selected_character == "Warrior":
                if self.in_combat and self.current_enemy:
                    if not self.warrior_boost_active:
                        # Activate boost
                        self.warrior_boost_active = True
                        self.boost_start_time = pygame.time.get_ticks()
                        self.rapid_fire()

        # Handle movement boost
        if self.warrior_boost_active:
            elapsed_time = pygame.time.get_ticks() - self.boost_start_time
            if elapsed_time > 3000:  # Boost lasts for 3 seconds
                self.warrior_boost_active = False
                print("Warrior boost ended.")

        if not self.in_combat:
            if self.check_for_combat():
                return
        self.handle_combat()

        if self.blue_orb and self.check_orb_collision():
            return 'quit'

    def draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.map_image, (0, 0))
        self.window.blit(self.player_image, (self.player_position[0], self.player_position[1]))

        if self.player_character:
            self.player_character.draw_health_bar(self.window, (self.player_position[0], self.player_position[1]))
            player_image_height = self.player_image.get_height()
            self.player_character.draw_xp_bar(self.window, self.player_position, player_image_height)

        for enemy in self.enemies:
            enemy.draw()
        
        # Draw the yellow rectangle for the highlighted enemies
        current_time = pygame.time.get_ticks()
        to_remove = []
        for highlighted_enemy, timestamp in self.highlighted_enemies:
            if current_time - timestamp < 1000:  # Highlight for 1 second
                pygame.draw.rect(self.window, (255, 255, 0), pygame.Rect(highlighted_enemy.position[0], highlighted_enemy.position[1] - 20, 60, 10))  # Adjust rectangle position and size as needed
            else:
                to_remove.append((highlighted_enemy, timestamp))
        
        # Remove expired highlights
        for item in to_remove:
            if item in self.highlighted_enemies:
                self.highlighted_enemies.remove(item)

        if self.blue_orb:
            self.window.blit(self.blue_orb, self.orb_position)

        pygame.display.flip()


