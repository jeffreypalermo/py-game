from typing import Tuple, Optional, List
from tic_tac_toe.models import GameState, Player, GameStatus, Move, GridCoordinate
from tic_tac_toe.services.move_executor import MoveExecutor
from tic_tac_toe.services.status_message_generator import StatusMessageGenerator


class GameService:
    """Business logic service for tic-tac-toe game operations."""
    
    def __init__(self):
        self._initialize_game_components()
    
    def start_new_game(self) -> GameState:
        """Start a new game and return the initial game state."""
        self.game_state.reset_to_initial_state()
        return self.game_state
    
    def make_move(self, coordinate: GridCoordinate) -> Tuple[bool, str]:
        """Attempt to make a move at the specified position."""
        return self.move_executor.attempt_move(coordinate)
    
    def get_game_state(self) -> GameState:
        """Get the current game state."""
        return self.game_state
    
    def get_current_player(self) -> Player:
        """Get the current player."""
        return self.game_state.current_player
    
    def get_game_status(self) -> GameStatus:
        """Get the current game status."""
        return self.game_state.status
    
    def get_winner(self) -> Optional[Player]:
        """Get the winner if game is finished."""
        return self.game_state.winner
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.game_state.status != GameStatus.IN_PROGRESS
    
    def get_status_message(self) -> str:
        """Get a human-readable status message."""
        return self.message_generator.create_status_message(
            self.game_state.status, 
            self.game_state.current_player
        )
    
    def get_move_history(self) -> List[Move]:
        """Get the history of moves made in the game."""
        return self.game_state.move_history.copy()
    
    def can_restart(self) -> bool:
        """Check if the game can be restarted."""
        return self.is_game_over()
    
    def _initialize_game_components(self):
        """Initialize the game service components."""
        self.game_state = GameState()
        self.move_executor = MoveExecutor(self.game_state)
        self.message_generator = StatusMessageGenerator()
