from typing import Optional
from tic_tac_toe.models.player import Player
from tic_tac_toe.models.value_objects import GridSize


class WinChecker:
    """Handles checking for winning conditions in tic-tac-toe."""
    
    def __init__(self, grid_size: GridSize = None):
        self.grid_size = grid_size or GridSize()
    
    def check_for_winner(self, board) -> Optional[Player]:
        """Check if there's a winner on the board."""
        winner = self._check_rows_for_winner(board)
        if winner:
            return winner
            
        winner = self._check_columns_for_winner(board)
        if winner:
            return winner
            
        return self._check_diagonals_for_winner(board)
    
    def _check_rows_for_winner(self, board) -> Optional[Player]:
        """Check all rows for a winning combination."""
        for row in range(self.grid_size.size):
            if self._is_winning_line(board[row][0], board[row][1], board[row][2]):
                return board[row][0]
        return None
    
    def _check_columns_for_winner(self, board) -> Optional[Player]:
        """Check all columns for a winning combination."""
        for col in range(self.grid_size.size):
            if self._is_winning_line(board[0][col], board[1][col], board[2][col]):
                return board[0][col]
        return None
    
    def _check_diagonals_for_winner(self, board) -> Optional[Player]:
        """Check both diagonals for a winning combination."""
        if self._is_winning_line(board[0][0], board[1][1], board[2][2]):
            return board[0][0]
            
        if self._is_winning_line(board[0][2], board[1][1], board[2][0]):
            return board[0][2]
            
        return None
    
    def _is_winning_line(self, cell1: Player, cell2: Player, cell3: Player) -> bool:
        """Check if three cells form a winning line."""
        return cell1 == cell2 == cell3 != Player.NONE
