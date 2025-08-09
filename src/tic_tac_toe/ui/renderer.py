import pygame
from typing import Tuple
from tic_tac_toe.models.player import Player
from tic_tac_toe.models.value_objects import Dimensions, GridCoordinate, ScreenPosition, GridSize


class GameRenderer:
    """Handles all visual rendering for the tic-tac-toe game."""
    
    def __init__(self, dimensions: Dimensions = None):
        self.dimensions = dimensions or Dimensions(600, 600)
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (128, 128, 128)
        
        # Grid configuration
        self.grid_size = GridSize()
        self._calculate_grid_layout()
        
        # Fonts
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
    
    def _calculate_grid_layout(self):
        """Calculate grid layout based on dimensions."""
        min_dimension = min(self.dimensions.width, self.dimensions.height)
        self.cell_size = min_dimension // self.grid_size.size
        self.grid_offset_x = (self.dimensions.width - self.grid_size.size * self.cell_size) // 2
        self.grid_offset_y = (self.dimensions.height - self.grid_size.size * self.cell_size) // 2
    
    def clear_screen(self, screen: pygame.Surface):
        """Clear the screen with background color."""
        screen.fill(self.BLACK)
    
    def draw_grid(self, screen: pygame.Surface):
        """Draw the tic-tac-toe grid."""
        # Draw vertical lines
        for i in range(1, self.grid_size.size):
            x = self.grid_offset_x + i * self.cell_size
            pygame.draw.line(screen, self.WHITE, 
                           (x, self.grid_offset_y), 
                           (x, self.grid_offset_y + self.grid_size.size * self.cell_size), 3)
        
        # Draw horizontal lines
        for i in range(1, self.grid_size.size):
            y = self.grid_offset_y + i * self.cell_size
            pygame.draw.line(screen, self.WHITE, 
                           (self.grid_offset_x, y), 
                           (self.grid_offset_x + self.grid_size.size * self.cell_size, y), 3)
        
        # Draw border
        pygame.draw.rect(screen, self.WHITE, 
                        (self.grid_offset_x, self.grid_offset_y, 
                         self.grid_size.size * self.cell_size, self.grid_size.size * self.cell_size), 3)
    
    def draw_x(self, screen: pygame.Surface, coordinate: GridCoordinate):
        """Draw an X symbol in the specified grid cell."""
        x = self.grid_offset_x + coordinate.col * self.cell_size
        y = self.grid_offset_y + coordinate.row * self.cell_size
        margin = self.cell_size // 6
        
        # Draw X as two diagonal lines
        pygame.draw.line(screen, self.RED, 
                        (x + margin, y + margin), 
                        (x + self.cell_size - margin, y + self.cell_size - margin), 5)
        pygame.draw.line(screen, self.RED, 
                        (x + self.cell_size - margin, y + margin), 
                        (x + margin, y + self.cell_size - margin), 5)
    
    def draw_o(self, screen: pygame.Surface, coordinate: GridCoordinate):
        """Draw an O symbol in the specified grid cell."""
        x = self.grid_offset_x + coordinate.col * self.cell_size
        y = self.grid_offset_y + coordinate.row * self.cell_size
        center_x = x + self.cell_size // 2
        center_y = y + self.cell_size // 2
        radius = self.cell_size // 3
        
        # Draw O as a circle
        pygame.draw.circle(screen, self.BLUE, (center_x, center_y), radius, 5)
    
    def draw_symbol(self, screen: pygame.Surface, coordinate: GridCoordinate, player: Player):
        """Draw the appropriate symbol for the given player."""
        if player == Player.X:
            self.draw_x(screen, coordinate)
        elif player == Player.O:
            self.draw_o(screen, coordinate)
    
    def draw_status_message(self, screen: pygame.Surface, message: str, color: Tuple[int, int, int] = None):
        """Draw a status message at the top of the screen."""
        if color is None:
            color = self.GREEN
            
        text_surface = self.font_medium.render(message, True, color)
        text_rect = text_surface.get_rect(center=(self.dimensions.width // 2, 50))
        screen.blit(text_surface, text_rect)
    
    def draw_instructions(self, screen: pygame.Surface, instructions: str):
        """Draw instruction text at the bottom of the screen."""
        text_surface = self.font_small.render(instructions, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(self.dimensions.width // 2, self.dimensions.height - 30))
        screen.blit(text_surface, text_rect)
    
    def screen_to_grid_coordinates(self, position: ScreenPosition) -> GridCoordinate:
        """Convert screen coordinates to grid coordinates."""
        grid_col = (position.x - self.grid_offset_x) // self.cell_size
        grid_row = (position.y - self.grid_offset_y) // self.cell_size
        return GridCoordinate(grid_row, grid_col)
    
    def is_click_in_grid(self, position: ScreenPosition) -> bool:
        """Check if a mouse click is within the game grid."""
        coordinate = self.screen_to_grid_coordinates(position)
        return self.grid_size.is_valid_coordinate(coordinate)
