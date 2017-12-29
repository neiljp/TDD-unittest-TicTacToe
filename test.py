#!/usr/bin/env python3

from typing import Optional

import unittest

class InvalidMarkers(Exception):
    pass

class Grid:
    textual_positions = ['top_left', 'top_middle', 'top_right',
                         'middle_left', 'center', 'middle_right',
                         'bottom_left', 'bottom_middle', 'bottom_right']
    def __init__(self, markers: str = "XO") -> None:
        if len(markers) != 2:
            raise InvalidMarkers()
        if markers[0] == markers[1]:
            raise InvalidMarkers()
        self.played_positions = dict()
        self.markers = markers
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
        winning_lines = [{'top_left', 'middle_left', 'bottom_left'},  # Down
                         {'top_middle', 'center', 'bottom_middle'},
                         {'top_right', 'middle_right', 'bottom_right'},
                         {'top_left', 'top_middle', 'top_right'},  # Across
                         {'middle_left', 'center', 'middle_right'},
                         {'bottom_left', 'bottom_middle', 'bottom_right'},
                         {'top_left', 'center', 'bottom_right'},  # Diagonal
                         {'top_right', 'center', 'bottom_left'},
        ]
        for marker in self.markers:
            positions = {k for k, v in self.played_positions.items() if v is marker}
            if len([line for line in winning_lines if positions.issuperset(line)]):
                return marker
        return None

class TicTacToeTest(unittest.TestCase):
    player_1 = "X"
    player_2 = "O"
    def make_grid(self):
        return Grid()

    def setUp(self):
        self.grid = self.make_grid()
    def test_too_few_markers(self):
        with self.assertRaises(InvalidMarkers):
            grid = Grid("O")
    def test_too_many_markers(self):
        with self.assertRaises(InvalidMarkers):
            grid = Grid("OXY")
    def test_duplicate_markers(self):
        with self.assertRaises(InvalidMarkers):
            grid = Grid("OO")
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
    def test_no_player_won_after_one_play(self):
        self.grid.play('center')
        self.assertEqual(self.grid.get_winning_player(), None)
    def test_alternating_play_marks(self):
        self.assertEqual(self.grid.play('center'), self.player_1)
        self.assertEqual(self.grid.play('top_left'), self.player_2)
        self.assertEqual(self.grid.play('bottom_middle'), self.player_1)
        self.assertEqual(self.grid.play('bottom_left'), self.player_2)
    def test_many_plays_but_no_player_won_yet(self):
        moves = ['top_left', 'top_right', 'middle_left', 'middle_right', 'center']
        for move in moves:
            self.grid.play(move)
        self.assertEqual(self.grid.get_winning_player(), None)

    def _make_plays(self, first_moves, second_moves, grid=None):
        if grid is None:
            grid = self.grid
        moves = first_moves + second_moves
        moves[::2] = first_moves
        moves[1::2] = second_moves
        for move in moves:
            grid.play(move)
    def _get_grids_for_multiple_encoded_plays(self, first_moves, second_moves):
        grids = []
        for game_first, game_second in zip(first_moves, second_moves):
            grid = self.make_grid()
            game_first  = [Grid.textual_positions[i] for i in game_first]
            game_second = [Grid.textual_positions[j] for j in game_second]
            self._make_plays(game_first, game_second, grid)
            grids.append((grid, game_first, game_second))
        return grids

    def test_first_player_should_win_on_left(self):
        moves = ['top_left', 'top_right', 'middle_left', 'middle_right', 'bottom_left']
        for move in moves:
            self.grid.play(move)
        self.assertEqual(self.grid.get_winning_player(), self.player_1)
    def test_first_player_should_win_on_right(self):
        moves = ['top_right', 'top_left', 'middle_right', 'middle_left', 'bottom_right']
        for move in moves:
            self.grid.play(move)
        self.assertEqual(self.grid.get_winning_player(), self.player_1)
    def test_second_player_should_win_on_left(self):
        moves = ['top_left', 'top_right', 'middle_left', 'middle_right', 'center', 'bottom_right']
        for move in moves:
            self.grid.play(move)
        self.assertEqual(self.grid.get_winning_player(), self.player_2)
    def test_second_player_should_win_on_right(self):
        moves = ['top_right', 'top_left', 'middle_right', 'middle_left', 'center', 'bottom_left']
        for move in moves:
            self.grid.play(move)
        self.assertEqual(self.grid.get_winning_player(), self.player_2)
    def test_second_player_should_win_on_top(self):
        player_1_moves = ['bottom_left', 'bottom_middle', 'center']
        player_2_moves = ['top_left', 'top_middle', 'top_right']
        self._make_plays(player_1_moves, player_2_moves)
        self.assertEqual(self.grid.get_winning_player(), self.player_2)
    def test_second_player_should_win_on_bottom(self):
        player_1_moves = ['top_left', 'top_middle', 'center']
        player_2_moves = ['bottom_left', 'bottom_middle', 'bottom_right']
        self._make_plays(player_1_moves, player_2_moves)
        self.assertEqual(self.grid.get_winning_player(), self.player_2)
    def test_second_player_should_win_middle_horizontally(self):
        player_1_moves = ['top_left', 'top_middle', 'bottom_left']
        player_2_moves = ['middle_left', 'center', 'middle_right']
        self._make_plays(player_1_moves, player_2_moves)
        self.assertEqual(self.grid.get_winning_player(), self.player_2)
    def test_second_player_should_win_middle_vertically(self):
        player_1_moves = ['top_left', 'bottom_right', 'bottom_left']
        player_2_moves = ['top_middle', 'center', 'bottom_middle']
        self._make_plays(player_1_moves, player_2_moves)
        self.assertEqual(self.grid.get_winning_player(), self.player_2)
    def test_first_player_should_win_horizontally_x3(self):
        player_1_moves = [[0,1,2], [3,4,5], [6,7,8]]
        player_2_moves = [[3,4], [6,7], [0,1]]  # Abitrary valid other moves
        for grid, first, second in self._get_grids_for_multiple_encoded_plays(player_1_moves, player_2_moves):
            self.assertEqual(grid.get_winning_player(), self.player_1, (first, second))
    def test_first_player_should_win_vertically_x3(self):
        player_1_moves = [[0,3,6], [1,4,7], [2,5,8]]
        player_2_moves = [[1,2], [2,3], [3,4]]  # Abitrary valid other moves
        for grid, first, second in self._get_grids_for_multiple_encoded_plays(player_1_moves, player_2_moves):
            self.assertEqual(grid.get_winning_player(), self.player_1, (first, second))
    def test_first_player_should_win_diagonally_x2(self):
        player_1_moves = [[0,4,8], [2,4,6]]
        player_2_moves = [[1,2], [3,5]]  # Abitrary valid other moves
        for grid, first, second in self._get_grids_for_multiple_encoded_plays(player_1_moves, player_2_moves):
            self.assertEqual(grid.get_winning_player(), self.player_1, (first, second))
    def test_second_player_should_win_horizontally_x3(self):
        player_1_moves = [[0,1,6], [3,4,1], [6,7,3]]  # Abitrary valid other moves
        player_2_moves = [[3,4,5], [6,7,8], [0,1,2]]
        for grid, first, second in self._get_grids_for_multiple_encoded_plays(player_1_moves, player_2_moves):
            self.assertEqual(grid.get_winning_player(), self.player_2, (first, second))
    def test_second_player_should_win_vertically_x3(self):
        player_1_moves = [[0,3,5], [1,4,5], [1,4,6]]  # Abitrary valid other moves
        player_2_moves = [[1,4,7], [0,3,6], [2,5,8]]
        for grid, first, second in self._get_grids_for_multiple_encoded_plays(player_1_moves, player_2_moves):
            self.assertEqual(grid.get_winning_player(), self.player_2, (first, second))
    def test_second_player_should_win_diagonally_x2(self):
        player_1_moves = [[1,3,7], [1,0,3]]  # Abitrary valid other moves
        player_2_moves = [[0,4,8], [2,4,6]]
        for grid, first, second in self._get_grids_for_multiple_encoded_plays(player_1_moves, player_2_moves):
            self.assertEqual(grid.get_winning_player(), self.player_2, (first, second))

class TicTacToeTest_XO(TicTacToeTest):
    player_1 = "X"
    player_2 = "O"
    def make_grid(self):
        return Grid("XO")

class TicTacToeTest_OX(TicTacToeTest):
    player_1 = "O"
    player_2 = "X"
    def make_grid(self):
        return Grid("OX")

class TicTacToeTest_star_plus(TicTacToeTest):  # Demonstration of arbitrary marker pairs
    player_1 = "*"
    player_2 = "+"
    def make_grid(self):
        return Grid("*+")

if __name__ == '__main__':
    unittest.main()
