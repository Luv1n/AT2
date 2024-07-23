import pygame
from assets import GAME_ASSETS

class CharacterSelect:
    """
    A class representing the character selection screen.
    """
    
    def __init__(self, window):
        """
        Initializes the CharacterSelect object.
        Args:
            window (pygame.Surface): The game window surface.
        """
        self.window = window
        self.font = pygame.font.Font(None, 36)
        self.background_image = self.load_image(GAME_ASSETS['main_menu_background'])
        self.background_image = pygame.transform.scale(self.background_image, (self.window.get_width(), self.window.get_height()))
        self.characters = {
            "Warrior": self.load_image(GAME_ASSETS['warrior_button']),
            "Mage": self.load_image(GAME_ASSETS['mage_button']),
            "Rogue": self.load_image(GAME_ASSETS['rogue_button'])
        }
        self.character_buttons = self.setup_character_buttons()
        self.back_button = pygame.Rect(50, self.window.get_height() - 50 - 30, 100, 30)

    def load_image(self, path):
        """
        Load an image from the specified path.
        Args:
            path (str): The path to the image file.
        Returns:
            pygame.Surface: The loaded image.
        """
        try:
            image = pygame.image.load(path).convert_alpha()
            return image
        except pygame.error as e:
            print(f"Error loading image at {path}: {e}")
            return None

    def setup_character_buttons(self):
        """
        Sets up the character buttons.
        Returns:
            dict: A dictionary mapping character names to their button rectangles.
        """
        buttons = {}
        total_spacing = 40
        num_buttons = len(self.characters)
        available_width = self.window.get_width() - total_spacing * (num_buttons + 1)
        button_width = available_width // num_buttons
        max_height = self.window.get_height() // 4

        x = total_spacing
        y = self.window.get_height() // 3 - max_height // 2

        for character, image in self.characters.items():
            if image:
                aspect_ratio = image.get_height() / image.get_width()
                button_height = int(button_width * aspect_ratio)
                button_height = min(button_height, max_height)
                scaled_image = pygame.transform.scale(image, (button_width, button_height))
                buttons[character] = (scaled_image, pygame.Rect(x, y, button_width, button_height))
                x += button_width + total_spacing

        return buttons

    def draw(self):
        """
        Draws the character selection screen elements.
        """
        self.window.blit(self.background_image, (0, 0))
        for character, (image, rect) in self.character_buttons.items():
            self.window.blit(image, rect)

        pygame.draw.rect(self.window, (200, 200, 200), self.back_button)
        back_text = self.font.render('Back', True, (0, 0, 0))
        text_rect = back_text.get_rect(center=self.back_button.center)
        self.window.blit(back_text, text_rect)

    def handle_events(self):
        """
        Handles events in the character selection screen.
        Returns:
            str: The name of the selected character or 'back' if back button is clicked.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.collidepoint(event.pos):
                    return 'back'
                for character, (image, rect) in self.character_buttons.items():
                    if rect.collidepoint(event.pos):
                        return character
        return None

    def run(self):
        """
        Runs the character selection screen loop.
        Returns:
            str: The name of the selected character or 'back' if back button is clicked.
        """
        running = True
        while running:
            self.draw()
            pygame.display.flip()
            result = self.handle_events()
            if result is not None:
                return result
        return None