from typing import Dict, List
from tic_tac_toe.models import GameState, Player, GameStatus


class GameAnalyticsService:
    """Service for analyzing game statistics and metrics."""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
    
    def calculate_game_metrics(self) -> Dict[str, int]:
        """Calculate comprehensive game metrics."""
        metrics = self._create_base_metrics()
        self._add_move_metrics(metrics)
        self._add_player_metrics(metrics)
        return metrics
    
    def get_game_efficiency(self) -> float:
        """Calculate game efficiency as moves per total possible."""
        total_moves = len(self.game_state.move_history)
        return total_moves / 9.0 if total_moves > 0 else 0.0
    
    def get_player_dominance(self) -> Dict[Player, float]:
        """Calculate each player's board dominance percentage."""
        player_counts = self._count_player_moves()
        total_moves = sum(player_counts.values())
        
        return self._calculate_dominance_percentages(player_counts, total_moves)
    
    def analyze_winning_pattern(self) -> str:
        """Analyze how the game was won."""
        if self.game_state.status == GameStatus.X_WINS:
            return self._determine_winning_pattern()
        elif self.game_state.status == GameStatus.O_WINS:
            return self._determine_winning_pattern()
        return "No winning pattern (game not won)"
    
    def _create_base_metrics(self) -> Dict[str, int]:
        """Create the base metrics dictionary."""
        return {
            'total_moves': len(self.game_state.move_history),
            'x_moves': 0,
            'o_moves': 0
        }
    
    def _add_move_metrics(self, metrics: Dict[str, int]):
        """Add move-based metrics to the metrics dictionary."""
        for move in self.game_state.move_history:
            if move.player == Player.X:
                metrics['x_moves'] += 1
            else:
                metrics['o_moves'] += 1
    
    def _add_player_metrics(self, metrics: Dict[str, int]):
        """Add player-specific metrics."""
        metrics['game_duration'] = len(self.game_state.move_history)
        metrics['empty_squares'] = 9 - metrics['total_moves']
    
    def _count_player_moves(self) -> Dict[Player, int]:
        """Count moves made by each player."""
        counts = {Player.X: 0, Player.O: 0}
        for move in self.game_state.move_history:
            counts[move.player] += 1
        return counts
    
    def _calculate_dominance_percentages(self, counts: Dict[Player, int], total: int) -> Dict[Player, float]:
        """Calculate dominance percentages for each player."""
        if total == 0:
            return {Player.X: 0.0, Player.O: 0.0}
        
        return {
            Player.X: (counts[Player.X] / total) * 100,
            Player.O: (counts[Player.O] / total) * 100
        }
    
    def _determine_winning_pattern(self) -> str:
        """Determine the specific winning pattern used."""
        # Simplified pattern detection - could be enhanced
        return "Three in a line (row, column, or diagonal)"
    
    def record_game_result(self, game_status: 'GameStatus'):
        """Record the result of a completed game."""
        # This could be expanded to persist analytics to a database
        # For now, just log the result
        pass
