from tic_tac_toe.models.player import Player
from tic_tac_toe.models.value_objects import GridSize, GridCoordinate


class BoardValidator:
    """Handles validation operations for the game board."""
    
    def __init__(self, grid_size: GridSize = None):
        self.grid_size = grid_size or GridSize()
    
    def is_valid_position(self, coordinate: GridCoordinate) -> bool:
        """Check if the position is within board boundaries."""
        return self.grid_size.is_valid_coordinate(coordinate)
    
    def is_cell_empty(self, board, coordinate: GridCoordinate) -> bool:
        """Check if the specified cell is empty."""
        if not self.is_valid_position(coordinate):
            return False
        return board[coordinate.row][coordinate.col] == Player.NONE
    
    def is_board_full(self, board) -> bool:
        """Check if the board is completely filled."""
        for row in range(self.grid_size.size):
            if self._has_empty_cell_in_row(board, row):
                return False
        return True
    
    def _is_row_valid(self, row: int) -> bool:
        """Check if row index is within valid range."""
        return 0 <= row < self.grid_size.size
    
    def _is_column_valid(self, col: int) -> bool:
        """Check if column index is within valid range."""
        return 0 <= col < self.grid_size.size
    
    def _has_empty_cell_in_row(self, board, row: int) -> bool:
        """Check if any cell in the row is empty."""
        for col in range(self.grid_size.size):
            if board[row][col] == Player.NONE:
                return True
        return False
