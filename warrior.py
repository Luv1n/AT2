
from character import Character

class Warrior(Character):
    def __init__(self, name, max_hp):
        super().__init__(name, "Warrior", armor=10, max_hp=max_hp)
        self.max_stamina = 100
        self.current_stamina = self.max_stamina
        self.stamina_regeneration = 10
        self.strength = 15
        self.attacks = {
            "Basic Attack": {"method": self.basic_attack, "stamina_cost": 10},
            "Charge": {"method": self.charge, "stamina_cost": 20},
            "Cleave Attack": {"method": self.cleave_attack, "stamina_cost": 30},
            "Shield Bash": {"method": self.shield_bash, "stamina_cost": 15},
            "Defensive Stance": {"method": self.defensive_stance, "stamina_cost": 5},
        }

    def choose_attack(self, target):
        print(f"Choose an attack (Current stamina: {self.current_stamina}):")
        attack_list = list(self.attacks.items())
        for i, (attack, info) in enumerate(attack_list):
            print(f"{i + 1}. {attack} (Stamina cost: {info['stamina_cost']})")
        chosen_attack = int(input("Enter the number of the attack: "))
        if 1 <= chosen_attack <= len(attack_list):
            attack, attack_info = attack_list[chosen_attack - 1]
            if self.current_stamina >= attack_info["stamina_cost"]:
                self.current_stamina -= attack_info["stamina_cost"]
                attack_method = attack_info["method"]
                attack_method(target)
            else:
                print("Not enough stamina for this attack.")
        else:
            print("Invalid attack.")

    def regenerate_stamina(self):
        self.current_stamina = min(self.max_stamina, self.current_stamina + self.stamina_regeneration)

    def attack(self, target):
        damage = self.strength * self.level
        target.take_damage(damage)
        return damage

    def charge(self, target):
        print(f"{self.name} charges towards {target.name}!")
        target.take_damage(self.strength)

    def basic_attack(self, target):
        damage = self.strength
        print(f"{self.name} performs a basic attack on {target} for {damage} damage!")
        target.take_damage(damage)

    def cleave_attack(self, targets):
        total_damage = 0
        for target in targets:
            damage = self.strength * 2
            total_damage += damage
            print(f"{self.name} cleaves {target} for {damage} damage!")
            target.take_damage(damage)
        print(f"{self.name} dealt a total of {total_damage} damage with cleave!")

    def shield_bash(self, target):
        damage = self.strength + 5
        print(f"{self.name} performs a shield bash on {target} for {damage} damage!")
        target.take_damage(damage)

    def defensive_stance(self):
        self.armor_class += 5
        print(f"{self.name} enters a defensive stance, increasing armor class!")

