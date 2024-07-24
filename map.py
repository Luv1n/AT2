import random
import pygame
from assets import GAME_ASSETS
from enemy import Enemy
from character import Character

class Map:
    pygame.init()
    pygame.mixer.init()
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
        self.initial_enemies = [
            Enemy(GAME_ASSETS["goblin"], [50, 50], self.window),
            Enemy(GAME_ASSETS["orc"], [self.window.get_width() - 120, 50], self.window),
            Enemy(GAME_ASSETS["skeleton"], [50, self.window.get_height() - 120], self.window),
            Enemy(GAME_ASSETS["skeleton"], [self.window.get_width() - 120, self.window.get_height() - 120], self.window)
        ]
        self.enemies = self.initial_enemies.copy()
        self.in_combat = False
        self.current_enemy = None
        self.blue_orb = None
        self.game_over = False
        self.player_character = None
        self.selected_character = None

        self.highlighted_enemies = []
        self.last_direction = pygame.math.Vector2(0, 0)
        self.warrior_boost_active = False
        self.heal_active = False
        self.heal_start_time = 0
        self.boost_start_time = 0
        self.game_phase = 1
        self.font = pygame.font.Font(None, 36)

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
            elif 100 > pygame.math.Vector2(enemy.position).distance_to(self.player_position) > 50 and self.selected_character == "Rogue":
                self.in_combat = True
                self.current_enemy = enemy
                return True
        return False

    def handle_combat(self):
        if self.in_combat and self.current_enemy:
            player_damage = random.randint(1, 2) * (1.25 ** self.player_character.level) * 0
            print(self.selected_character)
            self.player_character.gain_experience(0)
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
                enemy_damage = random.randint(1, 3)
                self.player_character.take_damage(enemy_damage)
                print(f"Enemy attacks back! Deals {enemy_damage} damage to the player.")

    def spawn_blue_orb(self):
        self.blue_orb = pygame.image.load(GAME_ASSETS["blue_orb"]).convert_alpha()
        self.blue_orb = pygame.transform.scale(self.blue_orb, (50, 50))
        self.orb_position = [self.window.get_width() / 2 - 25, self.window.get_height() / 2 - 25]

    def check_orb_collision(self):
        if self.blue_orb and pygame.math.Vector2(self.orb_position).distance_to(self.player_position) < 25:
            if self.game_phase == 1:
                self.restart_game_with_double_enemies()
                self.game_phase = 2
            else:
                self.game_over = True
                print("YOU WIN")
                return True
        return False

    def restart_game_with_double_enemies(self):
        self.game_phase += 1
        self.enemies = []
        for enemy in self.initial_enemies:
            for _ in range(2):  # Double the number of enemies
                position = self.get_valid_spawn_position()
                self.enemies.append(Enemy(enemy.image_path, position, self.window))
        self.blue_orb = None  # Remove the blue orb
        self.current_enemy = None
        self.in_combat = False
        pygame.mixer.music.load("Metal_Hit.ogg")
        pygame.mixer.music.play(1)
        print(f"Game Phase: {self.game_phase}. Enemies doubled!")

    def get_valid_spawn_position(self):
        while True:
            position = [random.randint(0, self.window.get_width() - 100), random.randint(0, self.window.get_height() - 100)]
            if not any(pygame.math.Vector2(position).distance_to(enemy.position) < 50 for enemy in self.enemies):
                return position

    def dash(self):
        if self.selected_character == "Rogue":
            if self.last_direction.length() == 0:
                return  # No movement direction available

            dash_distance = 25
            dash_vector = self.last_direction * dash_distance

            self.player_position[0] += dash_vector.x
            self.player_position[1] += dash_vector.y
            print(f"New Player Position: {self.player_position}")

            if self.in_combat and self.current_enemy:
                self.current_enemy.take_damage(30 * (1.25 ** self.player_character.level))
                self.player_character.gain_experience(50)
                pygame.mixer.music.load("Slash8-Bit.ogg")
                pygame.mixer.music.play(1)

    def rapid_fire(self):
        if self.in_combat and self.current_enemy:
            for _ in range(5):  # 5 rapid attacks
                pygame.time.wait(100)  # Short delay between attacks
                player_damage = random.randint(1, 2) * (1.25 ** self.player_character.level)
                self.player_character.gain_experience(50)
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

        # Prevent player from moving out of bounds
        player_width, player_height = self.player_image.get_size()
        player_x, player_y = self.player_position
        if player_x < 0:
            self.player_position[0] = 0
        elif player_x > self.window.get_width() - player_width:
            self.player_position[0] = self.window.get_width() - player_width
        if player_y < 0:
            self.player_position[1] = 0
        elif player_y > self.window.get_height() - player_height:
            self.player_position[1] = self.window.get_height() - player_height

        if keys[pygame.K_q]:
            if self.selected_character == "Mage":
                if self.in_combat and self.current_enemy:
                    self.current_enemy.take_damage(40 * (1.25 ** self.player_character.level))
                    self.player_character.gain_experience(50)
                    pygame.mixer.music.load("ChargedLightningAttack8-Bit.ogg")
                    pygame.mixer.music.play(1)
                    self.highlighted_enemies.append((self.current_enemy, pygame.time.get_ticks()))
            elif self.selected_character == "Rogue":
                if self.in_combat and self.current_enemy:
                    self.dash()
            elif self.selected_character == "Warrior":
                if self.in_combat and self.current_enemy:
                    if not self.warrior_boost_active:
                        self.warrior_boost_active = True
                        self.boost_start_time = pygame.time.get_ticks()
                        self.rapid_fire()
       
        if keys[pygame.K_e]:
            self.heal_active = True
            self.heal()
          

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
    def heal(self):
        if self.heal_active:
            elapsed_time = pygame.time.get_ticks() - self.heal_start_time
            if elapsed_time > 10000:
                self.player_character.heal(50)
                print("NOOOOO WAYYYY I JUST HEALED SKIVIVI")
                self.heal_active = False
                

    def draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.map_image, (0, 0))
        self.window.blit(self.player_image, (self.player_position[0], self.player_position[1]))

        if self.player_character:
            self.player_character.draw_health_bar(self.window, (self.player_position[0], self.player_position[1]))
            player_image_height = self.player_image.get_height()
            self.player_character.draw_xp_bar(self.window, self.player_position, player_image_height)

        # Move and draw each enemy
        for enemy in self.enemies:
            enemy.move()  # Update enemy position
            enemy.draw()

        current_time = pygame.time.get_ticks()
        to_remove = []
        for highlighted_enemy, timestamp in self.highlighted_enemies:
            if current_time - timestamp < 1000:  # Highlight for 1 second
                pygame.draw.rect(self.window, (255, 255, 0), pygame.Rect(highlighted_enemy.position[0], highlighted_enemy.position[1] - 20, 60, 10))  # Adjust rectangle position and size as needed
            else:
                to_remove.append((highlighted_enemy, timestamp))

        for item in to_remove:
            if item in self.highlighted_enemies:
                self.highlighted_enemies.remove(item)

        if self.blue_orb:
            self.window.blit(self.blue_orb, self.orb_position)

        # Draw game phase and player level at the top right
        phase_text = f"Game Phase: {self.game_phase}"
        phase_surface = self.font.render(phase_text, True, (255, 255, 255))
        phase_rect = phase_surface.get_rect(topright=(self.window.get_width() - 10, 10))
        self.window.blit(phase_surface, phase_rect)

        if self.player_character:
            level_text = f"Player Level: {self.player_character.level}"
            level_surface = self.font.render(level_text, True, (255, 255, 255))
            level_rect = level_surface.get_rect(topright=(self.window.get_width() - 10, phase_rect.bottom + 10))
            self.window.blit(level_surface, level_rect)

        # Draw control instructions
        controls_text = "Controls: Q = Special Ability | E = Heal"
        controls_surface = self.font.render(controls_text, True, (255, 255, 255))
        controls_rect = controls_surface.get_rect(topright=(self.window.get_width() - 10, self.window.get_height() - 30))
        self.window.blit(controls_surface, controls_rect)

        pygame.display.flip()


   
