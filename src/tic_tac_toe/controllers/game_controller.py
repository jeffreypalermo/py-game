import pygame
import sys
from typing import Tuple

from tic_tac_toe.models import Player, GameStatus, Dimensions, ScreenPosition, GridCoordinate
from tic_tac_toe.services import GameService, GameAnalyticsService
from tic_tac_toe.ui.renderer import GameRenderer
from tic_tac_toe.ui.input_handler import InputHandler, InputEvent


class GameController:
    """Main controller that orchestrates the tic-tac-toe game."""
    
    def __init__(self, dimensions: Dimensions = None):
        # Initialize pygame
        pygame.init()
        
        # Initialize dimensions
        self.dimensions = dimensions or Dimensions(600, 600)
        
        # Initialize components
        self.screen = pygame.display.set_mode(self.dimensions.to_tuple())
        pygame.display.set_caption("Tic-Tac-Toe Business Application")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize services and UI components
        self.game_service = GameService()
        self.analytics_service = GameAnalyticsService(self.game_service.get_game_state())
        self.renderer = GameRenderer(self.dimensions)
        self.input_handler = InputHandler()
        
        # Start the first game
        self.game_service.start_new_game()
    
    def run(self):
        """Main game loop."""
        while self.running:
            self._handle_input()
            self._update()
            self._render()
            self.clock.tick(60)  # 60 FPS
        
        self._cleanup()
    
    def _handle_input(self):
        """Process all input events."""
        input_events = self.input_handler.process_events()
        
        for input_event in input_events:
            if input_event.event_type == InputEvent.QUIT:
                self.running = False
            
            elif input_event.event_type == InputEvent.RESTART:
                self._handle_restart()
            
            elif input_event.event_type == InputEvent.MOUSE_CLICK:
                self._handle_mouse_click(input_event.data["position"])
    
    def _handle_mouse_click(self, position: ScreenPosition):
        """Handle mouse click events."""
        if not self.renderer.is_click_in_grid(position):
            return
        
        coordinate = self.renderer.screen_to_grid_coordinates(position)
        success, message = self.game_service.make_move(coordinate)
        
        # If the game just ended, record the result
        if success and self.game_service.is_game_over():
            self.analytics_service.record_game_result(self.game_service.get_game_status())
    
    def _handle_restart(self):
        """Handle restart game request."""
        if self.game_service.can_restart():
            self.game_service.start_new_game()
    
    def _update(self):
        """Update game logic."""
        # In this simple game, most updates are handled by the service layer
        # This method could be expanded for animations, AI players, etc.
        pass
    
    def _render(self):
        """Render the current game state."""
        # Clear screen
        self.renderer.clear_screen(self.screen)
        
        # Draw game grid
        self.renderer.draw_grid(self.screen)
        
        # Draw symbols on the board
        game_state = self.game_service.get_game_state()
        for row in range(game_state.grid_size.size):
            for col in range(game_state.grid_size.size):
                coordinate = GridCoordinate(row, col)
                player = game_state.get_cell(coordinate)
                if player != Player.NONE:
                    self.renderer.draw_symbol(self.screen, coordinate, player)
        
        # Draw status message
        status_message = self.game_service.get_status_message()
        message_color = self._get_status_color()
        self.renderer.draw_status_message(self.screen, status_message, message_color)
        
        # Draw instructions
        if self.game_service.is_game_over():
            instructions = "Press R to restart or ESC to exit"
        else:
            instructions = "Click to place symbol - Press ESC to exit"
        
        self.renderer.draw_instructions(self.screen, instructions)
        
        # Update display
        pygame.display.flip()
    
    def _get_status_color(self) -> Tuple[int, int, int]:
        """Get the appropriate color for the status message."""
        status = self.game_service.get_game_status()
        
        if status == GameStatus.X_WINS:
            return self.renderer.RED
        elif status == GameStatus.O_WINS:
            return self.renderer.BLUE
        elif status == GameStatus.TIE:
            return self.renderer.WHITE
        else:
            return self.renderer.GREEN
    
    def _cleanup(self):
        """Clean up resources before exiting."""
        # Print final statistics
        stats = self.analytics_service.get_statistics()
        print(f"\nGame Statistics:")
        print(f"Games played: {stats['games_played']}")
        print(f"X wins: {stats['x_wins']} ({stats['x_win_rate']:.1f}%)")
        print(f"O wins: {stats['o_wins']} ({stats['o_win_rate']:.1f}%)")
        print(f"Ties: {stats['ties']} ({stats['tie_rate']:.1f}%)")
        
        pygame.quit()
        sys.exit()
