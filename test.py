#!/usr/bin/env python3

import unittest

class Grid:
    def __init__(self) -> None:
        self.played = False
        self.played_positions = set()
    def is_empty(self) -> bool:
        return not self.played
    def play(self, position: str) -> bool:
        if position in self.played_positions:
            return False
        self.played_positions.add(position)
        self.played = True
        return True

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

if __name__ == '__main__':
    unittest.main()
