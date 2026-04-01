import sys
import clingo


class SudokuApp(clingo.Application):
    program_name = "sudoku1"
    version = "1.0"

    def main(self, control: clingo.Control, files):
        control.load("solutions/sudoku.lp")
        for f in files:
            control.load(f)
        control.ground([("base", [])])
        control.solve()

    def print_model(self, model: clingo.solving.Model, printer):
        atoms = sorted(str(symbol) for symbol in model.symbols(shown=True))
        printer(" ".join(atoms))


if __name__ == "__main__":
    sys.exit(clingo.clingo_main(SudokuApp(), sys.argv[1:]))
