#!/usr/bin/env python3

from typing import Optional

import unittest

class Grid:
    textual_positions = ['top_left', 'top_middle', 'top_right',
                         'middle_left', 'center', 'middle_right',
                         'bottom_left', 'bottom_middle', 'bottom_right']
    def __init__(self) -> None:
        self.played_positions = dict()
        self.markers = "XO"
    def is_empty(self) -> bool:
        return len(self.played_positions) == 0
    def is_full(self) -> bool:
        return len(self.played_positions) == 9
    def play(self, position: str) -> Optional[str]:
        if position in self.played_positions:
            return None
        if position not in self.textual_positions:
            return None
        marker = self.markers[len(self.played_positions)%2]
        self.played_positions[position] = marker
        return marker
    def get_winning_player(self) -> Optional[str]:
        if self.is_empty() or len(self.played_positions) < 5:
            return None
        winning_lines = [{'top_left', 'middle_left', 'bottom_left'},
                         {'top_right', 'middle_right', 'bottom_right'},
                         {'top_left', 'top_middle', 'top_right'},
                         {'middle_left', 'center', 'middle_right'},
                         {'bottom_left', 'bottom_middle', 'bottom_right'},
                         {'top_middle', 'center', 'bottom_middle'},
        ]
        for marker in self.markers:
            positions = {k for k, v in self.played_positions.items() if v is marker}
            if len([line for line in winning_lines if positions.issuperset(line)]):
                return marker
        return None

class TicTacToeTest(unittest.TestCase):
    def setUp(self):
        self.grid = Grid()
    def test_havegrid(self):
        assert(self.grid is not None)
    def test_startgrid_is_empty_and_not_full(self):
        assert(self.grid.is_empty())
        self.assertFalse(self.grid.is_full())
    def test_not_empty_and_not_full_after_play_center(self):
        assert(self.grid.play('center'))
        assert(not self.grid.is_empty())
        self.assertFalse(self.grid.is_full())
    def test_play_center_twice_fails(self):
        assert(self.grid.play('center'))
        assert(not self.grid.play('center'))
    def test_play_top_left_twice(self):
        assert(self.grid.play('top_left'))
        assert(not self.grid.play('top_left'))
    def test_play_center_then_top_left(self):
        assert(self.grid.play('center'))
        assert(self.grid.play('top_left'))
    def test_alternating_play_marks(self):
        self.assertEqual(self.grid.play('center'), 'X')
        self.assertEqual(self.grid.play('top_left'), 'O')
        self.assertEqual(self.grid.play('bottom_middle'), 'X')
        self.assertEqual(self.grid.play('bottom_left'), 'O')
    def test_bad_play_position(self):
        self.assertEqual(self.grid.play('cheese'), None)
    def test_all_textual_moves(self):
        for move in Grid.textual_positions:
            self.assertIsNotNone(self.grid.play(move), move)
    def test_is_full_after_all_moves_made(self):
        for move in Grid.textual_positions:
            self.grid.play(move)
        self.assertEqual(self.grid.is_full(), True)
    def test_no_player_won_with_empty_grid(self):
        self.assertEqual(self.grid.get_winning_player(), None)
    def test_no_player_won_after_X_plays_once(self):
        self.grid.play('center')
        self.assertEqual(self.grid.get_winning_player(), None)
    def test_many_plays_but_no_player_won_yet(self):
        plays = ['top_left', 'top_right', 'middle_left', 'middle_right', 'center']
        for play in plays:
            self.grid.play(play)
        self.assertEqual(self.grid.get_winning_player(), None)
    def test_X_player_should_win_on_left(self):
        plays = ['top_left', 'top_right', 'middle_left', 'middle_right', 'bottom_left']
        for play in plays:
            self.grid.play(play)
        self.assertEqual(self.grid.get_winning_player(), 'X')
    def test_X_player_should_win_on_right(self):
        plays = ['top_right', 'top_left', 'middle_right', 'middle_left', 'bottom_right']
        for play in plays:
            self.grid.play(play)
        self.assertEqual(self.grid.get_winning_player(), 'X')
    def test_O_player_should_win_on_left(self):
        plays = ['top_left', 'top_right', 'middle_left', 'middle_right', 'center', 'bottom_right']
        for play in plays:
            self.grid.play(play)
        self.assertEqual(self.grid.get_winning_player(), 'O')
    def test_O_player_should_win_on_right(self):
        plays = ['top_right', 'top_left', 'middle_right', 'middle_left', 'center', 'bottom_left']
        for play in plays:
            self.grid.play(play)
        self.assertEqual(self.grid.get_winning_player(), 'O')
    def _make_plays(self, x_plays, o_plays, grid=None):
        if grid is None:
            grid = self.grid
        plays = x_plays + o_plays
        plays[::2] = x_plays
        plays[1::2] = o_plays
        for play in plays:
            grid.play(play)
    def test_O_player_should_win_on_top(self):
        X_plays = ['bottom_left', 'bottom_middle', 'center']
        O_plays = ['top_left', 'top_middle', 'top_right']
        self._make_plays(X_plays, O_plays)
        self.assertEqual(self.grid.get_winning_player(), 'O')
    def test_O_player_should_win_on_bottom(self):
        X_plays = ['top_left', 'top_middle', 'center']
        O_plays = ['bottom_left', 'bottom_middle', 'bottom_right']
        self._make_plays(X_plays, O_plays)
        self.assertEqual(self.grid.get_winning_player(), 'O')
    def test_O_player_should_win_middle_horizontally(self):
        X_plays = ['top_left', 'top_middle', 'bottom_left']
        O_plays = ['middle_left', 'center', 'middle_right']
        self._make_plays(X_plays, O_plays)
        self.assertEqual(self.grid.get_winning_player(), 'O')
    def test_O_player_should_win_middle_vertically(self):
        X_plays = ['top_left', 'bottom_right', 'bottom_left']
        O_plays = ['top_middle', 'center', 'bottom_middle']
        self._make_plays(X_plays, O_plays)
        self.assertEqual(self.grid.get_winning_player(), 'O')
    def test_X_player_should_win_horizontally_x3(self):
        X_plays = [[0,1,2], [3,4,5], [6,7,8]]
        O_plays = [[3,4], [6,7], [0,1]]  # Abitrary valid other moves
        for game_x, game_o in zip(X_plays, O_plays):
            grid = Grid()
            game_x = [Grid.textual_positions[i] for i in game_x]
            game_o = [Grid.textual_positions[j] for j in game_o]
            self._make_plays(game_x, game_o, grid)
            self.assertEqual(grid.get_winning_player(), 'X', (game_x, game_o))

if __name__ == '__main__':
    unittest.main()
