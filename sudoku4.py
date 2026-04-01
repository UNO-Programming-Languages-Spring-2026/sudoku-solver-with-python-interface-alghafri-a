import sys
import clingo
from sudoku_board import Sudoku


class SudokuApp(clingo.Application):
    program_name = "sudoku4"
    version = "1.0"

    def main(self, control: clingo.Control, files):
        control.load("solutions/sudoku.lp")
        for f in files:
            control.load(f)
        control.ground([("base", [])])
        control.solve()

    def print_model(self, model: clingo.solving.Model, printer):
        sudoku = Sudoku.from_model(model)
        printer(str(sudoku))


if __name__ == "__main__":
    sys.exit(clingo.clingo_main(SudokuApp(), sys.argv[1:]))
