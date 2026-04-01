import sys
import clingo
from clingo.application import Application, clingo_main


class SudokuApp(Application):
    program_name = "sudoku1"
    version = "1.0"

    def main(self, control: clingo.Control, files):
        control.load("solutions/sudoku.lp")
        for f in files:
            control.load(f)
        control.ground([("base", [])])
        control.solve()

    def print_model(self, model, printer):
        symbols = model.symbols(shown=True)
        atoms = sorted(str(sym) for sym in symbols)
        printer(" ".join(atoms))


if __name__ == "__main__":
    clingo_main(SudokuApp(), sys.argv[1:])
