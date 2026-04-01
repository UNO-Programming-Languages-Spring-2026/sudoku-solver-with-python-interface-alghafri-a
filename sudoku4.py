import sys
from pathlib import Path
import clingo
from clingo.application import Application, clingo_main
from sudoku_board import Sudoku


class SudokuApp(Application):
    program_name = "sudoku4"
    version = "1.0"

    def main(self, control, files):
        candidates = [
            Path("sudoku.lp"),
            Path("solutions") / "sudoku.lp",
        ]

        loaded = False
        for path in candidates:
            if path.exists():
                control.load(str(path))
                loaded = True
                break

        if not loaded:
            raise RuntimeError("Could not find sudoku.lp")

        for f in files:
            control.load(f)

        control.ground([("base", [])])
        control.solve()

    def print_model(self, model, printer):
        sudoku = Sudoku.from_model(model)
        printer(str(sudoku))


if __name__ == "__main__":
    clingo_main(SudokuApp(), sys.argv[1:])
