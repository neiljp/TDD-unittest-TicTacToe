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
    def test_havegrid(self):
        grid = Grid()
        assert(grid is not None)
    def test_startgrid_is_empty(self):
        grid = Grid()
        assert(grid.is_empty())
    def test_not_empty_after_play_center(self):
        grid = Grid()
        assert(grid.play('center'))
        assert(not grid.is_empty())
    def test_play_center_twice_fails(self):
        grid = Grid()
        assert(grid.play('center'))
        assert(not grid.play('center'))

if __name__ == '__main__':
    unittest.main()
