from typing import Tuple, Optional
from tic_tac_toe.models import GameState, Player, GameStatus, Move, GridCoordinate


class MoveExecutor:
    """Handles the execution and validation of game moves."""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
    
    def attempt_move(self, coordinate: GridCoordinate) -> Tuple[bool, str]:
        """Attempt to make a move and return result with message."""
        if self._is_game_already_finished():
            return False, "Game is already finished"
        
        if not self._is_move_valid(coordinate):
            return False, "Invalid move: cell is occupied or out of bounds"
        
        return self._execute_valid_move(coordinate)
    
    def _is_game_already_finished(self) -> bool:
        """Check if the game has already ended."""
        return self.game_state.status != GameStatus.IN_PROGRESS
    
    def _is_move_valid(self, coordinate: GridCoordinate) -> bool:
        """Validate if the move can be made."""
        return self.game_state.is_valid_move(coordinate)
    
    def _execute_valid_move(self, coordinate: GridCoordinate) -> Tuple[bool, str]:
        """Execute a validated move and return success status."""
        success = self.game_state.execute_move(coordinate)
        if success:
            return True, self._create_success_message()
        return False, "Failed to make move"
    
    def _create_success_message(self) -> str:
        """Create appropriate success message based on game state."""
        if self.game_state.status == GameStatus.IN_PROGRESS:
            return f"Move successful: {self.game_state.current_player.name}"
        return "Move successful: Game ended"
