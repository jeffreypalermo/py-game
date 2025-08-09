"""Integration tests for tic-tac-toe game."""
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from tic_tac_toe.services.game_service_core import GameService
from tic_tac_toe.models.player import Player
from tic_tac_toe.models.game_status import GameStatus
from tic_tac_toe.models.value_objects import GridCoordinate


class TestGameIntegration:
    """Integration tests for the complete game flow."""

    def test_complete_game_x_wins(self):
        """Test a complete game where X wins."""
        service = GameService()
        
        # Simulate a game where X wins diagonally
        moves = [
            GridCoordinate(0, 0),  # X
            GridCoordinate(0, 1),  # O
            GridCoordinate(1, 1),  # X
            GridCoordinate(0, 2),  # O
            GridCoordinate(2, 2),  # X wins diagonally
        ]
        
        for i, coordinate in enumerate(moves):
            expected_player = Player.X if i % 2 == 0 else Player.O
            
            success, message = service.make_move(coordinate)
            assert success is True
            
            if i < len(moves) - 1:  # Not the last move
                assert not service.is_game_over()
                assert service.get_current_player() != expected_player  # Should switch
        
        # After final move
        assert service.is_game_over()
        assert service.get_winner() is Player.X
        assert service.get_game_status() is GameStatus.X_WINS

    def test_complete_game_tie(self):
        """Test a complete game that ends in a tie."""
        service = GameService()
        
        # Simulate a game that ends in a tie
        moves = [
            GridCoordinate(0, 0),  # X
            GridCoordinate(0, 1),  # O
            GridCoordinate(0, 2),  # X
            GridCoordinate(1, 0),  # O
            GridCoordinate(1, 2),  # X
            GridCoordinate(1, 1),  # O
            GridCoordinate(2, 0),  # X
            GridCoordinate(2, 2),  # O
            GridCoordinate(2, 1),  # X - board full, tie
        ]
        
        for coordinate in moves:
            success, message = service.make_move(coordinate)
            assert success is True
        
        assert service.is_game_over()
        assert service.get_winner() is None
        assert service.get_game_status() is GameStatus.TIE

    def test_game_restart_flow(self):
        """Test the complete game restart flow."""
        service = GameService()
        
        # Play partial game
        service.make_move(GridCoordinate(0, 0))
        service.make_move(GridCoordinate(1, 1))
        
        assert len(service.get_move_history()) == 2
        assert not service.can_restart()  # Game in progress
        
        # Complete the game (X wins)
        service.make_move(GridCoordinate(0, 1))
        service.make_move(GridCoordinate(1, 0))
        service.make_move(GridCoordinate(0, 2))  # X wins
        
        assert service.is_game_over()
        assert service.can_restart()
        
        # Restart game
        new_state = service.start_new_game()
        
        assert new_state.current_player is Player.X
        assert new_state.status is GameStatus.IN_PROGRESS
        assert len(service.get_move_history()) == 0
        assert not service.is_game_over()

    def test_invalid_moves_during_game(self):
        """Test various invalid moves during game play."""
        service = GameService()
        
        # Make valid move
        success, _ = service.make_move(GridCoordinate(1, 1))
        assert success is True
        
        # Try to move to same position
        success, message = service.make_move(GridCoordinate(1, 1))
        assert success is False
        assert "invalid" in message.lower() or "occupied" in message.lower()
        
        # Try out of bounds moves
        invalid_coordinates = [
            GridCoordinate(3, 0),  # Row out of bounds
            GridCoordinate(0, 3),  # Column out of bounds
            GridCoordinate(5, 5),  # Both out of bounds
        ]
        
        for coord in invalid_coordinates:
            success, message = service.make_move(coord)
            assert success is False

    def test_move_history_accuracy(self):
        """Test that move history is accurately maintained."""
        service = GameService()
        
        moves = [
            GridCoordinate(0, 0),
            GridCoordinate(1, 1),
            GridCoordinate(2, 2),
        ]
        
        for i, coordinate in enumerate(moves):
            service.make_move(coordinate)
            
            history = service.get_move_history()
            assert len(history) == i + 1
            
            # Check latest move
            latest_move = history[-1]
            assert latest_move.coordinate == coordinate
            expected_player = Player.X if i % 2 == 0 else Player.O
            assert latest_move.player is expected_player
