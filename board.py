import sys


class SudokuBoard:
    """
    Class to contain a sudoku board.
    """
    addresses = []
    address_grids = []

    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    addresses.append((k + (i * 3), l + (j * 3)))

    for i in range(9):
        address_grids.append([*addresses[(i * 9): (i * 9) + 9]])

    def __init__(self):
        """
        Initializes a blank sudoku board.
        """
        self.board = [[0] * 9 for _ in range(9)]

    @staticmethod
    def get_grid(row, col):
        """
        Get grid value of the provided cell location
        :param row: Row of current cell
        :param col: Column of current cell
        :return: int between 0 and 9
        """
        for i in range(9):
            if (row, col) in SudokuBoard.address_grids[i]:
                return i

    def update_board(self):
        """
        Asks user for location and value and updates the board accordingly.
        Designed for use in terminal.
        :return: None
        """
        row = int(input("Input row value (1-9): "))
        column = int(input("Input column value (1-9): "))
        value = int(input("Input number: "))
        if row in range(1, 10) or column in range(1, 10) or value in range(1, 10):
            self.board[row-1][column-1] = value
        else:
            print("Invalid values!")
            return None

    def ui_update_board(self, value=0, row=9, column=9):
        """
        Receives row, column and value from GUI window and updates the board accordingly.
        :param value: int. Value between 1 and 9.
        :param row: int. Value between 0 and 8.
        :param column: int. Value between 0 and 8.
        :return: None
        """
        if row in range(9) and column in range(9) and value in range(1, 10):
            self.board[row][column] = value
        else:
            # print("Invalid values!")
            return None

    def check_row(self, value, row):
        """
        Check if duplicate value is present on the same row containing the cell.

        :param value: value: Value to verify
        :param row: Row of current cell
        :return: bool
        """
        for i in self.board[row]:
            if value == i:
                return True

        return False

    def check_col(self, value, col):
        """
        Check if duplicate value is present on the same column containing the cell.

        :param value: Value to verify
        :param col: Column of current cell
        :return: bool
        """
        for i in range(9):
            if value == self.board[i][col]:
                return True

        return False

    def check_grid(self, value, row, col):
        """
        Check if duplicate value is present on the small grid containing the cell.

        :param value: Value to verify
        :param row: Row of current cell
        :param col: Column of current cell
        :return: bool
        """
        g = SudokuBoard.get_grid(row, col)
        for loc in SudokuBoard.address_grids[g]:
            x, y = loc
            if value == self.board[x][y]:
                return True

        return False

    def find_empty(self):
        """
        Finds empty cells on the grid.

        :return: row, column if empty cell is found, else None
        """
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def check_board_valid(self):
        """
        Check if board is valid. Unused method.
        Validation takes place on the UI end before values are passed.
        :return bool
        """
        for i in range(9):
            for j in range(9):
                if self.board[i][j] >= 10:
                    return False
                elif self.board[i][j] < 0:
                    return False
                elif self.board[i][j] != 0:
                    if self.check_grid(self.board[i][j], i, j):
                        return False
                    elif self.check_row(self.board[i][j], i) or self.check_col(self.board[i][j], j):
                        return False
        return True

    def solve(self):
        """
        Solves the board based on provided data.
        Algorithm concept acquired online.
        :return: bool
        """
        chk = self.find_empty()
        if chk:
            row, col = chk
            for new_val in range(1, 10):
                if self.check_grid(new_val, row, col) or self.check_col(new_val, col) or self.check_row(new_val, row):
                    continue
                else:
                    self.board[row][col] = new_val
                    if self.solve():
                        return True
                    self.board[row][col] = 0
        else:
            return True
        return False

    def clear(self):
        """
        Resets the board and changes all cells to 0.
        :return: None
        """
        self.board = [[0] * 9 for _ in range(9)]

    def cell_value(self, row, col):
        """
        Returns value of cell based on row and column.
        :param row: int. Value between 0 and 8.
        :param col: int. Value between 0 and 8.
        :return: int.
        """
        val = self.board[row][col]
        return val

    def full_board(self) -> list[list[int]]:
        """
        Copy the full board and pass it as return.
        :return: int[]. A 2D list of integers.
        """
        return self.board.copy()

    def print_board(self):
        """
        Prints the board in a grid format to match Sudoku board.
        Source: stackoverflow.com
        :return: None
        """
        print(" ", end="")
        for i in range(1, 10):
            print(f"   {i}", end="")
        print()
        print("  " + "-" * 37)
        for i, row in enumerate(self.board):
            print((f"{i+1} |" + " {}   {}   {} |" * 3).format(*[x if x != 0 else " " for x in row]))
            if i == 8:
                print("  " + "-" * 37)
            elif i % 3 == 2:
                print("  |" + "---+" * 8 + "---|")
            else:
                print("  |" + "   +" * 8 + "   |")


def handler(s: SudokuBoard):
    """
    Handles the process of adding/editing elements to a blank grid, printing the grid and solving the grid.
    Infinitely loops until option 4 is selected.
    Built to check functionality of the class in terminal.

    :param s: SudokuBoard object
    :return: None
    """
    choice = 2
    while choice:
        print("Actions\n1. Update Board\n2. Print Current Board\n3. Solve Board\n4. Exit")
        try:
            choice = int(input("Enter a choice: "))
        except EOFError:
            print("Exit Triggered.")
            sys.exit()
        except ValueError:
            choice = 5
        if choice == 4:
            sys.exit()
        elif choice == 1:
            s.update_board()
        elif choice == 2:
            s.print_board()
        elif choice == 3:
            s.solve()
        # elif choice == 6:
        #     for i in range(9):
        #         for j in range(9):
        #             print(s.cell_value(i, j), end=" ")
        #         print()
        else:
            print("Invalid Value")
            continue


def main():
    s = SudokuBoard()
    handler(s)


if __name__ == '__main__':
    main()
