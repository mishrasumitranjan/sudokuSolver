# sudokuSolver
#### Video Demo: [https://youtu.be/RrX8sP15V4E](https://youtu.be/RrX8sP15V4E)
#### Description:

**_<TL;DR> -_** Solves Sudoku. Uses GUI. Run `project.py` if you got the code.
Run `project.exe` if you got the distributable.

This project is a simple implementation of Bruteforce Backtracking algorithm used
to solve a Sudoku Board problem. It uses a GUI made using `tkinter` to receive
values and display the result.

The program consists of four functional components.
1. **Main Project File -**
    This file creates the UI window and calls the `Window1` class.

2. **Window1 Class File -**
    This file implements all the widgets of the window and interacts with
    the `SudokuBoard` class in board.py to pass the input values and retrieve
    the results.

3. **SudokuBoard Class File -**
    This file implements the functional aspects of the board and is also
responsible for solving the Sudoku board problem.

4. **GradientFrame Class File -**
    This file implements the gradient background implemented in the window.


### Main Project File (project.py)
This file has no purpose other than creating a blank `Tk()` object and passing it
to the `Window1` class initializing a `Window1` class object.


### Window1 Class File (window_1.py)
This file receives the `Tk()` object from the project.py file and creates the
entire window within it. The first object that is created is a `GradientFrame`
object _(described below)_. Three more `Frame` objects are created within the
`GradientFrame` object.

The first Frame contains the `Entry` widgets that make up the Sudoku board. The
`Entry` widgets are created using two nested `for` loops, with padding in
appropriate places to create the smaller grid structure.

The second Frame contains the buttons that control all the functions related to the
board. The frame contains three buttons.
- **Clear button** - Clears the board and resets the `SudokuBoard` class.
  - Triggers a Confirmation dialog asking user to confirm clearing the board.
  - Answering 'Yes' on the dialog clears the numbers on the UI board and resets all
  values in the board in `SudokuBoard` object to 0, thus resetting the board.
- **Update button** - Updates the values input into the GUI board onto the
  `SudokuBoard` class.
  - Clicking the button two nested `for` loops which call a function on every
    iteration that validates the values input into the GUI board.
    - If the validation fails on any iteration, a `ValueError` exception is raised
      and an Error pop-up is shown along with the location of the current element.
    - If the validation passes, the program continues on.
  - If the validation passes, the program then checks if the`Entry` widgets is
    non-empty and passes the value, row and column to be updated in the board
    of `SudokuBoard` object.
  - The Entry widgets of the values that get updated are disabled to avoid any
    unintended changes.
- **Solve button** - Solves the Sudoku board and updates the solution in the
  remaining places.
  - Clicking the button calls a method which checks if there are any non-empty
    cells in the board, that have not been updated in the board of `SudokuBoard`
    object.
  - If any such cell is detected, the method triggers a Confirmation dialog
    asking the user to confirm if they want to continue solving the Sudoku board
    without the values.
    - Answering 'Yes' ignores the values that have not been updated and continues
      to the next step.
    - Answering 'No' returns the user to the board without continuing the operations.
  - If 'Yes' is answered, or if all values have been correctly updated, the program
    then starts a new Thread that calls the functions related to solving the
    Sudoku board.
  - The Thread first reveals the third Frame _(see below)_ and then starts the
    progress bar.
  - It then calls the method in `SudokuBoard` class that solves the board.
  - Once the board has been solved, each value of the solution is written in its
    respective location _(excluding the disabled cells)_.
  - After that, the Thread stops the progress bar and hides the third Frame.
  - If the board has not been solved, the method triggers an Error pop-up informing
    the user about the same.

The third Frame contains an indeterminate progress bar which appears while the board
is being solved. The progress bar disappears once the solution has been displayed.
This is to ensure that users to do assume that the window is frozen if the program is
taking longer than usual to solve the board.

The `Window1` class also creates a Menu object which contains a File menu dropdown
and a Help menu dropdown.
- The File menu dropdown contains two options - *Clear* and *Exit*
  - **Clear** - Has the same functionality as the Clear button.
  - **Exit** - Exits the program immediately.
- The Help menu dropdown contains one option - *How to Use*
  - **How to Use** - Opens a Dialog Box containing the instructions on how to
    use the program.

The `Window1` class also contains other methods which support the functionality of the
widgets and establish connection between the `Window1` class object and the
`SudokuBoard` class object.

### SudokuBoard Class File (board.py)
This file contains the board structure and all its relevant functions.

The method that solves the board looks for an empty cell in the board.
- If an empty cell is found, the method starts a for loop of all values valid
  on the board and checks if the value is present in the same row, column or
  smaller grid.
  - If the value is found in any of the locations, the program continues to the
    next value in the `for` loop
  - If the value is not found, the program fills in the current value and calls
    the method again.
  - If the method returns False, the value is changed back to 0 and the for loop
    moves onto the next value.
- If an empty cell in not found, it means that the board is solved and the
  program returns True.
- The method returns False if the current board cannot be solved.

The file comes with a `handler` method, which can be used to test the `board.py` file
directly from the terminal.


### GradientFrame Class File (gradient_check.py)
This file contains a class that inherits the `Canvas` Class from `tkinter`, takes two
colors as parameters and creates the gradient background.

The `GradientFrame` class achieves the same by taking the RGB values of both colors
and finding their difference. The difference is then applied to one color, a little
at a time across the width of the `Canvas` object using a loop until it reaches the
target color.
