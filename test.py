#!/usr/bin/env python3

from typing import Optional

import unittest

class Grid:
    def __init__(self) -> None:
        self.played_positions = dict()
        self.markers = "XO"
        self.allowed_positions = {'top_left', 'top_middle', 'top_right',
                                  'middle_left', 'center', 'middle_right',
                                  'bottom_left', 'bottom_middle', 'bottom_right'}
    def is_empty(self) -> bool:
        return len(self.played_positions) == 0
    def is_full(self) -> bool:
        return len(self.played_positions) == 9
    def play(self, position: str) -> Optional[str]:
        if position in self.played_positions:
            return None
        if position not in self.allowed_positions:
            return None
        marker = self.markers[len(self.played_positions)%2]
        self.played_positions[position] = marker
        return marker

class TicTacToeTest(unittest.TestCase):
    def setUp(self):
        self.grid = Grid()
    def test_havegrid(self):
        assert(self.grid is not None)
    def test_startgrid_is_empty(self):
        assert(self.grid.is_empty())
    def test_not_empty_after_play_center(self):
        assert(self.grid.play('center'))
        assert(not self.grid.is_empty())
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
        moves = {'top_left', 'top_middle', 'top_right',
                 'middle_left', 'center', 'middle_right',
                 'bottom_left', 'bottom_middle', 'bottom_right'}
        for move in moves:
            self.assertIsNotNone(self.grid.play(move), move)
    def test_is_full_after_all_moves_made(self):
        moves = {'top_left', 'top_middle', 'top_right',
                 'middle_left', 'center', 'middle_right',
                 'bottom_left', 'bottom_middle', 'bottom_right'}
        for move in moves:
            self.grid.play(move)
        self.assertEqual(self.grid.is_full(), True)

if __name__ == '__main__':
    unittest.main()
