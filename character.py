class Character:
    MAX_LEVEL = 50  # Maximum level a character can reach
    ATTRIBUTE_POINTS_PER_LEVEL = 3  # Number of attribute points gained per level

    def __init__(self, name, character_class, armor, max_hp):
        self.name = name  # Character's name
        self.character_class = character_class  # Character's class
        self.armor = armor  # Character's armor value
        self.level = 1  # Character's current level
        self.experience_points = 0  # Character's current experience points
        self.hit_points = max_hp  # Example starting value for character's hit points
        self.max_hp = max_hp
        self.armor_class = 10  # Example starting value for character's armor class
        self.skills = {}  # Example empty dictionary for character's skills
        self.inventory = []  # Example empty list for character's inventory
        self.gold = 0  # Example starting value for character's gold
        self.attribute_points = 0  # Attribute points available to allocate
        self.position = [0, 0]

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
            self.hit_points += 10  # Example: Increase hit points by 10 each level up
            self.attribute_points += self.ATTRIBUTE_POINTS_PER_LEVEL  # Allocate attribute points
            print(f"Level up! {self.name} is now level {self.level}.")
            # Calculate experience required for next level
            required_experience = self.calculate_required_experience(self.level + 1)

    def calculate_required_experience(self, level):
        # Example exponential scaling: Each level requires 100 more experience points than the previous level
        return int(100 * (1.5 ** (level - 1)))

    def is_alive(self):
        return self.hit_points > 0

    def take_damage(self, amount):
        # Calculate the actual damage taken, taking into account the character's armor
        actual_damage = max(0, amount - self.armor)
        self.hit_points -= actual_damage
        if self.hit_points <= 0:
            print(f"{self.name} takes {actual_damage} damage and has been defeated!")
        else:
            print(f"{self.name} takes {actual_damage} damage. Remaining hit points: {self.hit_points}")

    def move(self, direction, speed):
        if direction == 'left':
            self.position[0] -= speed
        elif direction == 'right':
            self.position[0] += speed
        elif direction == 'up':
            self.position[1] -= speed
        elif direction == 'down':
            self.position[1] += speed

    def check_for_combat(self, enemies):
        for enemy in enemies:
            if pygame.math.Vector2(enemy.position).distance_to(self.position) < 50:
                return enemy
        return None

    def handle_combat(self, enemy):
        if enemy:
            player_damage = random.randint(5, 10)
            enemy_defeated = enemy.take_damage(player_damage)
            print(f"Player attacks! Deals {player_damage} damage to the enemy.")
            if enemy_defeated:
                print("Enemy defeated!")
                return True
            else:
                enemy_damage = random.randint(5, 10)
                print(f"Enemy attacks back! Deals {enemy_damage} damage to the player.")
                self.take_damage(enemy_damage)
                return False
        return False


