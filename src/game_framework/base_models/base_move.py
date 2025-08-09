"""Abstract base class for moves."""
from abc import ABC, abstractmethod
from typing import Any


class BaseMove(ABC):
    """Abstract base class for game moves."""
    
    @abstractmethod
    def is_valid(self) -> bool:
        """Check if the move is valid."""
        pass
    
    @abstractmethod
    def get_position(self) -> Any:
        """Get the position/coordinate of the move."""
        pass
    
    @abstractmethod
    def get_player(self) -> Any:
        """Get the player making the move."""
        pass
