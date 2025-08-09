from typing import List
from tic_tac_toe.models.player import Player
from tic_tac_toe.models.move import Move
from tic_tac_toe.models.value_objects import GridSize, GridCoordinate


class GameBoard:
    """Manages the game board state and operations."""
    
    def __init__(self, grid_size: GridSize = None):
        self.grid_size = grid_size or GridSize()
        self.board = self._create_empty_board()
    
    def reset_board(self):
        """Reset the board to initial empty state."""
        self.board = self._create_empty_board()
    
    def place_move(self, coordinate: GridCoordinate, player: Player):
        """Place a player's symbol at the specified position."""
        self.board[coordinate.row][coordinate.col] = player
    
    def get_cell_player(self, coordinate: GridCoordinate) -> Player:
        """Get the player occupying the specified cell."""
        if self._is_position_valid(coordinate):
            return self.board[coordinate.row][coordinate.col]
        return Player.NONE
    
    def get_board_copy(self) -> List[List[Player]]:
        """Get a copy of the current board state."""
        return [row[:] for row in self.board]
    
    def _create_empty_board(self) -> List[List[Player]]:
        """Create a new empty game board."""
        return [[Player.NONE for _ in range(self.grid_size.size)] 
                for _ in range(self.grid_size.size)]
    
    def _is_position_valid(self, coordinate: GridCoordinate) -> bool:
        """Check if the position coordinates are valid."""
        return self.grid_size.is_valid_coordinate(coordinate)
