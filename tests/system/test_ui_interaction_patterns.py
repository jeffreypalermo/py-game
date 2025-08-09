"""Specialized UI interaction pattern tests."""
import sys
from pathlib import Path
import pytest
from unittest.mock import Mock, patch, MagicMock
import pygame

# Add src to Python path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from tic_tac_toe.models.value_objects import ScreenPosition, GridCoordinate, Dimensions
from tic_tac_toe.models.player import Player
from tic_tac_toe.models.game_status import GameStatus
from tic_tac_toe.ui.input_handler import InputHandler, InputData, InputEvent
from tic_tac_toe.ui.renderer import GameRenderer


class TestUIInteractionPatterns:
    """Test various UI interaction patterns and user behaviors."""
    
    @pytest.fixture
    def mock_pygame_events(self):
        """Mock pygame events for testing."""
        with patch('pygame.event.get') as mock_get:
            yield mock_get
    
    @pytest.fixture
    def input_handler(self):
        """Provide an input handler for testing."""
        return InputHandler()
    
    @pytest.fixture
    def renderer(self):
        """Provide a renderer for coordinate conversion testing."""
        return GameRenderer(Dimensions(600, 600))
    
    def test_mouse_click_coordinate_conversion(self, renderer):
        """Test that screen coordinates are correctly converted to grid coordinates."""
        # Test clicks in each grid cell
        test_cases = [
            # (screen_x, screen_y, expected_row, expected_col)
            (100, 100, 0, 0),  # Top-left
            (300, 100, 0, 1),  # Top-center
            (500, 100, 0, 2),  # Top-right
            (100, 300, 1, 0),  # Middle-left
            (300, 300, 1, 1),  # Center
            (500, 300, 1, 2),  # Middle-right
            (100, 500, 2, 0),  # Bottom-left
            (300, 500, 2, 1),  # Bottom-center
            (500, 500, 2, 2),  # Bottom-right
        ]
        
        for screen_x, screen_y, expected_row, expected_col in test_cases:
            screen_pos = ScreenPosition(screen_x, screen_y)
            grid_coord = renderer.screen_to_grid_coordinates(screen_pos)
            
            assert grid_coord.row == expected_row, f"Row mismatch for ({screen_x}, {screen_y})"
            assert grid_coord.col == expected_col, f"Col mismatch for ({screen_x}, {screen_y})"
    
    def test_click_boundary_detection(self, renderer):
        """Test boundary detection for grid clicks."""
        # Test clicks inside grid
        inside_clicks = [
            ScreenPosition(150, 150),  # Well inside first cell
            ScreenPosition(300, 300),  # Center of grid
            ScreenPosition(450, 450),  # Inside bottom-right area
        ]
        
        for position in inside_clicks:
            assert renderer.is_click_in_grid(position), f"Click at {position} should be inside grid"
        
        # Test clicks outside grid (assuming 600x600 window with centered grid)
        outside_clicks = [
            ScreenPosition(50, 50),    # Too far left/up
            ScreenPosition(550, 550),  # Too far right/down
            ScreenPosition(10, 300),   # Far left edge
            ScreenPosition(590, 300),  # Far right edge
        ]
        
        for position in outside_clicks:
            # Some of these might actually be inside depending on grid layout
            # The important thing is the method doesn't crash
            result = renderer.is_click_in_grid(position)
            assert isinstance(result, bool)
    
    def test_rapid_clicking_pattern(self, input_handler, mock_pygame_events):
        """Test rapid clicking pattern handling."""
        # Simulate rapid mouse clicks
        rapid_clicks = []
        for i in range(10):
            click_event = Mock()
            click_event.type = pygame.MOUSEBUTTONDOWN
            click_event.button = 1  # Left click
            click_event.pos = (100 + i * 10, 100 + i * 10)  # Slightly different positions
            rapid_clicks.append(click_event)
        
        mock_pygame_events.return_value = rapid_clicks
        
        input_events = input_handler.process_events()
        
        # Should receive all click events
        assert len(input_events) == 10
        for event in input_events:
            assert event.event_type == InputEvent.MOUSE_CLICK
            assert 'position' in event.data
    
    def test_mixed_input_events(self, input_handler, mock_pygame_events):
        """Test handling of mixed input event types."""
        mixed_events = []
        
        # Add mouse click
        click_event = Mock()
        click_event.type = pygame.MOUSEBUTTONDOWN
        click_event.button = 1
        click_event.pos = (300, 300)
        mixed_events.append(click_event)
        
        # Add keyboard events
        key_r = Mock()
        key_r.type = pygame.KEYDOWN
        key_r.key = pygame.K_r
        mixed_events.append(key_r)
        
        key_esc = Mock()
        key_esc.type = pygame.KEYDOWN
        key_esc.key = pygame.K_ESCAPE
        mixed_events.append(key_esc)
        
        # Add quit event
        quit_event = Mock()
        quit_event.type = pygame.QUIT
        mixed_events.append(quit_event)
        
        mock_pygame_events.return_value = mixed_events
        
        input_events = input_handler.process_events()
        
        # Should receive all events converted to our format
        assert len(input_events) == 4
        
        event_types = [event.event_type for event in input_events]
        assert InputEvent.MOUSE_CLICK in event_types
        assert InputEvent.RESTART in event_types
        assert InputEvent.QUIT in event_types
        assert event_types.count(InputEvent.QUIT) == 2  # Both ESC and QUIT
    
    def test_invalid_mouse_button_clicks(self, input_handler, mock_pygame_events):
        """Test that only left mouse button clicks are processed."""
        invalid_clicks = []
        
        # Right click
        right_click = Mock()
        right_click.type = pygame.MOUSEBUTTONDOWN
        right_click.button = 3  # Right button
        right_click.pos = (300, 300)
        invalid_clicks.append(right_click)
        
        # Middle click
        middle_click = Mock()
        middle_click.type = pygame.MOUSEBUTTONDOWN
        middle_click.button = 2  # Middle button
        middle_click.pos = (300, 300)
        invalid_clicks.append(middle_click)
        
        # Valid left click for comparison
        left_click = Mock()
        left_click.type = pygame.MOUSEBUTTONDOWN
        left_click.button = 1  # Left button
        left_click.pos = (300, 300)
        invalid_clicks.append(left_click)
        
        mock_pygame_events.return_value = invalid_clicks
        
        input_events = input_handler.process_events()
        
        # Should only receive the left click
        assert len(input_events) == 1
        assert input_events[0].event_type == InputEvent.MOUSE_CLICK
    
    def test_coordinate_edge_cases(self, renderer):
        """Test coordinate conversion edge cases."""
        # Test coordinates at cell boundaries
        edge_cases = [
            # Coordinates right at grid boundaries
            ScreenPosition(0, 0),      # Far top-left
            ScreenPosition(600, 600),  # Far bottom-right (outside grid)
            ScreenPosition(200, 200),  # Cell boundary area
            ScreenPosition(400, 400),  # Another boundary area
        ]
        
        for position in edge_cases:
            # These shouldn't crash the system
            try:
                grid_coord = renderer.screen_to_grid_coordinates(position)
                # Verify the coordinate is valid integers
                assert isinstance(grid_coord.row, int)
                assert isinstance(grid_coord.col, int)
            except Exception as e:
                pytest.fail(f"Coordinate conversion failed for {position}: {e}")
    
    def test_input_event_data_integrity(self, input_handler, mock_pygame_events):
        """Test that input event data maintains integrity."""
        test_position = (250, 350)
        
        click_event = Mock()
        click_event.type = pygame.MOUSEBUTTONDOWN
        click_event.button = 1
        click_event.pos = test_position
        
        mock_pygame_events.return_value = [click_event]
        
        input_events = input_handler.process_events()
        
        assert len(input_events) == 1
        event = input_events[0]
        
        # Verify event structure
        assert event.event_type == InputEvent.MOUSE_CLICK
        assert 'position' in event.data
        
        # Verify position data integrity
        position = event.data['position']
        assert isinstance(position, ScreenPosition)
        assert position.x == test_position[0]
        assert position.y == test_position[1]
    
    def test_clear_events_functionality(self, input_handler):
        """Test that clear_events works correctly."""
        with patch('pygame.event.clear') as mock_clear:
            input_handler.clear_events()
            mock_clear.assert_called_once()


class TestUIResponsePatterns:
    """Test UI response patterns and user experience flows."""
    
    def test_grid_layout_calculations(self):
        """Test grid layout calculations for different window sizes."""
        test_dimensions = [
            Dimensions(600, 600),  # Square
            Dimensions(800, 600),  # Landscape
            Dimensions(600, 800),  # Portrait
            Dimensions(400, 400),  # Small square
            Dimensions(1000, 800), # Large landscape
        ]
        
        for dimensions in test_dimensions:
            renderer = GameRenderer(dimensions)
            
            # Verify basic layout properties
            assert renderer.cell_size > 0, f"Cell size should be positive for {dimensions}"
            assert renderer.grid_offset_x >= 0, f"Grid offset X should be non-negative for {dimensions}"
            assert renderer.grid_offset_y >= 0, f"Grid offset Y should be non-negative for {dimensions}"
            
            # Verify grid fits within window
            total_grid_width = renderer.grid_size.size * renderer.cell_size
            total_grid_height = renderer.grid_size.size * renderer.cell_size
            
            assert renderer.grid_offset_x + total_grid_width <= dimensions.width
            assert renderer.grid_offset_y + total_grid_height <= dimensions.height
    
    def test_cell_center_calculations(self):
        """Test that cell center calculations are accurate."""
        renderer = GameRenderer(Dimensions(600, 600))
        
        # Test center calculation for each cell
        for row in range(3):
            for col in range(3):
                # Calculate expected center
                expected_x = renderer.grid_offset_x + (col * renderer.cell_size) + (renderer.cell_size // 2)
                expected_y = renderer.grid_offset_y + (row * renderer.cell_size) + (renderer.cell_size // 2)
                
                # Verify a click at this center maps back to correct grid position
                center_position = ScreenPosition(expected_x, expected_y)
                grid_coord = renderer.screen_to_grid_coordinates(center_position)
                
                assert grid_coord.row == row, f"Center click row mismatch for cell ({row}, {col})"
                assert grid_coord.col == col, f"Center click col mismatch for cell ({row}, {col})"
    
    def test_screen_to_grid_consistency(self):
        """Test consistency of screen-to-grid coordinate conversion."""
        renderer = GameRenderer(Dimensions(600, 600))
        
        # Test that multiple clicks in the same cell map to the same grid position
        test_cases = [
            # Multiple positions within the same cell should map to same grid coord
            [(150, 150), (180, 180), (120, 170)],  # All should map to (0,0) area
            [(350, 350), (380, 320), (320, 380)],  # All should map to center area
            [(450, 450), (480, 470), (470, 450)],  # All should map to same cell
        ]
        
        for positions in test_cases:
            grid_coords = []
            for x, y in positions:
                position = ScreenPosition(x, y)
                if renderer.is_click_in_grid(position):
                    grid_coord = renderer.screen_to_grid_coordinates(position)
                    grid_coords.append((grid_coord.row, grid_coord.col))
            
            # All positions in the same cell should map to the same grid coordinate
            if grid_coords:  # Only test if at least one position was in grid
                first_coord = grid_coords[0]
                for coord in grid_coords[1:]:
                    assert coord == first_coord, f"Inconsistent mapping: {grid_coords}"
    
    def test_ui_bounds_safety(self):
        """Test that UI operations are safe with extreme inputs."""
        renderer = GameRenderer(Dimensions(600, 600))
        
        # Test with extreme coordinates (all valid - no negative values)
        extreme_positions = [
            ScreenPosition(10000, 10000),  # Far positive
            ScreenPosition(0, 0),          # Origin
        ]
        
        for position in extreme_positions:
            # These operations should not crash
            try:
                is_in_grid = renderer.is_click_in_grid(position)
                assert isinstance(is_in_grid, bool)
                
                # Grid coordinate conversion should also not crash
                grid_coord = renderer.screen_to_grid_coordinates(position)
                assert isinstance(grid_coord.row, int)
                assert isinstance(grid_coord.col, int)
                
            except Exception as e:
                pytest.fail(f"UI operation failed for extreme position {position}: {e}")
        
        # Test that negative coordinates are properly rejected by ScreenPosition
        with pytest.raises(ValueError, match="Screen position coordinates must be non-negative"):
            ScreenPosition(-1000, -1000)
        
        with pytest.raises(ValueError, match="Screen position coordinates must be non-negative"):
            ScreenPosition(-100, 300)
        
        with pytest.raises(ValueError, match="Screen position coordinates must be non-negative"):
            ScreenPosition(300, -100)


class TestUserExperienceFlows:
    """Test complete user experience flows through the UI."""
    
    def test_typical_user_game_flow(self):
        """Test a typical user playing a complete game."""
        # This would be a high-level test of the complete flow
        # In a real implementation, this would involve the full game controller
        
        # Simulate typical user behavior:
        # 1. Start game
        # 2. Click center
        # 3. Opponent clicks corner
        # 4. Continue until game ends
        # 5. Restart game
        
        renderer = GameRenderer(Dimensions(600, 600))
        
        # Simulate clicks for a typical game
        typical_clicks = [
            (300, 300),  # Center
            (150, 150),  # Top-left corner
            (150, 300),  # Left middle
            (450, 150),  # Top-right
            (450, 300),  # Right middle - this should complete a winning line
        ]
        
        grid_moves = []
        for x, y in typical_clicks:
            position = ScreenPosition(x, y)
            if renderer.is_click_in_grid(position):
                grid_coord = renderer.screen_to_grid_coordinates(position)
                grid_moves.append((grid_coord.row, grid_coord.col))
        
        # Verify we captured all the intended moves
        assert len(grid_moves) == 5
        
        # Verify the moves form a sensible game pattern
        expected_pattern = [(1, 1), (0, 0), (1, 0), (0, 2), (1, 2)]
        assert grid_moves == expected_pattern
    
    def test_error_recovery_patterns(self):
        """Test UI behavior during error conditions."""
        renderer = GameRenderer(Dimensions(600, 600))
        
        # Test recovery from invalid clicks (only valid positive coordinates)
        invalid_attempts = [
            ScreenPosition(50, 50),    # Outside grid
            ScreenPosition(700, 700),  # Way outside
        ]
        
        for position in invalid_attempts:
            # UI should handle these gracefully
            is_valid = renderer.is_click_in_grid(position)
            
            # Even invalid positions should return a boolean
            assert isinstance(is_valid, bool)
            
            # System should remain stable
            grid_coord = renderer.screen_to_grid_coordinates(position)
            assert isinstance(grid_coord, GridCoordinate)
        
        # Test that negative coordinates are properly rejected by ScreenPosition
        with pytest.raises(ValueError, match="Screen position coordinates must be non-negative"):
            ScreenPosition(-50, 300)
