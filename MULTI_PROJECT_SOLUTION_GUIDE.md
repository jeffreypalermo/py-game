# Multi-Project Python Solution Structure

## Recommended Structure for Game Solution

```
game-solution/
├── pyproject.toml                 # Root project configuration
├── README.md                     # Solution overview
├── requirements.txt              # Shared dependencies
├── .gitignore
├── src/
│   ├── tic_tac_toe/             # Your current project
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── models/
│   │   ├── services/
│   │   ├── controllers/
│   │   └── ui/
│   ├── connect_four/            # New game project
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── models/
│   │   ├── services/
│   │   └── ui/
│   ├── chess/                   # Another game project
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── ...
│   └── game_framework/          # Shared game framework
│       ├── __init__.py
│       ├── base_models/
│       ├── base_services/
│       ├── base_ui/
│       └── common/
├── tests/
│   ├── test_tic_tac_toe/
│   ├── test_connect_four/
│   ├── test_chess/
│   └── test_framework/
├── docs/
│   ├── api/
│   ├── games/
│   └── framework/
└── scripts/
    ├── build.py
    ├── test_all.py
    └── deploy.py
```

## Root Configuration (pyproject.toml)

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "game-solution"
version = "0.1.0"
description = "Multi-game solution with shared framework"
authors = [{name = "Your Name", email = "your.email@example.com"}]
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "pygame>=2.5.0",
    "numpy>=1.21.0",
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "black>=22.0", "mypy>=0.991"]
docs = ["sphinx>=5.0", "sphinx-rtd-theme"]

[project.scripts]
tic-tac-toe = "tic_tac_toe.app:main"
connect-four = "connect_four.app:main" 
chess = "chess.app:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-dir]
"" = "src"
```

## Shared Framework Example

```python
# src/game_framework/base_models/base_game_state.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

PlayerType = TypeVar('PlayerType')
MoveType = TypeVar('MoveType')

class BaseGameState(ABC, Generic[PlayerType, MoveType]):
    """Abstract base class for all game states."""
    
    def __init__(self):
        self.current_player: Optional[PlayerType] = None
        self.is_game_over: bool = False
        self.winner: Optional[PlayerType] = None
    
    @abstractmethod
    def make_move(self, move: MoveType) -> bool:
        """Execute a move and return success status."""
        pass
    
    @abstractmethod
    def get_valid_moves(self) -> list[MoveType]:
        """Get all valid moves for current state."""
        pass
    
    @abstractmethod
    def is_terminal(self) -> bool:
        """Check if game is in terminal state."""
        pass

# src/game_framework/base_services/base_game_service.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

GameStateType = TypeVar('GameStateType')

class BaseGameService(ABC, Generic[GameStateType]):
    """Abstract base class for game services."""
    
    def __init__(self):
        self.game_state: Optional[GameStateType] = None
    
    @abstractmethod
    def start_new_game(self) -> GameStateType:
        """Start a new game."""
        pass
    
    @abstractmethod
    def get_game_state(self) -> GameStateType:
        """Get current game state."""
        pass
```

## Individual Game Implementation

```python
# src/tic_tac_toe/models/game_state.py
from game_framework.base_models.base_game_state import BaseGameState
from .player import Player
from .move import Move

class TicTacToeGameState(BaseGameState[Player, Move]):
    """Tic-tac-toe specific game state."""
    
    def make_move(self, move: Move) -> bool:
        # Your existing implementation
        pass
    
    def get_valid_moves(self) -> list[Move]:
        # Implementation specific to tic-tac-toe
        pass

# src/connect_four/models/game_state.py  
from game_framework.base_models.base_game_state import BaseGameState
from .player import Player
from .move import Move

class ConnectFourGameState(BaseGameState[Player, Move]):
    """Connect Four specific game state."""
    
    def make_move(self, move: Move) -> bool:
        # Connect Four specific implementation
        pass
```
