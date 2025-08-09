"""Abstract base class for game states."""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

PlayerType = TypeVar('PlayerType')
MoveType = TypeVar('MoveType')


class BaseGameState(ABC, Generic[PlayerType, MoveType]):
    """Abstract base class for all game states."""
    
    def __init__(self) -> None:
        self.current_player: Optional[PlayerType] = None
        self.is_game_over: bool = False
        self.winner: Optional[PlayerType] = None
        self.move_history: List[MoveType] = []
    
    @abstractmethod
    def make_move(self, move: MoveType) -> bool:
        """Execute a move and return success status."""
        pass
    
    @abstractmethod
    def get_valid_moves(self) -> List[MoveType]:
        """Get all valid moves for current state."""
        pass
    
    @abstractmethod
    def is_terminal(self) -> bool:
        """Check if game is in terminal state."""
        pass
    
    @abstractmethod
    def reset_to_initial_state(self) -> None:
        """Reset the game to initial state."""
        pass
    
    @abstractmethod
    def get_game_status(self) -> str:
        """Get current game status as string."""
        pass
