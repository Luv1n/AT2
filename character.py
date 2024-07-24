import pygame

class Character:
    MAX_LEVEL = 50  # Maximum level a character can reach
    ATTRIBUTE_POINTS_PER_LEVEL = 3  # Number of attribute points gained per level
    MAX_STAMINA = 100
    def __init__(self, name, character_class, armor):
        self.name = name  # Character's name
        self.character_class = character_class  # Character's class
        self.armor = armor  # Character's armor value
        self.level = 1  # Character's current level
        self.experience_points = 0  # Character's current experience points
        self.hit_points = 10000  # Example starting value for character's hit points
        self.max_hit_points = self.hit_points  # Set max hit points
        self.armor_class = 10  # Example starting value for character's armor class
        self.skills = {}  # Example empty dictionary for character's skills
        self.inventory = []  # Example empty list for character's inventory
        self.gold = 0  # Example starting value for character's gold
        self.attribute_points = 0  # Attribute points available to allocate
        self.font = pygame.font.SysFont('Arial', 24)
        self.stamina = 0
    
    
       
    def heal(self, health):

        self.hit_points += health

    def assign_attribute_points(self, attribute, points):
        # Ensure the attribute exists before assigning points
        if attribute in self.__dict__:
            setattr(self, attribute, getattr(self, attribute) + points)  # Add points to the attribute
            self.attribute_points -= points  # Decrease available attribute points
        else:
            print(f"Error: Attribute '{attribute}' does not exist.")
    def gain_experience(self, experience):
        self.experience_points += experience  # Increase character's experience points
        # Calculate experience required for next level
        required_experience = self.calculate_required_experience(self.level + 1)
        # Check if character has enough experience to level up and is below the level cap
        while self.experience_points >= required_experience and self.level < self.MAX_LEVEL:
            self.level += 1  # Level up the character
            self.experience_points -= required_experience  # Decrease character's experience points
            self.max_hit_points += 10  # Example: Increase max hit points by 10 each level up
            self.hit_points = self.max_hit_points  # Heal to max hit points
            self.attribute_points += self.ATTRIBUTE_POINTS_PER_LEVEL  # Allocate attribute points
            print(f"Level up! {self.name} is now level {self.level}.")
            # Calculate experience required for next level
            required_experience = self.calculate_required_experience(self.level + 1)

    def calculate_required_experience(self, level):
        # Exponential scaling of experience required
        return int(100 * (1.2 ** (level - 1)))


    def is_alive(self):
        return self.hit_points > 0
    def take_damage(self, amount):
        # Calculate the actual damage taken, taking into account the character's armor
        actual_damage = max(0, amount - self.armor)
        self.hit_points -= actual_damage
        if self.hit_points <= 0:
            print(f"{self.name} takes {actual_damage} damage and has been defeated!")
            pygame.quit()
        else:
            print(f"{self.name} takes {actual_damage} damage. Remaining hit points: {self.hit_points}")

    def draw_health_bar(self, window, position):
        health_bar_width = 100  # Example width of the health bar
        health_bar_height = 5  # Example height of the health bar
        health_bar_x = position[0] - (health_bar_width // 2)
        health_bar_y = position[1] - health_bar_height - 10  # 5 pixels above the player image

        health_ratio = self.hit_points / self.max_hit_points
        current_health_bar_width = int(health_bar_width * health_ratio)

        pygame.draw.rect(window, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))  # Red background
        pygame.draw.rect(window, (0, 255, 0), (health_bar_x, health_bar_y, current_health_bar_width, health_bar_height))  # Green foreground

    def draw_xp_bar(self, window, player_position, player_image_height):
        xp_bar_width = 100  # Width of the XP bar
        xp_bar_height = 10  # Height of the XP bar

        # Calculate XP ratio
        current_xp_to_next_level = self.calculate_required_experience(self.level + 1)
        xp_ratio = self.experience_points / current_xp_to_next_level

        # Clamp the XP ratio to a maximum of 1.0
        if xp_ratio > 1.0:
            xp_ratio = 1.0

        current_xp_bar_width = int(xp_bar_width * xp_ratio)

        # Position the XP bar 5 pixels below the player
        xp_bar_x = player_position[0] - (xp_bar_width // 2)  # Center horizontally relative to the player
        xp_bar_y = player_position[1] + player_image_height + 5  # 5 pixels below the player image

        # Draw the XP bar
        pygame.draw.rect(window, (0, 0, 0), (xp_bar_x, xp_bar_y, xp_bar_width, xp_bar_height))  # Black background
        pygame.draw.rect(window, (0, 0, 255), (xp_bar_x, xp_bar_y, current_xp_bar_width, xp_bar_height))  # Blue foreground

        # Render the XP needed for the next level
        xp_needed_text = self.font.render(f"XP Needed: {current_xp_to_next_level - self.experience_points}", True, (255, 255, 255))
        xp_needed_text_rect = xp_needed_text.get_rect()
        xp_needed_text_rect.midbottom = (xp_bar_x + xp_bar_width // 2, xp_bar_y - 20)  # Position above the XP bar

        window.blit(xp_needed_text, xp_needed_text_rect)
