import tkinter as tk
import threading
import gradient_check as gc

from tkinter import ttk
from board import SudokuBoard
from tkinter import messagebox as msg
from tkinter import Menu


def main():
    ...


class Window1:
    def __init__(self, window):
        """
        Initializes the Window1 object and creates the entire window structure.

        :param window: Tk() object
        """
        # Creates the base window
        self.window = window
        self.s = SudokuBoard()
        self.s_copy = [[0] * 9 for _ in range(9)]
        self.window.title("Sudoku Solver")
        self.window.geometry('530x440')
        self.window.resizable(False, False)

        # Creates a frame with gradient background. Two options present.
        # self.big_frame = gc.GradientFrame(self.window, color1="#cc2b5e", color2="#753a88")    # Magenta gradient
        self.big_frame = gc.GradientFrame(self.window, color1="#60b0a7", color2="#13547a")  # Sea Green gradient
        self.big_frame.pack(fill='both', expand=True)

        # Creates a frame inside the gradient frame. This holds the board.
        self.frame_1 = tk.Frame(self.big_frame, background="#333", bd=5, relief="ridge")
        self.frame_1.grid(row=0, column=0, padx=(20, 10), pady=(20, 10))

        # Creates a second frame inside the gradient frame, to the right of the first frame. This holds the buttons.
        self.frame_2 = tk.Frame(self.big_frame, background="")
        self.frame_2.grid(row=0, column=1, padx=(0, 20), pady=(20, 10))

        # Creates a third frame inside the gradient frame, below the first two frames. This hold the progress bar.
        # The frame is hidden and only appears while the board is being solved.
        self.frame_3 = tk.Frame(self.big_frame, background="")

        # Creates a nested list of integers. This is a skeleton meant to hold the Entry widgets later.
        self.board = [[0] * 9 for _ in range(9)]

        # Creates the top menu bar.
        self.menubar = Menu(self.window)
        self.window.configure(menu=self.menubar)

        # Creates the File menu in menu bar.
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Clear", command=self.clear_button)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.window.destroy)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        # Creates the Help menu in menu bar.
        self.help_menu = Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="How to Use", command=Window1.how_to_use)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        # Creates the board and all Entry widgets within it.
        for i in range(9):
            for j in range(9):
                self.board[i][j] = tk.Entry(self.frame_1, width=2, justify='center', bd=1, background="white",
                                            font=("Helvetica", "20"))
                if i in [3, 6]:
                    self.board[i][j].grid(pady=(5, 0))
                if j in [3, 6]:
                    self.board[i][j].grid(padx=(5, 0))

                self.board[i][j].grid(row=i, column=j)

        button_text = ["Clear", "Update", "Solve"]
        buttons = [0, 0, 0]

        # Create the buttons for the board actions.
        for i, j in enumerate([1, 4, 7]):
            buttons[i] = tk.Button(self.frame_2, width=10, text=button_text[i], font=("Helvetica", 16, "bold"))
            buttons[i].grid(row=j, column=10, padx=10, pady=40)

        buttons[0].configure(command=self.clear_button)
        buttons[1].configure(command=self.update_button)
        buttons[2].configure(command=self.multi_solve)

        # Creates the progress bar.
        self.progress_bar = ttk.Progressbar(self.frame_3, orient="horizontal", length=480, mode="indeterminate")
        self.progress_bar.pack()

    @staticmethod
    def how_to_use():
        """
        Static Function. Displays a message pop-up containing instructions.
        :return:
        """
        msg.showinfo("Instructions",
                     "1. Enter the available numbers at their respective positions on the board."
                     "\n2. Click the Update button."
                     "\n3. Click the Solve button.")

    @staticmethod
    def validate(val):
        """
        Checks if an entered number is valid on the board. Raises ValueError if number is not valid.
        :param val: String.
        :return: None
        """
        if val.isnumeric():
            if int(val) < 1 or int(val) > 9:
                raise ValueError("Invalid number")
        else:
            raise ValueError("Invalid number")

    def is_board_updated(self):
        """
        Checks if the board has any values that are not present in the SudokuBoard object.
        :return: bool. True if the board is updated, False otherwise.
        """
        for i in range(9):
            for j in range(9):
                if self.board[i][j].get() != "" and self.board[i][j]["state"] == "disabled":
                    pass
                elif self.board[i][j].get() == "":
                    pass
                else:
                    return False
        return True

    def refresh(self):
        """
        Updates the window object every second. Used for running other operations simultaneously.
        :return: None
        """
        self.window.update()
        self.window.after(1000, self.refresh)

    def multi_solve(self):
        """
        Starts a separate thread for solve_button().
        :return: None
        """
        self.refresh()
        threading.Thread(target=self.solve_button).start()

    def clear_button(self):
        """
        Clears the board after confirmation.
        :return: None
        """
        answer = msg.askyesno("Confirm Clearing", "Are you sure you want to clear the board?")
        if answer:
            self.s.clear()
            for i in range(9):
                for j in range(9):
                    self.board[i][j].configure(state="normal", fg="black", bg="#ffffff")
                    self.board[i][j].delete(0, "end")
        else:
            return None

    def update_button(self):
        """
        Updates the values on the board to the SudokuBoard object.
        :return: None
        """
        for i in range(9):
            for j in range(9):
                # Check if cell is non-empty.
                if self.board[i][j].get() != "":
                    try:
                        # Validation function for cell.
                        Window1.validate(self.board[i][j].get())
                        self.s.ui_update_board(int(self.board[i][j].get()), i, j)
                        # Disable the current cell to prevent further changes.
                        self.board[i][j].configure(state='disabled')
                    except ValueError:
                        msg.showerror("Invalid Value", f"There is an invalid value at row:{i + 1}, column:{j + 1}.")
                        return None

    def solve_button(self):
        """
        Initiates the board-solving and other related operations.
        :return: None
        """
        # Checks if the board has been updated properly.
        if self.check_update():
            self.progress_bar_start()
            self.solve_board()
            self.progress_bar_stop()

    def solve_board(self):
        """
        Calls the SudokuBoard solve(). Solves the current board.
        :return: None
        """
        result = self.s.solve()
        # Solved board is stored in a local list.
        self.s_copy = self.s.full_board()
        if result:
            self.board_updator()
        else:
            msg.showerror("Error while Solving", "The board could not be Solved."
                                                 "\nThe values on the board do not seem to be correct.")

    def board_updator(self):
        """
        Updates the board on the window with values if the solved board.
        :return:
        """
        for i in range(9):
            for j in range(9):
                self.board[i][j].delete(0, "end")
                self.board[i][j].insert(0, self.s_copy[i][j])
                # self.board[i][j].configure(bg="#2997ae", fg="#ffffff")
                self.board[i][j].configure(bg="#23749a", fg="#ffffff")
                # self.board[i][j].configure(state='disabled')

    def check_update(self):
        """
        Calls is_board_updated() and takes actions based on the result.
        :return: bool. True if operations can continue. False otherwise.
        """
        if self.is_board_updated():
            return True
        else:
            answer = msg.askyesno("Board Clear Warning", "Board is not updated."
                                                         "\nSolving the board now will result in loss "
                                                         "of the values currently on the board."
                                                         "\n Do you wish to continue?")

            if answer:
                return True
            else:
                return False
        pass

    def progress_bar_start(self):
        """
        Reveals the third frame and progress bar. Then starts the progress bar.
        :return: None
        """
        self.frame_3.grid(row=1, column=0, columnspan=2)
        self.progress_bar.start()

    def progress_bar_stop(self):
        """
        Stops the progress bar. Then hides the frame and the progress bar.
        :return: None
        """
        self.progress_bar.stop()
        self.frame_3.grid_remove()
        self.window.update()


if __name__ == "__main__":
    main()
