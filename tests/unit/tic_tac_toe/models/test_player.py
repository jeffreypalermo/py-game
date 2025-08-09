"""Unit tests for Player enum."""
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from tic_tac_toe.models.player import Player


class TestPlayer:
    """Test cases for Player enum."""

    def test_player_values(self):
        """Test that player enum has correct values."""
        assert Player.NONE.value == 0
        assert Player.X.value == 1
        assert Player.O.value == 2

    def test_player_names(self):
        """Test that player enum has correct names."""
        assert Player.NONE.name == "NONE"
        assert Player.X.name == "X"
        assert Player.O.name == "O"

    def test_player_count(self):
        """Test that there are exactly 3 players."""
        assert len(Player) == 3

    def test_player_iteration(self):
        """Test iterating over players."""
        players = list(Player)
        assert players == [Player.NONE, Player.X, Player.O]

    def test_player_comparison(self):
        """Test player comparison."""
        assert Player.X == Player.X
        assert Player.X != Player.O
        assert Player.NONE != Player.X

    def test_player_in_collection(self):
        """Test player membership in collections."""
        active_players = {Player.X, Player.O}
        assert Player.X in active_players
        assert Player.O in active_players
        assert Player.NONE not in active_players
