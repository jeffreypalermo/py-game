from tic_tac_toe.models.player import Player
from tic_tac_toe.models.value_objects import GridCoordinate


class Move:
    """Represents a move made by a player."""
    
    def __init__(self, coordinate: GridCoordinate, player: Player):
        self._initialize_move_properties(coordinate, player)
        
    def _initialize_move_properties(self, coordinate: GridCoordinate, player: Player):
        """Initialize the move with coordinate and player."""
        self.coordinate = coordinate
        self.player = player
        
    @property
    def row(self) -> int:
        """Get the row of this move for backward compatibility."""
        return self.coordinate.row
        
    @property 
    def col(self) -> int:
        """Get the column of this move for backward compatibility."""
        return self.coordinate.col
        
    def __repr__(self):
        return self._create_string_representation()
    
    def _create_string_representation(self) -> str:
        """Create a string representation of the move."""
        return f"Move(coordinate={self.coordinate}, player={self.player})"
