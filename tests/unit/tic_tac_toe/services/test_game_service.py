"""Unit tests for GameService."""
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from tic_tac_toe.services.game_service_core import GameService
from tic_tac_toe.models.player import Player
from tic_tac_toe.models.game_status import GameStatus
from tic_tac_toe.models.value_objects import GridCoordinate


class TestGameService:
    """Test suite for GameService."""

    def test_service_initialization(self):
        """Test that game service initializes correctly."""
        service = GameService()
        
        assert service.get_current_player() is Player.X
        assert service.get_game_status() is GameStatus.IN_PROGRESS
        assert service.get_winner() is None
        assert not service.is_game_over()

    def test_start_new_game(self):
        """Test starting a new game."""
        service = GameService()
        
        # Make a move first
        coordinate = GridCoordinate(0, 0)
        service.make_move(coordinate)
        
        # Start new game
        game_state = service.start_new_game()
        
        assert game_state.current_player is Player.X
        assert game_state.status is GameStatus.IN_PROGRESS
        assert len(service.get_move_history()) == 0

    def test_make_valid_move(self):
        """Test making a valid move."""
        service = GameService()
        coordinate = GridCoordinate(1, 1)
        
        success, message = service.make_move(coordinate)
        
        assert success is True
        assert "successful" in message.lower()
        assert service.get_current_player() is Player.O  # Should switch to O

    def test_make_invalid_move_occupied_cell(self):
        """Test making a move to an occupied cell."""
        service = GameService()
        coordinate = GridCoordinate(1, 1)
        
        # Make first move
        service.make_move(coordinate)
        
        # Try to move to same cell
        success, message = service.make_move(coordinate)
        
        assert success is False
        assert "invalid" in message.lower() or "occupied" in message.lower()

    def test_make_move_out_of_bounds(self):
        """Test making a move out of bounds."""
        service = GameService()
        
        # Test various out of bounds coordinates
        invalid_coords = [
            GridCoordinate(3, 0),  # Row too high
            GridCoordinate(0, 3),  # Column too high
        ]
        
        for coord in invalid_coords:
            success, message = service.make_move(coord)
            assert success is False

    def test_make_move_with_invalid_coordinates(self):
        """Test that negative coordinates raise ValueError during creation."""
        import pytest
        
        # These should raise ValueError during GridCoordinate creation
        with pytest.raises(ValueError):
            GridCoordinate(-1, 0)  # Negative row
            
        with pytest.raises(ValueError):
            GridCoordinate(0, -1)  # Negative column

    def test_get_move_history(self):
        """Test getting move history."""
        service = GameService()
        
        coord1 = GridCoordinate(0, 0)
        coord2 = GridCoordinate(1, 1)
        
        service.make_move(coord1)
        service.make_move(coord2)
        
        history = service.get_move_history()
        
        assert len(history) == 2
        assert history[0].coordinate == coord1
        assert history[0].player is Player.X
        assert history[1].coordinate == coord2
        assert history[1].player is Player.O

    def test_winning_game_horizontal(self):
        """Test winning the game with horizontal line."""
        service = GameService()
        
        # X wins with top row
        moves = [
            (GridCoordinate(0, 0), Player.X),  # X
            (GridCoordinate(1, 0), Player.O),  # O
            (GridCoordinate(0, 1), Player.X),  # X
            (GridCoordinate(1, 1), Player.O),  # O
            (GridCoordinate(0, 2), Player.X),  # X wins
        ]
        
        for coordinate, expected_player in moves[:-1]:
            service.make_move(coordinate)
        
        # Final winning move
        success, message = service.make_move(moves[-1][0])
        
        assert success is True
        assert service.is_game_over()
        assert service.get_winner() is Player.X

    def test_can_restart_after_game_over(self):
        """Test that restart is only allowed after game over."""
        service = GameService()
        
        # Complete a game quickly (X wins)
        moves = [
            GridCoordinate(0, 0), GridCoordinate(1, 0),  # X, O
            GridCoordinate(0, 1), GridCoordinate(1, 1),  # X, O  
            GridCoordinate(0, 2)  # X wins
        ]
        
        for move in moves:
            service.make_move(move)
        
        assert service.is_game_over()
        assert service.can_restart()

    def test_cannot_restart_during_game(self):
        """Test that restart is not allowed during active game."""
        service = GameService()
        
        # Make one move
        service.make_move(GridCoordinate(0, 0))
        
        assert not service.is_game_over()
        assert not service.can_restart()

    def test_status_message_generation(self):
        """Test that status messages are generated correctly."""
        service = GameService()
        
        # Test successful move message
        success, message = service.make_move(GridCoordinate(1, 1))
        assert success is True
        assert isinstance(message, str)
        assert len(message) > 0
        
        # Test invalid move message
        success, message = service.make_move(GridCoordinate(1, 1))  # Same cell
        assert success is False
        assert isinstance(message, str)
        assert len(message) > 0
