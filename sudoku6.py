import sys
from pathlib import Path
import clingo
from clingo.application import Application, clingo_main
from sudoku_board import Sudoku


class Context:
    def __init__(self, board: Sudoku):
        self.board = board

    def initial(self):
        facts = []
        for (r, c), v in self.board.sudoku.items():
            facts.append(
                clingo.Function(
                    "initial",
                    [clingo.Number(r), clingo.Number(c), clingo.Number(v)]
                )
            )
        return facts


class SudokuApp(Application):
    program_name = "sudoku6"
    version = "1.0"

    def main(self, control, files):
        if not files:
            raise RuntimeError("Missing input file")

        input_file = files[0]

        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()

        board = Sudoku.from_str(text)
        context = Context(board)

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

        control.load("sudoku_py.lp")
        control.ground([("base", [])], context=context)
        control.solve()

    def print_model(self, model, printer):
        sudoku = Sudoku.from_model(model)
        printer(str(sudoku))


if __name__ == "__main__":
    clingo_main(SudokuApp(), sys.argv[1:])
