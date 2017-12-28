#!/usr/bin/env python3

from typing import Optional

import unittest

class Grid:
    def __init__(self) -> None:
        self.played = False
        self.played_positions = dict()
        self.markers = "XO"
    def is_empty(self) -> bool:
        return not self.played
    def play(self, position: str) -> Optional[str]:
        if position in self.played_positions:
            return None
        marker = self.markers[len(self.played_positions)%2]
        self.played_positions[position] = marker
        self.played = True
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

if __name__ == '__main__':
    unittest.main()
