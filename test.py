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
    def get_grid(self) -> str:
        if self.is_empty():
            return " "*9
        return "".join(self.played_positions[posn]
                           if posn in self.played_positions else " "
                       for posn in self.textual_positions)
    def __str__(self) -> str:
        return self.get_grid()
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
    def test_get_grid_at_start(self):
        self.assertEqual(self.grid.get_grid(), " "*9)
    def test_get_grid_after_all_textual_moves(self):
        for move in Grid.textual_positions:
            self.grid.play(move)
        self.assertEqual(self.grid.get_grid(),
                         (self.player_1 + self.player_2)*4 + self.player_1)
    def test_get_grid_after_all_moves_offset_by_3(self):
        moves = list(range(3,9))
        moves.extend(list(range(0,3)))
        for move in moves:
            self.grid.play(Grid.textual_positions[move])
        target = (self.player_1 + self.player_2 + self.player_1 +
                  (self.player_1 + self.player_2)*3)
        self.assertEqual(self.grid.get_grid(), target)
    def test_get_grid_after_center_play(self):
        self.grid.play('center')
        self.assertEqual(self.grid.get_grid(), " "*4 + self.player_1 + " "*4)
    def test_get_grid_same_as_str(self):
        self.grid.play('center')
        self.grid.play('top_left')
        self.grid.play('bottom_right')
        self.assertEqual(self.grid.get_grid(), "%s" % self.grid)

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

class TTTComputer:
    def __init__(self):
        self.triples = [ {0, 4, 8}, {2, 4, 6} ]  # Diagonals
        for i in range(0,3):
            self.triples.append({0+(3*i), 1+(3*i), 2+(3*i)})  # Horizontals
            self.triples.append({0+i, 3+i, 6+i})  # Verticals
    def play_on_grid(self, grid: Grid, with_mark: str, vs_mark: str) -> None:
        grid_s = grid.get_grid()
        number_of_plays = len([entry for entry in grid_s if entry is not " "])
        # Try to win
        winning_move = self._try_to_win(grid_s, with_mark)
        if winning_move is not None:
            grid.play(Grid.textual_positions[winning_move])
            return
        # Block any potential losing move
        avoid_loss_move = self._try_to_avoid_loss(grid_s, vs_mark)
        if avoid_loss_move is not None:
            grid.play(Grid.textual_positions[avoid_loss_move])
            return
        # If center is not taken, take it, except on first move
        if number_of_plays > 0 and grid_s[4] == " ":
            grid.play('center')
            return
        # Play in next available space
        for sequential_move in range(0, 9):
            if grid_s[sequential_move] == " ":
                grid.play(Grid.textual_positions[sequential_move])
                return
        return
    def _try_to_win(self, grid_str: str, with_mark: str) -> Optional[int]:
        '''Tries to find a move to win; if so, returns index, otherwise None.'''
        my_marks = {idx for idx, what in enumerate(grid_str) if what is with_mark}
        # We know we have one entry, so using pop is safe (triple less length=2 item)
        winning_moves = [(triple - (triple & my_marks)).pop() for triple in self.triples
                         if len(triple & my_marks) == 2]
        if winning_moves:
            empty_winning_moves = [move for move in winning_moves if grid_str[move] == " "]
            if empty_winning_moves:
                assert(len(empty_winning_moves)==1)  # FIXME? Previous code assumed this
                return empty_winning_moves[0]
        return None
    def _try_to_avoid_loss(self, grid_str: str, vs_mark: str) -> Optional[int]:
        '''Tries to find if a position must be played to block an opponent's win.
           If so, returns that index, otherwise None.'''
        vs_marks = {idx for idx, what in enumerate(grid_str) if what is vs_mark}
        # We know we have one entry, so using pop is safe (triple less length=2 item)
        avoid_loss_moves = [(triple - (triple & vs_marks)).pop() for triple in self.triples
                            if len(triple & vs_marks) == 2]
        if avoid_loss_moves:
            empty_avoid_loss_moves = [move for move in avoid_loss_moves if grid_str[move] == " "]
            if empty_avoid_loss_moves:
                assert(len(empty_avoid_loss_moves)==1)  # FIXME? Computer has lost - forked!
                return empty_avoid_loss_moves[0]
        return None

class TTT_computer_test(unittest.TestCase):
    def setUp(self):
        self.computer = TTTComputer()
        self.grid = Grid("XO")
    def assertNumberOfPlaysOnGrid(self, grid_str: str, number_of_plays: int, msg=""):
        expected_number_of_plays = len([entry for entry in grid_str if entry is not " "])
        self.assertEqual(expected_number_of_plays, number_of_plays, msg=msg)
    def print_grid_2d(self, grid_str: str):
        grid_str_ = "".join(["_" if chr == " " else chr for chr in grid_str])
        print()
        print(grid_str_[0:3])
        print(grid_str_[3:6])
        print(grid_str_[6:9])
        print()

    def test_TTTComputer_exists(self):
        self.assertIsNotNone(self.computer)
    def test_computer_play_leaves_grid_not_empty(self):
        self.assertTrue(self.grid.is_empty())
        self.computer.play_on_grid(self.grid, "X", "O")
        self.assertFalse(self.grid.is_empty())
    def test_computer_tries_to_win_from_2_in_row_down_left_side(self):
        self.grid.play('top_left')  # X
        self.grid.play('top_right')  # O
        self.grid.play('bottom_left')  # X
        self.grid.play('bottom_right')  # O
        self.computer.play_on_grid(self.grid, "X", "O")  # X
        self.assertEqual(self.grid.get_grid(), "X OX  X O")
        self.assertEqual(self.grid.get_winning_player(), 'X')
    def test_computer_tries_to_win_from_2_in_row_down_right_side(self):
        self.grid.play('top_right')  # X
        self.grid.play('top_left')  # O
        self.grid.play('bottom_right')  # X
        self.grid.play('bottom_left')  # O
        self.computer.play_on_grid(self.grid, "X", "O")  # X
        self.assertEqual(self.grid.get_grid(), "O X  XO X")
        self.assertEqual(self.grid.get_winning_player(), 'X')
    def test_computer_doesnt_try_to_win_where_opponent_has_marker(self):
        self.grid.play('top_right')  # X
        self.grid.play('top_left')  # O
        self.grid.play('bottom_right')  # X
        self.grid.play('middle_right')  # O [blocks X win]
        self.computer.play_on_grid(self.grid, "X", "O")  # X
        self.assertNumberOfPlaysOnGrid(self.grid.get_grid(), 5)
    def test_computer_plays_in_blank_if_cant_win(self):
        for move_2 in range(1, 9):
            grid = Grid("XO")  # Use new grid each time
            grid.play('top_left')
            grid.play(Grid.textual_positions[move_2])
            self.computer.play_on_grid(grid, "X", "O")
            self.assertNumberOfPlaysOnGrid(grid.get_grid(), 3, Grid.textual_positions[move_2])
    def test_computer_can_block(self):
        self.grid.play('top_right')  # X
        self.grid.play('top_left')  # O
        self.grid.play('bottom_middle')  # X
        self.grid.play('middle_left')  # O
        self.computer.play_on_grid(self.grid, "X", "O")  # X
        grid_s = self.grid.get_grid()
        self.assertNumberOfPlaysOnGrid(grid_s, 5)
        self.assertEqual(grid_s, "O XO  XX ")
    def test_computer_plays_in_center_if_unoccupied_and_not_first_move(self):
        for move_1 in range(0, 9):
            grid = Grid("XO")  # Use new grid each time
            grid.play(Grid.textual_positions[move_1])
            self.computer.play_on_grid(grid, "O", "X")
            self.assertNumberOfPlaysOnGrid(grid.get_grid(), 2, Grid.textual_positions[move_1])
            expected_grid = ["X" if i==move_1 else " " for i in range(0, 9)]
            if move_1 != 4:
                expected_grid[4] = "O"
            else:
                expected_grid[0] = "O"
            self.assertEqual(grid.get_grid(), "".join(expected_grid))
    def test_computer_starts_in_the_corner(self):  # best probabilistic strategy
        self.computer.play_on_grid(self.grid, "X", "O")
        grid_s = self.grid.get_grid()
        self.assertNumberOfPlaysOnGrid(grid_s, 1)
        X_index = grid_s.find("X")
        self.assertTrue(X_index in (0, 2, 6, 8))

if __name__ == '__main__':
    unittest.main()
