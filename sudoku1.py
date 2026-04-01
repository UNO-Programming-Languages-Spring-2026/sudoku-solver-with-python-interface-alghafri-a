import sys
from clingo.application import Application, clingo_main


class SudokuApp(Application):
    program_name = "sudoku1"
    version = "1.0"

    def main(self, control, files):
        control.load("sudoku.lp")
        for f in files:
            control.load(f)
        control.ground([("base", [])])
        control.solve()

    def print_model(self, model, printer):
        atoms = sorted(str(sym) for sym in model.symbols(shown=True))
        printer(" ".join(atoms))


if __name__ == "__main__":
    sys.exit(clingo_main(SudokuApp(), sys.argv[1:]))
