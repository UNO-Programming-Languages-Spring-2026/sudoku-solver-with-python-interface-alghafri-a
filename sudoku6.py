import sys
import clingo
import clingo.symbol
from sudoku_board import Sudoku


class Context:

    def __init__(self, board: Sudoku):
        self.board = board

    def initial(self) -> list:
        result = []
        for (row, col), val in sorted(self.board.board.items()):
            tup = clingo.Function("", [
                clingo.Number(row),
                clingo.Number(col),
                clingo.Number(val)
            ], True)
            result.append(tup)
        return result


class SudokuApp(clingo.Application):
    program_name = "sudoku6"

    def __init__(self):
        self.context = None

    def print_model(self, model, printer):
        sudoku = Sudoku.from_model(model)
        print(str(sudoku))

    def main(self, ctl, files):
        txt_file = None
        lp_files = []
        for f in files:
            if f.endswith(".txt"):
                txt_file = f
            else:
                lp_files.append(f)

        if txt_file:
            with open(txt_file) as fh:
                board = Sudoku.from_str(fh.read())
        else:
            board = Sudoku({})

        self.context = Context(board)

        ctl.load("sudoku.lp")
        ctl.load("sudoku_py.lp")
        for f in lp_files:
            ctl.load(f)

        ctl.ground([("base", [])], context=self.context)
        ctl.solve(on_model=lambda m: None)


if __name__ == "__main__":
    clingo.clingo_main(SudokuApp(), sys.argv[1:])
