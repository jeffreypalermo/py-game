"""Value objects for encapsulating primitive data types."""
from typing import Tuple


class GridCoordinate:
    """Represents a coordinate position on the game grid."""
    
    def __init__(self, row: int, col: int):
        self._validate_coordinate_values(row, col)
        self.row = row
        self.col = col
    
    def to_tuple(self) -> Tuple[int, int]:
        """Convert to tuple format for compatibility."""
        return (self.row, self.col)
    
    def is_valid_for_grid(self, grid_size: int) -> bool:
        """Check if coordinate is valid for given grid size."""
        return (0 <= self.row < grid_size and 
                0 <= self.col < grid_size)
    
    def __eq__(self, other) -> bool:
        """Check equality with another GridCoordinate."""
        if not isinstance(other, GridCoordinate):
            return False
        return self.row == other.row and self.col == other.col
    
    def __repr__(self) -> str:
        """String representation of the coordinate."""
        return f"GridCoordinate(row={self.row}, col={self.col})"
    
    def _validate_coordinate_values(self, row: int, col: int):
        """Validate that coordinate values are non-negative."""
        if row < 0 or col < 0:
            raise ValueError("Grid coordinates must be non-negative")


class ScreenPosition:
    """Represents a position on the screen in pixels."""
    
    def __init__(self, x: int, y: int):
        self._validate_position_values(x, y)
        self.x = x
        self.y = y
    
    def to_tuple(self) -> Tuple[int, int]:
        """Convert to tuple format for compatibility."""
        return (self.x, self.y)
    
    def __eq__(self, other) -> bool:
        """Check equality with another ScreenPosition."""
        if not isinstance(other, ScreenPosition):
            return False
        return self.x == other.x and self.y == other.y
    
    def __repr__(self) -> str:
        """String representation of the position."""
        return f"ScreenPosition(x={self.x}, y={self.y})"
    
    def _validate_position_values(self, x: int, y: int):
        """Validate that position values are non-negative."""
        if x < 0 or y < 0:
            raise ValueError("Screen position coordinates must be non-negative")


class Dimensions:
    """Represents width and height dimensions."""
    
    def __init__(self, width: int, height: int):
        self._validate_dimension_values(width, height)
        self.width = width
        self.height = height
    
    def to_tuple(self) -> Tuple[int, int]:
        """Convert to tuple format for compatibility."""
        return (self.width, self.height)
    
    def get_center_point(self) -> ScreenPosition:
        """Get the center point of these dimensions."""
        return ScreenPosition(self.width // 2, self.height // 2)
    
    def __eq__(self, other) -> bool:
        """Check equality with another Dimensions object."""
        if not isinstance(other, Dimensions):
            return False
        return self.width == other.width and self.height == other.height
    
    def __repr__(self) -> str:
        """String representation of the dimensions."""
        return f"Dimensions(width={self.width}, height={self.height})"
    
    def _validate_dimension_values(self, width: int, height: int):
        """Validate that dimension values are positive."""
        if width <= 0 or height <= 0:
            raise ValueError("Dimensions must be positive")


class GridSize:
    """Represents the size of the game grid."""
    
    def __init__(self, size: int = 3):
        self._validate_grid_size(size)
        self.size = size
    
    def get_total_cells(self) -> int:
        """Get the total number of cells in the grid."""
        return self.size * self.size
    
    def is_valid_coordinate(self, coordinate: GridCoordinate) -> bool:
        """Check if a coordinate is valid for this grid size."""
        return coordinate.is_valid_for_grid(self.size)
    
    def __eq__(self, other) -> bool:
        """Check equality with another GridSize."""
        if not isinstance(other, GridSize):
            return False
        return self.size == other.size
    
    def __repr__(self) -> str:
        """String representation of the grid size."""
        return f"GridSize(size={self.size})"
    
    def _validate_grid_size(self, size: int):
        """Validate that grid size is appropriate."""
        if size <= 0:
            raise ValueError("Grid size must be positive")
        if size > 10:
            raise ValueError("Grid size too large (maximum 10)")
