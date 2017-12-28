#!/usr/bin/env python3

from typing import Optional

import unittest

class Grid:
    textual_positions = {'top_left', 'top_middle', 'top_right',
                         'middle_left', 'center', 'middle_right',
                         'bottom_left', 'bottom_middle', 'bottom_right'}
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
        if self.is_empty():
            return None
        X = [v for v in self.played_positions.values() if v is 'X']
        if not self.is_empty() and len(X) < 3:
            return None
        return 'X'

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
    def test_X_player_should_win(self):
        plays = ['top_left', 'top_right', 'middle_left', 'middle_right', 'bottom_left']
        for play in plays:
            self.grid.play(play)
        self.assertEqual(self.grid.get_winning_player(), 'X')

if __name__ == '__main__':
    unittest.main()
