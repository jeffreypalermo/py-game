"""Performance and stress tests for the complete game system."""
import sys
from pathlib import Path
import pytest
import time
from typing import List, Tuple

# Add src to Python path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from tic_tac_toe.models.value_objects import GridCoordinate
from tic_tac_toe.models.player import Player
from tic_tac_toe.models.game_status import GameStatus
from tic_tac_toe.services.game_service_core import GameService


class TestPerformanceScenarios:
    """Test performance and stress scenarios."""
    
    @pytest.fixture
    def game_service(self):
        """Provide a fresh game service for each test."""
        return GameService()
    
    @pytest.mark.slow
    def test_rapid_game_succession(self, game_service):
        """Test playing many games in rapid succession."""
        start_time = time.time()
        games_played = 0
        
        # Play 100 complete games
        for _ in range(100):
            game_service.start_new_game()
            
            # Play a quick game (X wins top row)
            moves = [
                GridCoordinate(0, 0),  # X
                GridCoordinate(1, 0),  # O
                GridCoordinate(0, 1),  # X
                GridCoordinate(1, 1),  # O
                GridCoordinate(0, 2),  # X wins
            ]
            
            for move in moves:
                success, _ = game_service.make_move(move)
                if not success:
                    break
                if game_service.is_game_over():
                    break
            
            games_played += 1
        
        end_time = time.time()
        total_time = end_time - start_time
        
        assert games_played == 100
        assert total_time < 5.0  # Should complete in under 5 seconds
        assert game_service.is_game_over()
    
    @pytest.mark.slow
    def test_all_possible_winning_combinations(self, game_service):
        """Test all 8 possible winning combinations systematically."""
        winning_combinations = [
            # Rows
            [(0, 0), (0, 1), (0, 2)],  # Top row
            [(1, 0), (1, 1), (1, 2)],  # Middle row
            [(2, 0), (2, 1), (2, 2)],  # Bottom row
            # Columns
            [(0, 0), (1, 0), (2, 0)],  # Left column
            [(0, 1), (1, 1), (2, 1)],  # Middle column
            [(0, 2), (1, 2), (2, 2)],  # Right column
            # Diagonals
            [(0, 0), (1, 1), (2, 2)],  # Main diagonal
            [(0, 2), (1, 1), (2, 0)],  # Anti-diagonal
        ]
        
        for i, winning_line in enumerate(winning_combinations):
            game_service.start_new_game()
            
            # Create a game where X wins with this combination
            x_moves = [GridCoordinate(row, col) for row, col in winning_line]
            o_moves = []
            
            # Generate O moves that don't interfere with X's winning line
            all_positions = [(r, c) for r in range(3) for c in range(3)]
            available_positions = [pos for pos in all_positions if pos not in winning_line]
            o_moves = [GridCoordinate(row, col) for row, col in available_positions[:2]]
            
            # Alternate moves: X, O, X, O, X (X wins)
            moves = []
            for j in range(3):
                moves.append(x_moves[j])
                if j < 2:  # Don't add O move after X's winning move
                    moves.append(o_moves[j])
            
            # Play the moves
            for move in moves:
                success, _ = game_service.make_move(move)
                assert success
                if game_service.is_game_over():
                    break
            
            # Verify X won
            assert game_service.is_game_over()
            assert game_service.get_winner() == Player.X
            assert game_service.get_game_status() == GameStatus.X_WINS
    
    def test_memory_usage_stability(self, game_service):
        """Test that memory usage remains stable across many games."""
        # This is a simple test - in a real scenario you'd use memory profiling tools
        
        initial_move_count = 0
        
        # Play 50 games and ensure no memory leaks in move history
        for game_num in range(50):
            game_service.start_new_game()
            
            # Quick game
            moves = [
                GridCoordinate(0, 0), GridCoordinate(1, 0),
                GridCoordinate(0, 1), GridCoordinate(1, 1),
                GridCoordinate(0, 2)
            ]
            
            for move in moves:
                success, _ = game_service.make_move(move)
                if not success or game_service.is_game_over():
                    break
            
            # After each game, verify move history is properly managed
            if game_num == 0:
                initial_move_count = len(game_service.get_move_history())
            
            # Each game should have similar move count (no accumulation)
            current_move_count = len(game_service.get_move_history())
            assert abs(current_move_count - initial_move_count) <= 1  # Allow small variance
    
    def test_concurrent_game_simulation(self):
        """Test multiple game instances running simultaneously."""
        services = [GameService() for _ in range(10)]
        
        # Start all games
        for service in services:
            service.start_new_game()
        
        # Play different games on each service
        game_sequences = [
            # Different winning patterns for each game
            [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)],  # X wins top row
            [(1, 0), (0, 0), (1, 1), (0, 1), (1, 2)],  # X wins middle row
            [(2, 0), (0, 0), (2, 1), (0, 1), (2, 2)],  # X wins bottom row
            [(0, 0), (0, 1), (1, 0), (0, 2), (2, 0)],  # X wins left column
            [(0, 1), (0, 0), (1, 1), (0, 2), (2, 1)],  # X wins middle column
            [(0, 2), (0, 0), (1, 2), (0, 1), (2, 2)],  # X wins right column
            [(0, 0), (0, 1), (1, 1), (0, 2), (2, 2)],  # X wins main diagonal
            [(0, 2), (0, 0), (1, 1), (0, 1), (2, 0)],  # X wins anti-diagonal
            [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (1, 1), (2, 0), (2, 2), (2, 1)],  # Tie
            [(1, 1), (0, 0), (0, 1), (2, 0), (2, 1)],  # X wins middle column
        ]
        
        # Execute all games
        for i, (service, sequence) in enumerate(zip(services, game_sequences)):
            for row, col in sequence:
                success, _ = service.make_move(GridCoordinate(row, col))
                if not success or service.is_game_over():
                    break
        
        # Verify all games completed successfully
        for i, service in enumerate(services):
            assert service.is_game_over() or len(service.get_move_history()) > 0
            
            # Most should have X wins (except the tie game)
            if i == 8:  # The tie game
                assert service.get_game_status() == GameStatus.TIE
            else:
                assert service.get_game_status() in [GameStatus.X_WINS, GameStatus.O_WINS, GameStatus.TIE]


class TestEdgeCaseScenarios:
    """Test edge cases and boundary conditions."""
    
    @pytest.fixture
    def game_service(self):
        """Provide a fresh game service for each test."""
        return GameService()
    
    def test_boundary_coordinates(self, game_service):
        """Test moves at grid boundaries."""
        game_service.start_new_game()
        
        # Test all corner and edge positions
        boundary_positions = [
            (0, 0), (0, 2), (2, 0), (2, 2),  # Corners
            (0, 1), (1, 0), (1, 2), (2, 1),  # Edges
            (1, 1)  # Center
        ]
        
        for i, (row, col) in enumerate(boundary_positions):
            if not game_service.is_game_over():
                success, _ = game_service.make_move(GridCoordinate(row, col))
                assert success, f"Failed to make move at boundary position ({row}, {col})"
    
    def test_immediate_win_detection(self, game_service):
        """Test that wins are detected immediately when they occur."""
        game_service.start_new_game()
        
        # Set up a game where X can win on the next move
        moves = [
            GridCoordinate(0, 0),  # X
            GridCoordinate(1, 0),  # O
            GridCoordinate(0, 1),  # X
            GridCoordinate(1, 1),  # O
        ]
        
        for move in moves:
            success, _ = game_service.make_move(move)
            assert success
            assert not game_service.is_game_over()  # Game should not be over yet
        
        # Make the winning move
        success, message = game_service.make_move(GridCoordinate(0, 2))
        assert success
        assert game_service.is_game_over()  # Game should be over immediately
        assert game_service.get_winner() == Player.X
        assert "win" in message.lower() or "successful" in message.lower()
    
    def test_alternating_player_turns(self, game_service):
        """Test that players alternate correctly throughout the game."""
        game_service.start_new_game()
        
        expected_players = [Player.X, Player.O, Player.X, Player.O, Player.X, Player.O, Player.X, Player.O, Player.X]
        moves = [
            (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (1, 1), (2, 0), (2, 2), (2, 1)
        ]
        
        for i, (row, col) in enumerate(moves):
            if not game_service.is_game_over():
                current_player = game_service.get_current_player()
                assert current_player == expected_players[i], f"Expected {expected_players[i]} but got {current_player} at move {i}"
                
                success, _ = game_service.make_move(GridCoordinate(row, col))
                assert success
    
    def test_game_state_consistency(self, game_service):
        """Test that game state remains consistent throughout play."""
        game_service.start_new_game()
        
        # Play a complete game and verify state consistency at each step
        moves = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)]  # X wins
        
        for i, (row, col) in enumerate(moves):
            # Before move
            move_count_before = len(game_service.get_move_history())
            game_over_before = game_service.is_game_over()
            
            # Make move
            success, _ = game_service.make_move(GridCoordinate(row, col))
            assert success
            
            # After move
            move_count_after = len(game_service.get_move_history())
            game_over_after = game_service.is_game_over()
            
            # Verify consistency
            assert move_count_after == move_count_before + 1
            
            # Game should be over only after the winning move (last move)
            if i == len(moves) - 1:
                assert game_over_after
                assert game_service.get_winner() == Player.X
            else:
                assert not game_over_after or game_over_before  # Could already be over from previous move
    
    def test_invalid_moves_ignored(self, game_service):
        """Test that invalid moves are properly ignored and don't affect game state."""
        game_service.start_new_game()
        
        # Make a valid move
        success, _ = game_service.make_move(GridCoordinate(0, 0))
        assert success
        initial_move_count = len(game_service.get_move_history())
        initial_player = game_service.get_current_player()
        
        # Try to make an invalid move (same position)
        success, _ = game_service.make_move(GridCoordinate(0, 0))
        assert not success
        
        # Verify game state unchanged
        assert len(game_service.get_move_history()) == initial_move_count
        assert game_service.get_current_player() == initial_player
        
        # Verify a valid move still works
        success, _ = game_service.make_move(GridCoordinate(1, 1))
        assert success
        assert len(game_service.get_move_history()) == initial_move_count + 1


class TestExhaustiveGameCombinations:
    """Test exhaustive combinations of game scenarios."""
    
    @pytest.fixture
    def game_service(self):
        """Provide a fresh game service for each test."""
        return GameService()
    
    @pytest.mark.slow
    def test_all_first_move_combinations(self, game_service):
        """Test all possible first moves and verify they're all valid."""
        all_positions = [(r, c) for r in range(3) for c in range(3)]
        
        for row, col in all_positions:
            game_service.start_new_game()
            
            success, _ = game_service.make_move(GridCoordinate(row, col))
            assert success, f"First move at ({row}, {col}) should always be valid"
            assert game_service.get_current_player() == Player.O  # Should switch to O
            assert len(game_service.get_move_history()) == 1
    
    @pytest.mark.slow
    def test_systematic_win_prevention(self, game_service):
        """Test systematic win prevention scenarios."""
        # Test scenarios where O prevents X from winning
        prevention_scenarios = [
            {
                'name': 'Prevent top row',
                'x_moves': [(0, 0), (0, 1)],
                'o_prevention': (0, 2),
                'description': 'O blocks X from completing top row'
            },
            {
                'name': 'Prevent diagonal', 
                'x_moves': [(0, 0), (1, 1)],
                'o_prevention': (2, 2),
                'description': 'O blocks X from completing main diagonal'
            },
            {
                'name': 'Prevent anti-diagonal',
                'x_moves': [(0, 2), (1, 1)],
                'o_prevention': (2, 0),
                'description': 'O blocks X from completing anti-diagonal'
            },
            {
                'name': 'Prevent left column',
                'x_moves': [(0, 0), (1, 0)],
                'o_prevention': (2, 0),
                'description': 'O blocks X from completing left column'
            }
        ]
        
        for scenario in prevention_scenarios:
            game_service.start_new_game()
            
            # X makes first two moves
            game_service.make_move(GridCoordinate(*scenario['x_moves'][0]))
            game_service.make_move(GridCoordinate(1, 2))  # O's first move (non-interfering)
            game_service.make_move(GridCoordinate(*scenario['x_moves'][1]))
            
            # O prevents the win
            success, _ = game_service.make_move(GridCoordinate(*scenario['o_prevention']))
            assert success, f"Prevention move failed in scenario: {scenario['name']}"
            
            # X should not be able to complete the winning line immediately
            assert not game_service.is_game_over(), f"Game ended prematurely in scenario: {scenario['name']}"
