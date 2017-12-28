#!/usr/bin/env python3

import unittest

class Grid:
    def __init__(self) -> None:
        self.played = False
    def is_empty(self) -> bool:
        return not self.played
    def play(self, position: str) -> bool:
        clear_position = not self.played
        self.played = True
        return clear_position

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

if __name__ == '__main__':
    unittest.main()
