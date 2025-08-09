from enum import Enum


class GameStatus(Enum):
    """Enum representing the current status of the game."""
    IN_PROGRESS = "in_progress"
    X_WINS = "x_wins"
    O_WINS = "o_wins"
    TIE = "tie"
