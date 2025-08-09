"""
Tic-Tac-Toe Business Application

A multi-layered, object-oriented implementation of tic-tac-toe game
following enterprise application patterns and best practices.

Architecture:
- Models: Data models and business entities
- Services: Business logic and game operations  
- Controllers: Application flow control and coordination
- UI: User interface components (rendering and input handling)

Author: AI Assistant
Date: August 2025
"""

from controllers.game_controller import GameController
from models import Dimensions


def main():
    """Main entry point for the tic-tac-toe business application."""
    try:
        # Create and run the game controller
        game_dimensions = Dimensions(600, 600)
        game_controller = GameController(game_dimensions)
        game_controller.run()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
