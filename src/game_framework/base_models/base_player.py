"""Abstract base class for players."""
from abc import ABC, abstractmethod
from enum import Enum


class BasePlayer(ABC):
    """Abstract base class for game players."""
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the player's name."""
        pass
    
    @abstractmethod
    def get_symbol(self) -> str:
        """Get the player's symbol for display."""
        pass
