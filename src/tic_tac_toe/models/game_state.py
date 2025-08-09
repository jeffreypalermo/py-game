from typing import Optional, List
from tic_tac_toe.models.player import Player
from tic_tac_toe.models.game_status import GameStatus
from tic_tac_toe.models.move import Move
from tic_tac_toe.models.game_board import GameBoard
from tic_tac_toe.models.board_validator import BoardValidator
from tic_tac_toe.models.win_checker import WinChecker
from tic_tac_toe.models.value_objects import GridSize, GridCoordinate


class GameState:
    """Represents the current state of the tic-tac-toe game."""
    
    def __init__(self, grid_size: GridSize = None):
        self.grid_size = grid_size or GridSize()
        self._initialize_game_components()
        self._initialize_game_state()
    
    def reset_to_initial_state(self):
        """Reset the game to initial state."""
        self._initialize_game_state()
        self.board.reset_board()
    
    def is_valid_move(self, coordinate: GridCoordinate) -> bool:
        """Check if a move is valid."""
        return (self._is_game_in_progress() and 
                self.validator.is_cell_empty(self.board.board, coordinate))
    
    def execute_move(self, coordinate: GridCoordinate) -> bool:
        """Execute a move at the specified position."""
        if not self.is_valid_move(coordinate):
            return False
        
        self._place_current_player_move(coordinate)
        self._check_for_game_completion()
        self._switch_to_next_player_if_game_continues()
        
        return True
    
    def get_cell(self, coordinate: GridCoordinate) -> Player:
        """Get the player at the specified cell."""
        return self.board.get_cell_player(coordinate)
    
    def _initialize_game_components(self):
        """Initialize the game helper components."""
        self.board = GameBoard(self.grid_size)
        self.validator = BoardValidator(self.grid_size)
        self.win_checker = WinChecker(self.grid_size)
    
    def _initialize_game_state(self):
        """Initialize the core game state variables."""
        self.current_player = Player.X
        self.status = GameStatus.IN_PROGRESS
        self.winner: Optional[Player] = None
        self.move_history: List[Move] = []
    
    def _is_game_in_progress(self) -> bool:
        """Check if the game is still in progress."""
        return self.status == GameStatus.IN_PROGRESS
    
    def _place_current_player_move(self, coordinate: GridCoordinate):
        """Place the current player's move and record it."""
        move = Move(coordinate, self.current_player)
        self.board.place_move(coordinate, self.current_player)
        self.move_history.append(move)
    
    def _check_for_game_completion(self):
        """Check if the game has ended and update status."""
        winner = self.win_checker.check_for_winner(self.board.board)
        if winner:
            self._set_winner_and_end_game(winner)
        elif self.validator.is_board_full(self.board.board):
            self._set_tie_game()
    
    def _set_winner_and_end_game(self, winner: Player):
        """Set the winner and end the game."""
        self.winner = winner
        self.status = GameStatus.X_WINS if winner == Player.X else GameStatus.O_WINS
    
    def _set_tie_game(self):
        """Set the game status to tie."""
        self.status = GameStatus.TIE
    
    def _switch_to_next_player_if_game_continues(self):
        """Switch to the next player if game is still in progress."""
        if self._is_game_in_progress():
            self._switch_current_player()
    
    def _switch_current_player(self):
        """Switch between X and O players."""
        self.current_player = Player.O if self.current_player == Player.X else Player.X
