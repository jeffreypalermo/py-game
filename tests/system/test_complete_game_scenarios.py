"""System tests for tic-tac-toe game - Complete UI simulation tests."""
import sys
from pathlib import Path
import pytest
import pygame
from unittest.mock import Mock, patch
from typing import List, Tuple, Optional

# Add src to Python path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from tic_tac_toe.controllers.game_controller import GameController
from tic_tac_toe.models.value_objects import Dimensions, ScreenPosition, GridCoordinate
from tic_tac_toe.models.player import Player
from tic_tac_toe.models.game_status import GameStatus
from tic_tac_toe.ui.input_handler import InputData, InputEvent


class GameSimulator:
    """Simulates complete games through UI interactions."""
    
    def __init__(self, dimensions: Dimensions = None):
        self.dimensions = dimensions or Dimensions(600, 600)
        # Initialize pygame in headless mode for testing
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.NOFRAME)
        self.controller = GameController(self.dimensions)
        
    def calculate_cell_center(self, row: int, col: int) -> ScreenPosition:
        """Calculate the center point of a grid cell for mouse clicking."""
        renderer = self.controller.renderer
        x = renderer.grid_offset_x + (col * renderer.cell_size) + (renderer.cell_size // 2)
        y = renderer.grid_offset_y + (row * renderer.cell_size) + (renderer.cell_size // 2)
        return ScreenPosition(x, y)
    
    def simulate_mouse_click(self, row: int, col: int):
        """Simulate a mouse click at the specified grid position."""
        position = self.calculate_cell_center(row, col)
        self.controller._handle_mouse_click(position)
    
    def simulate_restart(self):
        """Simulate a restart command."""
        self.controller._handle_restart()
    
    def play_game_sequence(self, moves: List[Tuple[int, int]]) -> GameStatus:
        """Play a complete game sequence and return the final status."""
        self.controller.game_service.start_new_game()
        
        for row, col in moves:
            if not self.controller.game_service.is_game_over():
                self.simulate_mouse_click(row, col)
        
        return self.controller.game_service.get_game_status()
    
    def get_current_player(self) -> Player:
        """Get the current player."""
        return self.controller.game_service.get_current_player()
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.controller.game_service.is_game_over()
    
    def get_winner(self) -> Optional[Player]:
        """Get the winner of the game."""
        return self.controller.game_service.get_winner()


@pytest.fixture
def game_simulator():
    """Provide a fresh game simulator for each test."""
    return GameSimulator()


class TestXWinningScenarios:
    """Test all scenarios where X should win."""
    
    def test_x_wins_top_row(self, game_simulator):
        """Test X winning with top row (0,0), (0,1), (0,2)."""
        moves = [
            (0, 0),  # X
            (1, 0),  # O
            (0, 1),  # X
            (1, 1),  # O
            (0, 2),  # X wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.X_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.X
    
    def test_x_wins_middle_row(self, game_simulator):
        """Test X winning with middle row (1,0), (1,1), (1,2)."""
        moves = [
            (1, 0),  # X
            (0, 0),  # O
            (1, 1),  # X
            (0, 1),  # O
            (1, 2),  # X wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.X_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.X
    
    def test_x_wins_bottom_row(self, game_simulator):
        """Test X winning with bottom row (2,0), (2,1), (2,2)."""
        moves = [
            (2, 0),  # X
            (0, 0),  # O
            (2, 1),  # X
            (0, 1),  # O
            (2, 2),  # X wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.X_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.X
    
    def test_x_wins_left_column(self, game_simulator):
        """Test X winning with left column (0,0), (1,0), (2,0)."""
        moves = [
            (0, 0),  # X
            (0, 1),  # O
            (1, 0),  # X
            (0, 2),  # O
            (2, 0),  # X wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.X_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.X
    
    def test_x_wins_middle_column(self, game_simulator):
        """Test X winning with middle column (0,1), (1,1), (2,1)."""
        moves = [
            (0, 1),  # X
            (0, 0),  # O
            (1, 1),  # X
            (0, 2),  # O
            (2, 1),  # X wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.X_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.X
    
    def test_x_wins_right_column(self, game_simulator):
        """Test X winning with right column (0,2), (1,2), (2,2)."""
        moves = [
            (0, 2),  # X
            (0, 0),  # O
            (1, 2),  # X
            (0, 1),  # O
            (2, 2),  # X wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.X_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.X
    
    def test_x_wins_main_diagonal(self, game_simulator):
        """Test X winning with main diagonal (0,0), (1,1), (2,2)."""
        moves = [
            (0, 0),  # X
            (0, 1),  # O
            (1, 1),  # X
            (0, 2),  # O
            (2, 2),  # X wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.X_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.X
    
    def test_x_wins_anti_diagonal(self, game_simulator):
        """Test X winning with anti-diagonal (0,2), (1,1), (2,0)."""
        moves = [
            (0, 2),  # X
            (0, 0),  # O
            (1, 1),  # X
            (0, 1),  # O
            (2, 0),  # X wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.X_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.X
    
    def test_x_wins_complex_sequence_1(self, game_simulator):
        """Test X winning in a complex game sequence."""
        moves = [
            (1, 1),  # X center
            (0, 0),  # O corner
            (0, 1),  # X
            (2, 1),  # O
            (2, 0),  # X
            (0, 2),  # O
            (1, 0),  # X
            (1, 2),  # O
            (2, 2),  # X - this should result in a TIE, not X win
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.TIE  # Fixed: this sequence results in a tie
        assert game_simulator.is_game_over()
    
    def test_x_wins_early_sequence(self, game_simulator):
        """Test X winning quickly in 5 moves."""
        moves = [
            (1, 1),  # X center
            (0, 0),  # O
            (0, 1),  # X
            (2, 0),  # O
            (2, 1),  # X wins (vertical middle column)
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.X_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.X


class TestOWinningScenarios:
    """Test all scenarios where O should win."""
    
    def test_o_wins_top_row(self, game_simulator):
        """Test O winning with top row (0,0), (0,1), (0,2)."""
        moves = [
            (1, 0),  # X
            (0, 0),  # O
            (1, 1),  # X
            (0, 1),  # O
            (2, 2),  # X
            (0, 2),  # O wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.O_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.O
    
    def test_o_wins_middle_row(self, game_simulator):
        """Test O winning with middle row (1,0), (1,1), (1,2)."""
        moves = [
            (0, 0),  # X
            (1, 0),  # O
            (0, 1),  # X
            (1, 1),  # O
            (2, 2),  # X
            (1, 2),  # O wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.O_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.O
    
    def test_o_wins_bottom_row(self, game_simulator):
        """Test O winning with bottom row (2,0), (2,1), (2,2)."""
        moves = [
            (0, 0),  # X
            (2, 0),  # O
            (0, 1),  # X
            (2, 1),  # O
            (1, 0),  # X
            (2, 2),  # O wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.O_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.O
    
    def test_o_wins_left_column(self, game_simulator):
        """Test O winning with left column (0,0), (1,0), (2,0)."""
        moves = [
            (0, 1),  # X
            (0, 0),  # O
            (0, 2),  # X
            (1, 0),  # O
            (1, 1),  # X
            (2, 0),  # O wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.O_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.O
    
    def test_o_wins_middle_column(self, game_simulator):
        """Test O winning with middle column (0,1), (1,1), (2,1)."""
        moves = [
            (0, 0),  # X
            (0, 1),  # O
            (0, 2),  # X
            (1, 1),  # O
            (1, 0),  # X
            (2, 1),  # O wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.O_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.O
    
    def test_o_wins_right_column(self, game_simulator):
        """Test O winning with right column (0,2), (1,2), (2,2)."""
        moves = [
            (0, 0),  # X
            (0, 2),  # O
            (0, 1),  # X
            (1, 2),  # O
            (1, 0),  # X
            (2, 2),  # O wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.O_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.O
    
    def test_o_wins_main_diagonal(self, game_simulator):
        """Test O winning with main diagonal (0,0), (1,1), (2,2)."""
        moves = [
            (0, 1),  # X
            (0, 0),  # O
            (0, 2),  # X
            (1, 1),  # O
            (1, 0),  # X
            (2, 2),  # O wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.O_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.O
    
    def test_o_wins_anti_diagonal(self, game_simulator):
        """Test O winning with anti-diagonal (0,2), (1,1), (2,0)."""
        moves = [
            (0, 0),  # X
            (0, 2),  # O
            (0, 1),  # X
            (1, 1),  # O
            (1, 0),  # X
            (2, 0),  # O wins
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.O_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.O
    
    def test_o_wins_defensive_play(self, game_simulator):
        """Test O winning after blocking X's attempts."""
        moves = [
            (0, 0),  # X
            (1, 1),  # O (center)
            (0, 1),  # X
            (0, 2),  # O (blocks X's top row)
            (1, 0),  # X
            (2, 0),  # O wins (completes left column)
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.O_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.O
    
    def test_o_wins_counterattack(self, game_simulator):
        """Test O winning by counterattacking after X's opening."""
        moves = [
            (1, 1),  # X (center)
            (0, 0),  # O (corner)
            (2, 2),  # X (opposite corner)
            (0, 2),  # O
            (1, 0),  # X
            (0, 1),  # O wins (top row)
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.O_WINS
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() == Player.O


class TestTieScenarios:
    """Test all scenarios that should result in a tie."""
    
    def test_tie_scenario_1(self, game_simulator):
        """Test a tie game scenario."""
        moves = [
            (0, 0),  # X
            (0, 1),  # O
            (0, 2),  # X
            (1, 0),  # O
            (1, 2),  # X
            (1, 1),  # O
            (2, 0),  # X
            (2, 2),  # O
            (2, 1),  # X - board full, tie
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.TIE
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() is None
    
    def test_tie_scenario_2(self, game_simulator):
        """Test another tie game scenario."""
        moves = [
            (1, 1),  # X (center)
            (0, 0),  # O (corner)
            (2, 2),  # X (opposite corner)
            (0, 2),  # O
            (2, 0),  # X
            (1, 0),  # O
            (1, 2),  # X
            (2, 1),  # O
            (0, 1),  # X - tie
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.TIE
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() is None
    
    def test_tie_scenario_3(self, game_simulator):
        """Test a defensive tie scenario."""
        moves = [
            (0, 0),  # X
            (1, 1),  # O (center)
            (2, 2),  # X
            (0, 2),  # O (block diagonal)
            (2, 0),  # X (force anti-diagonal threat)
            (1, 0),  # O (block column)
            (0, 1),  # X
            (2, 1),  # O
            (1, 2),  # X - tie
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        
        assert final_status == GameStatus.TIE
        assert game_simulator.is_game_over()
        assert game_simulator.get_winner() is None


class TestGameRestartScenarios:
    """Test game restart functionality through UI simulation."""
    
    def test_restart_after_x_wins(self, game_simulator):
        """Test restarting the game after X wins."""
        # First, play a game where X wins
        moves = [
            (0, 0), (1, 0), (0, 1), (1, 1), (0, 2)  # X wins top row
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        assert final_status == GameStatus.X_WINS
        assert game_simulator.is_game_over()
        
        # Now restart the game
        game_simulator.simulate_restart()
        
        # Verify the game has restarted
        assert not game_simulator.is_game_over()
        assert game_simulator.get_current_player() == Player.X
        assert game_simulator.controller.game_service.get_game_status() == GameStatus.IN_PROGRESS
    
    def test_restart_after_o_wins(self, game_simulator):
        """Test restarting the game after O wins."""
        # First, play a game where O wins
        moves = [
            (1, 0), (0, 0), (1, 1), (0, 1), (2, 2), (0, 2)  # O wins top row
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        assert final_status == GameStatus.O_WINS
        assert game_simulator.is_game_over()
        
        # Now restart the game
        game_simulator.simulate_restart()
        
        # Verify the game has restarted
        assert not game_simulator.is_game_over()
        assert game_simulator.get_current_player() == Player.X
        assert game_simulator.controller.game_service.get_game_status() == GameStatus.IN_PROGRESS
    
    def test_restart_after_tie(self, game_simulator):
        """Test restarting the game after a tie."""
        # First, play a tie game
        moves = [
            (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (1, 1), (2, 0), (2, 2), (2, 1)
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        assert final_status == GameStatus.TIE
        assert game_simulator.is_game_over()
        
        # Now restart the game
        game_simulator.simulate_restart()
        
        # Verify the game has restarted
        assert not game_simulator.is_game_over()
        assert game_simulator.get_current_player() == Player.X
        assert game_simulator.controller.game_service.get_game_status() == GameStatus.IN_PROGRESS


class TestInvalidMoveScenarios:
    """Test invalid move scenarios through UI simulation."""
    
    def test_click_occupied_cell(self, game_simulator):
        """Test clicking on an already occupied cell."""
        # Make initial moves
        game_simulator.simulate_mouse_click(0, 0)  # X
        game_simulator.simulate_mouse_click(1, 1)  # O
        
        # Try to click on an occupied cell
        initial_state = game_simulator.controller.game_service.get_move_history()
        game_simulator.simulate_mouse_click(0, 0)  # Try to click X's position
        
        # Verify no additional move was made
        final_state = game_simulator.controller.game_service.get_move_history()
        assert len(final_state) == len(initial_state)
        assert game_simulator.get_current_player() == Player.X  # Should still be X's turn
    
    def test_click_after_game_over(self, game_simulator):
        """Test clicking after the game is over."""
        # Play a complete game
        moves = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)]  # X wins
        game_simulator.play_game_sequence(moves)
        
        assert game_simulator.is_game_over()
        
        # Try to make another move
        initial_move_count = len(game_simulator.controller.game_service.get_move_history())
        game_simulator.simulate_mouse_click(2, 2)  # Try to click empty cell
        
        # Verify no additional move was made
        final_move_count = len(game_simulator.controller.game_service.get_move_history())
        assert final_move_count == initial_move_count


class TestComplexGameSequences:
    """Test complex and edge-case game sequences."""
    
    def test_all_corners_first(self, game_simulator):
        """Test a game where all corners are played first."""
        moves = [
            (0, 0),  # X top-left
            (0, 2),  # O top-right
            (2, 0),  # X bottom-left
            (2, 2),  # O bottom-right
            (1, 1),  # X center
            (0, 1),  # O top-middle
            (1, 0),  # X middle-left - X wins with left column (0,0)-(1,0)-(2,0)
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        assert final_status == GameStatus.X_WINS  # Fixed: X wins on move 7 with left column
        assert game_simulator.get_winner() == Player.X
    
    def test_alternating_patterns(self, game_simulator):
        """Test games with alternating move patterns."""
        moves = [
            (1, 1),  # X center
            (0, 1),  # O top-middle
            (0, 0),  # X top-left
            (1, 0),  # O middle-left
            (2, 2),  # X bottom-right - X wins main diagonal (0,0)-(1,1)-(2,2)
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        assert final_status == GameStatus.X_WINS
        assert game_simulator.get_winner() == Player.X
    
    def test_defensive_masterclass(self, game_simulator):
        """Test a game with excellent defensive play leading to tie."""
        moves = [
            (0, 0),  # X corner
            (1, 1),  # O center (good defense)
            (2, 2),  # X opposite corner
            (0, 2),  # O block diagonal
            (2, 0),  # X create new threat
            (1, 0),  # O block column
            (0, 1),  # X
            (2, 1),  # O
            (1, 2),  # X - perfect defense leads to tie
        ]
        
        final_status = game_simulator.play_game_sequence(moves)
        assert final_status == GameStatus.TIE
