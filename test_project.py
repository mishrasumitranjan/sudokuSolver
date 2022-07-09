import pytest
import project as pr

from board import SudokuBoard

s = SudokuBoard()

empty_board = [[0] * 9 for _ in range(9)]
partial_board = [
    [0, 0, 5, 0, 0, 3, 0, 0, 0],
    [1, 0, 0, 0, 5, 0, 8, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 9, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 2, 0, 0, 0, 6, 4, 8, 0],
    [0, 0, 0, 0, 8, 0, 0, 0, 9],
    [2, 0, 0, 0, 3, 0, 1, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 6, 0, 7, 0, 0, 0, 0, 0],
]

solved_board = [
    [8, 9, 5, 2, 6, 3, 7, 4, 1],
    [1, 3, 4, 9, 5, 7, 8, 2, 6],
    [6, 7, 2, 4, 1, 8, 3, 9, 5],
    [4, 8, 9, 1, 7, 2, 5, 6, 3],
    [3, 2, 1, 5, 9, 6, 4, 8, 7],
    [7, 5, 6, 3, 8, 4, 2, 1, 9],
    [2, 4, 7, 6, 3, 9, 1, 5, 8],
    [9, 1, 3, 8, 2, 5, 6, 7, 4],
    [5, 6, 8, 7, 4, 1, 9, 3, 2],
]


def test_ui_update_board():
    for i in range(9):
        for j in range(9):
            if partial_board[i][j] != 0:
                s.ui_update_board(partial_board[i][j], i, j)
                assert s.cell_value(i, j) == partial_board[i][j]


def test_solve():
    s.solve()


def test_cell_value():
    for i in range(9):
        for j in range(9):
            assert s.cell_value(i, j) == solved_board[i][j]


def test_full_board():
    assert solved_board == s.full_board()


def test_clear():
    s.clear()
    assert empty_board == s.full_board()


def test_get_grid():
    for i in range(3):
        for j in range(3):
            assert SudokuBoard.get_grid(i, j) == 0

    for i in range(3):
        for j in range(3, 6):
            assert SudokuBoard.get_grid(i, j) == 1

    for i in range(3):
        for j in range(6, 9):
            assert SudokuBoard.get_grid(i, j) == 2

    for i in range(3, 6):
        for j in range(3):
            assert SudokuBoard.get_grid(i, j) == 3

    for i in range(3, 6):
        for j in range(3, 6):
            assert SudokuBoard.get_grid(i, j) == 4

    for i in range(3, 6):
        for j in range(6, 9):
            assert SudokuBoard.get_grid(i, j) == 5

    for i in range(6, 9):
        for j in range(3):
            assert SudokuBoard.get_grid(i, j) == 6

    for i in range(6, 9):
        for j in range(3, 6):
            assert SudokuBoard.get_grid(i, j) == 7

    for i in range(6, 9):
        for j in range(6, 9):
            assert SudokuBoard.get_grid(i, j) == 8


def test_validate():
    for i in range(1, 10):
        assert pr.Window1.validate(str(i))
    with pytest.raises(ValueError):
        assert pr.Window1.validate('s')
        assert pr.Window1.validate(10)
        assert pr.Window1.validate(6456613)
        assert pr.Window1.validate(-85)
        assert pr.Window1.validate(0)
        assert pr.Window1.validate('hello')
