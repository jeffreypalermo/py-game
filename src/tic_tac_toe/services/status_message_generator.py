from tic_tac_toe.models import GameStatus, Player


class StatusMessageGenerator:
    """Generates human-readable status messages for the game."""
    
    def create_status_message(self, status: GameStatus, current_player: Player) -> str:
        """Generate appropriate status message based on game state."""
        if self._is_game_in_progress(status):
            return self._create_current_player_message(current_player)
        
        return self._create_game_ended_message(status)
    
    def _is_game_in_progress(self, status: GameStatus) -> bool:
        """Check if the game is still in progress."""
        return status == GameStatus.IN_PROGRESS
    
    def _create_current_player_message(self, current_player: Player) -> str:
        """Create message showing whose turn it is."""
        player_name = self._get_player_display_name(current_player)
        return f"Current player: {player_name}"
    
    def _create_game_ended_message(self, status: GameStatus) -> str:
        """Create message for when the game has ended."""
        if status == GameStatus.X_WINS:
            return "X Wins!"
        elif status == GameStatus.O_WINS:
            return "O Wins!"
        elif status == GameStatus.TIE:
            return "It's a Tie!"
        else:
            return "Unknown game state"
    
    def _get_player_display_name(self, player: Player) -> str:
        """Get the display name for a player."""
        return "X" if player == Player.X else "O"
