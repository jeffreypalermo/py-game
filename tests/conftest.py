"""Test configuration and fixtures."""
import pytest
import sys
from pathlib import Path

# Add src to Python path for testing
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_grid_coordinate():
    """Fixture providing a sample grid coordinate."""
    from tic_tac_toe.models.value_objects import GridCoordinate
    return GridCoordinate(1, 1)


@pytest.fixture
def sample_screen_position():
    """Fixture providing a sample screen position."""
    from tic_tac_toe.models.value_objects import ScreenPosition
    return ScreenPosition(100, 100)


@pytest.fixture
def sample_dimensions():
    """Fixture providing sample dimensions."""
    from tic_tac_toe.models.value_objects import Dimensions
    return Dimensions(600, 600)


@pytest.fixture
def sample_grid_size():
    """Fixture providing sample grid size."""
    from tic_tac_toe.models.value_objects import GridSize
    return GridSize(3)


@pytest.fixture
def game_service():
    """Provide a fresh GameService instance for each test."""
    from tic_tac_toe.services.game_service_core import GameService
    return GameService()


@pytest.fixture
def sample_coordinates():
    """Provide sample valid grid coordinates."""
    from tic_tac_toe.models.value_objects import GridCoordinate
    return [
        GridCoordinate(0, 0),
        GridCoordinate(1, 1),
        GridCoordinate(2, 2),
        GridCoordinate(0, 2),
        GridCoordinate(2, 0),
    ]


@pytest.fixture
def invalid_coordinates():
    """Provide sample invalid grid coordinates."""
    from tic_tac_toe.models.value_objects import GridCoordinate
    return [
        GridCoordinate(3, 0),   # Row out of bounds
        GridCoordinate(0, 3),   # Column out of bounds
        GridCoordinate(-1, 0),  # Negative row
        GridCoordinate(0, -1),  # Negative column
        GridCoordinate(5, 5),   # Both out of bounds
    ]


@pytest.fixture
def all_players():
    """Provide all player types."""
    from tic_tac_toe.models.player import Player
    return [Player.X, Player.O]


@pytest.fixture
def sample_moves():
    """Provide sample moves for testing."""
    from tic_tac_toe.models.move import Move
    from tic_tac_toe.models.player import Player
    from tic_tac_toe.models.value_objects import GridCoordinate
    return [
        Move(Player.X, GridCoordinate(0, 0), 1),
        Move(Player.O, GridCoordinate(1, 1), 2),
        Move(Player.X, GridCoordinate(2, 2), 3),
    ]


# Test markers configuration
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "system: mark test as a system test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "ui: mark test as UI-related"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance-related"
    )
    config.addinivalue_line(
        "markers", "x_wins: mark test as X winning scenario"
    )
    config.addinivalue_line(
        "markers", "o_wins: mark test as O winning scenario"
    )
    config.addinivalue_line(
        "markers", "tie_game: mark test as tie game scenario"
    )


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their location."""
    for item in items:
        # Mark unit tests
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Mark integration tests
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Mark system tests
        if "system" in str(item.fspath):
            item.add_marker(pytest.mark.system)
        
        # Mark UI tests
        if "ui" in str(item.fspath) or "interface" in str(item.fspath):
            item.add_marker(pytest.mark.ui)
        
        # Mark performance tests
        if "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
        
        # Mark based on test class names for game outcome scenarios
        if hasattr(item, 'cls') and item.cls:
            class_name = item.cls.__name__
            if "XWinning" in class_name:
                item.add_marker(pytest.mark.x_wins)
            elif "OWinning" in class_name:
                item.add_marker(pytest.mark.o_wins)
            elif "Tie" in class_name:
                item.add_marker(pytest.mark.tie_game)
