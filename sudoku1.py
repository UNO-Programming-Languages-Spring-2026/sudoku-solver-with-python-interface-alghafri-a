import sys
import clingo
from sudoku_board import Sudoku


class SudokuApp(clingo.Application):
    program_name = "sudoku1"

    def print_model(self, model, printer):
        atoms = sorted(str(sym) for sym in model.symbols(shown=True))
        print(" ".join(atoms))

    def main(self, ctl, files):
        for f in files:
            ctl.load(f)
        ctl.ground([("base", [])])
        ctl.solve(on_model=lambda m: None)


if __name__ == "__main__":
    clingo.clingo_main(SudokuApp(), sys.argv[1:])
