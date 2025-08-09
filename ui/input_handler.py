import pygame
from typing import Tuple, Optional
from enum import Enum
from models.value_objects import ScreenPosition


class InputEvent(Enum):
    """Enum for different types of input events."""
    QUIT = "quit"
    RESTART = "restart"
    MOUSE_CLICK = "mouse_click"
    UNKNOWN = "unknown"


class InputData:
    """Data class for input events."""
    
    def __init__(self, event_type: InputEvent, data: Optional[dict] = None):
        self.event_type = event_type
        self.data = data or {}


class InputHandler:
    """Handles all user input for the tic-tac-toe game."""
    
    def __init__(self):
        self.events = []
    
    def process_events(self) -> list[InputData]:
        """Process pygame events and return a list of game-relevant input events."""
        input_events = []
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                input_events.append(InputData(InputEvent.QUIT))
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    input_events.append(InputData(InputEvent.QUIT))
                elif event.key == pygame.K_r:
                    input_events.append(InputData(InputEvent.RESTART))
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    position = ScreenPosition(event.pos[0], event.pos[1])
                    input_events.append(InputData(
                        InputEvent.MOUSE_CLICK, 
                        {"position": position}
                    ))
        
        return input_events
    
    def clear_events(self):
        """Clear the event queue."""
        pygame.event.clear()
