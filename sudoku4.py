import sys
import clingo
from sudoku_board import Sudoku


class SudokuApp(clingo.Application):
    program_name = "sudoku4"

    def print_model(self, model, printer):
        sudoku = Sudoku.from_model(model)
        print(str(sudoku))

    def main(self, ctl, files):
        for f in files:
            ctl.load(f)
        ctl.ground([("base", [])])
        ctl.solve(on_model=lambda m: None)


if __name__ == "__main__":
    clingo.clingo_main(SudokuApp(), sys.argv[1:])
