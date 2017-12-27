#!/usr/bin/env python3

import unittest

class Grid:
    def is_empty(self) -> bool:
        return True

class TicTacToeTest(unittest.TestCase):
    def test_havegrid(self):
        grid = Grid()
        assert(grid is not None)
    def test_startgrid_is_empty(self):
        grid = Grid()
        assert(grid.is_empty())

if __name__ == '__main__':
    unittest.main()
