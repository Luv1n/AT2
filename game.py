import pygame
from menu import MainMenu
from character_select import CharacterSelect
from map import Map
from assets import load_assets, GAME_ASSETS

class Game:
    def __init__(self):
        pygame.init()
        load_assets()  # Load the game image assets
        self.window = pygame.display.set_mode((800, 600))
        self.menu = MainMenu(self.window)  # Create an instance of the MainMenu class
        self.character_select = CharacterSelect(self.window)  # Create an instance of the CharacterSelect class
        self.game_map = Map(self.window)  # Create an instance of the Map class
        self.state = 'menu'  # Set the initial state to 'menu'
        self.current_character = None  # To store the chosen character

    def run(self):
        while True:
            if self.state == 'menu':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                
                result = self.menu.run()
                if result == 'Start Game':
                    self.state = 'character_select'
                elif result == 'Settings':
                    pass  # Settings handling would go here
                elif result == 'Exit':
                    pygame.quit()
                    return

            elif self.state == 'character_select':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                
                selected_character = self.character_select.run()
                if selected_character == 'back':
                    self.state = 'menu'
                elif selected_character:
                    self.current_character = selected_character
                    self.game_map.load_player(selected_character)
                    self.state = 'game_map'

            elif self.state == 'game_map':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                
                result = self.game_map.handle_events()
                if result == 'back':
                    self.state = 'character_select'
                elif result == 'quit':
                    if self.game_map.game_phase == 2:
                        pygame.quit()
                        return
                else:
                    self.game_map.draw()

if __name__ == "__main__":
    game = Game()
    game.run()
