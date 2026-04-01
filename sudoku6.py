import sys
import clingo
from clingo.application import Application, clingo_main
from sudoku_board import Sudoku


class Context:
    def __init__(self, board: Sudoku):
        self.board = board

    def initial(self):
        result = []
        for (row, col), value in self.board.sudoku.items():
            result.append(
                clingo.Function(
                    "",
                    [clingo.Number(row), clingo.Number(col), clingo.Number(value)],
                    True,
                )
            )
        return result


class SudokuApp(Application):
    program_name = "sudoku6"
    version = "1.0"

    def main(self, control, files):
        with open(files[0], "r", encoding="utf-8") as f:
            text = f.read()

        sudoku = Sudoku.from_str(text)
        context = Context(sudoku)

        control.load("sudoku.lp")
        control.load("sudoku_py.lp")
        control.ground([("base", [])], context=context)
        control.solve()

    def print_model(self, model, printer):
        sudoku = Sudoku.from_model(model)
        printer(str(sudoku))


if __name__ == "__main__":
    sys.exit(clingo_main(SudokuApp(), sys.argv[1:]))
