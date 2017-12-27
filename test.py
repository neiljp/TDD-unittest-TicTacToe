#!/usr/bin/env python3

import unittest

class Grid:
    def __init__(self) -> None:
        self.played = False
    def is_empty(self) -> bool:
        return not self.played
    def play(self, position: str) -> None:
        self.played = True

class TicTacToeTest(unittest.TestCase):
    def test_havegrid(self):
        grid = Grid()
        assert(grid is not None)
    def test_startgrid_is_empty(self):
        grid = Grid()
        assert(grid.is_empty())
    def test_play_center_after_empty(self):
        grid = Grid()
        grid.play('center')
        assert(not grid.is_empty())

if __name__ == '__main__':
    unittest.main()
