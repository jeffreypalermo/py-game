"""Unit tests for Move class."""
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from tic_tac_toe.models.move import Move
from tic_tac_toe.models.player import Player
from tic_tac_toe.models.value_objects import GridCoordinate


class TestMove:
    """Test cases for Move class."""

    def test_move_creation(self):
        """Test creating a valid move."""
        coordinate = GridCoordinate(1, 2)
        move = Move(coordinate, Player.X)
        
        assert move.coordinate == coordinate
        assert move.player == Player.X

    def test_move_row_property(self):
        """Test backward compatibility row property."""
        coordinate = GridCoordinate(1, 2)
        move = Move(coordinate, Player.X)
        
        assert move.row == 1

    def test_move_col_property(self):
        """Test backward compatibility col property."""
        coordinate = GridCoordinate(1, 2)
        move = Move(coordinate, Player.X)
        
        assert move.col == 2

    def test_move_string_representation(self):
        """Test string representation of move."""
        coordinate = GridCoordinate(1, 2)
        move = Move(coordinate, Player.O)
        
        str_repr = str(move)
        assert "coordinate=GridCoordinate(row=1, col=2)" in str_repr
        assert "player=Player.O" in str_repr

    def test_move_with_different_players(self):
        """Test moves with different players."""
        coordinate = GridCoordinate(0, 0)
        
        move_x = Move(coordinate, Player.X)
        move_o = Move(coordinate, Player.O)
        
        assert move_x.player == Player.X
        assert move_o.player == Player.O
        assert move_x.coordinate == move_o.coordinate

    def test_move_with_different_coordinates(self):
        """Test moves with different coordinates."""
        coord1 = GridCoordinate(0, 0)
        coord2 = GridCoordinate(2, 2)
        
        move1 = Move(coord1, Player.X)
        move2 = Move(coord2, Player.X)
        
        assert move1.coordinate != move2.coordinate
        assert move1.player == move2.player
