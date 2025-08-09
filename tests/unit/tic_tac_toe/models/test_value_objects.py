"""Unit tests for value objects."""
import pytest
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from tic_tac_toe.models.value_objects import GridCoordinate, ScreenPosition, Dimensions, GridSize


class TestGridCoordinate:
    """Test cases for GridCoordinate value object."""

    def test_valid_coordinate_creation(self):
        """Test creating valid grid coordinates."""
        coord = GridCoordinate(2, 3)
        assert coord.row == 2
        assert coord.col == 3

    def test_negative_coordinates_raise_error(self):
        """Test that negative coordinates raise ValueError."""
        with pytest.raises(ValueError, match="Grid coordinates must be non-negative"):
            GridCoordinate(-1, 2)
            
        with pytest.raises(ValueError, match="Grid coordinates must be non-negative"):
            GridCoordinate(2, -1)

    def test_to_tuple(self):
        """Test converting coordinate to tuple."""
        coord = GridCoordinate(1, 2)
        assert coord.to_tuple() == (1, 2)

    def test_is_valid_for_grid(self):
        """Test grid validation."""
        coord = GridCoordinate(1, 1)
        assert coord.is_valid_for_grid(3) is True
        assert coord.is_valid_for_grid(2) is True
        assert coord.is_valid_for_grid(1) is False

    def test_equality(self):
        """Test coordinate equality."""
        coord1 = GridCoordinate(1, 2)
        coord2 = GridCoordinate(1, 2)
        coord3 = GridCoordinate(2, 1)
        
        assert coord1 == coord2
        assert coord1 != coord3
        assert coord1 != "not a coordinate"

    def test_repr(self):
        """Test string representation."""
        coord = GridCoordinate(1, 2)
        assert str(coord) == "GridCoordinate(row=1, col=2)"


class TestScreenPosition:
    """Test cases for ScreenPosition value object."""

    def test_valid_position_creation(self):
        """Test creating valid screen positions."""
        pos = ScreenPosition(100, 200)
        assert pos.x == 100
        assert pos.y == 200

    def test_negative_position_raises_error(self):
        """Test that negative positions raise ValueError."""
        with pytest.raises(ValueError, match="Screen position coordinates must be non-negative"):
            ScreenPosition(-1, 100)

    def test_to_tuple(self):
        """Test converting position to tuple."""
        pos = ScreenPosition(100, 200)
        assert pos.to_tuple() == (100, 200)

    def test_equality(self):
        """Test position equality."""
        pos1 = ScreenPosition(100, 200)
        pos2 = ScreenPosition(100, 200)
        pos3 = ScreenPosition(200, 100)
        
        assert pos1 == pos2
        assert pos1 != pos3

    def test_repr(self):
        """Test string representation."""
        pos = ScreenPosition(100, 200)
        assert str(pos) == "ScreenPosition(x=100, y=200)"


class TestDimensions:
    """Test cases for Dimensions value object."""

    def test_valid_dimensions_creation(self):
        """Test creating valid dimensions."""
        dim = Dimensions(800, 600)
        assert dim.width == 800
        assert dim.height == 600

    def test_zero_dimensions_raise_error(self):
        """Test that zero or negative dimensions raise ValueError."""
        with pytest.raises(ValueError, match="Dimensions must be positive"):
            Dimensions(0, 600)
            
        with pytest.raises(ValueError, match="Dimensions must be positive"):
            Dimensions(800, -1)

    def test_to_tuple(self):
        """Test converting dimensions to tuple."""
        dim = Dimensions(800, 600)
        assert dim.to_tuple() == (800, 600)

    def test_get_center_point(self):
        """Test getting center point."""
        dim = Dimensions(800, 600)
        center = dim.get_center_point()
        assert center.x == 400
        assert center.y == 300

    def test_equality(self):
        """Test dimensions equality."""
        dim1 = Dimensions(800, 600)
        dim2 = Dimensions(800, 600)
        dim3 = Dimensions(600, 800)
        
        assert dim1 == dim2
        assert dim1 != dim3

    def test_repr(self):
        """Test string representation."""
        dim = Dimensions(800, 600)
        assert str(dim) == "Dimensions(width=800, height=600)"


class TestGridSize:
    """Test cases for GridSize value object."""

    def test_valid_grid_size_creation(self):
        """Test creating valid grid size."""
        grid = GridSize(3)
        assert grid.size == 3

    def test_default_grid_size(self):
        """Test default grid size."""
        grid = GridSize()
        assert grid.size == 3

    def test_invalid_grid_size_raises_error(self):
        """Test that invalid grid sizes raise ValueError."""
        with pytest.raises(ValueError, match="Grid size must be positive"):
            GridSize(0)
            
        with pytest.raises(ValueError, match="Grid size too large"):
            GridSize(11)

    def test_get_total_cells(self):
        """Test getting total cell count."""
        grid = GridSize(3)
        assert grid.get_total_cells() == 9
        
        grid = GridSize(4)
        assert grid.get_total_cells() == 16

    def test_is_valid_coordinate(self):
        """Test coordinate validation."""
        grid = GridSize(3)
        
        valid_coord = GridCoordinate(1, 1)
        invalid_coord = GridCoordinate(3, 3)
        
        assert grid.is_valid_coordinate(valid_coord) is True
        assert grid.is_valid_coordinate(invalid_coord) is False

    def test_equality(self):
        """Test grid size equality."""
        grid1 = GridSize(3)
        grid2 = GridSize(3)
        grid3 = GridSize(4)
        
        assert grid1 == grid2
        assert grid1 != grid3

    def test_repr(self):
        """Test string representation."""
        grid = GridSize(3)
        assert str(grid) == "GridSize(size=3)"
