# Tic-Tac-Toe Business Application

A professional, multi-layered Python application implementing tic-tac-toe using enterprise software architecture patterns and object-oriented programming principles.

## Architecture

This application follows a clean, layered architecture with clear separation of concerns:

### 📁 Project Structure

```
py-game/
├── app.py                    # Main application entry point
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── .vscode/
│   └── tasks.json           # VS Code tasks configuration
├── .github/
│   └── copilot-instructions.md
├── models/
│   ├── __init__.py
│   ├── player.py            # Player enum
│   ├── game_status.py       # Game status enum
│   ├── move.py              # Move data model
│   ├── game_board.py        # Game board operations
│   ├── board_validator.py   # Board validation logic
│   ├── win_checker.py       # Win condition checking
│   ├── game_state.py        # Complete game state management
│   └── value_objects.py     # Value objects for primitive encapsulation
├── services/
│   ├── __init__.py
│   ├── game_service_core.py         # Core game business logic
│   ├── game_analytics_service.py    # Game analytics and metrics
│   ├── move_executor.py             # Move execution and validation
│   └── status_message_generator.py  # UI message generation
├── controllers/
│   ├── __init__.py
│   └── game_controller.py   # Application flow control
├── ui/
│   ├── __init__.py
│   ├── renderer.py          # Visual rendering components
│   └── input_handler.py     # User input processing
└── .venv/                   # Virtual environment
```

### 🏗️ Architecture Layers

1. **Models Layer** (`models/`)
   - `Player` enum: Represents X, O, or empty cell
   - `GameStatus` enum: Tracks game state (in progress, wins, tie)
   - `Move` class: Represents a single game move
   - `GameState` class: Core game state management

2. **Services Layer** (`services/`)
   - `GameService`: Business logic for game operations
   - `GameAnalyticsService`: Statistics and game analytics

3. **Controllers Layer** (`controllers/`)
   - `GameController`: Orchestrates the entire application flow
   - Coordinates between services and UI components

4. **UI Layer** (`ui/`)
   - `GameRenderer`: Handles all visual rendering
   - `InputHandler`: Processes user input events

5. **Configuration** (`config/`)
   - Application settings and constants
   - Centralized configuration management

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python app.py
```

Or use VS Code task: `Ctrl+Shift+P` → "Tasks: Run Task" → "Run Python Game"

## Controls

- **Left Click**: Place X or O (alternating turns)
- **R Key**: Restart game when it's over
- **ESC**: Exit the game

## Features

### Core Gameplay
- ✅ Interactive tic-tac-toe grid
- ✅ Alternating X and O players
- ✅ Win detection (horizontal, vertical, diagonal)
- ✅ Tie game detection
- ✅ Game restart functionality

### Technical Features
- ✅ Object-oriented design with SOLID principles
- ✅ Layered architecture with separation of concerns
- ✅ Comprehensive game state management
- ✅ Event-driven input handling
- ✅ Modular rendering system
- ✅ Game analytics and statistics tracking
- ✅ Configuration management
- ✅ Error handling and graceful shutdown

### Analytics
- Game statistics tracking
- Win/loss/tie ratios
- Game history maintenance
- Statistics displayed on exit

## Design Patterns Used

- **MVC (Model-View-Controller)**: Clear separation between data, UI, and control logic
- **Service Layer**: Business logic encapsulation
- **Strategy Pattern**: Different rendering strategies for X and O
- **Observer Pattern**: Event-driven input handling
- **Enum Pattern**: Type-safe game states and players
- **Factory Pattern**: Centralized object creation

## Development

This application demonstrates enterprise-level software development practices:

- **Clean Architecture**: Dependencies point inward toward business logic
- **SOLID Principles**: Each class has a single responsibility
- **Type Hints**: Full type annotation for better maintainability
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Graceful error management
- **Configuration**: Externalized settings and constants

## Extending the Application

The modular architecture makes it easy to extend:

- **AI Players**: Add AI service in the services layer
- **Network Play**: Add network service for multiplayer
- **Different Boards**: Modify models for different grid sizes
- **Themes**: Add theme configuration and rendering
- **Sound**: Add audio service and sound effects
- **Animations**: Extend renderer for move animations
