import sys
import clingo
import clingo.symbol
from sudoku_board import Sudoku


SUDOKU_ENCODING = """
{ sudoku(R,C,V) : V = 1..9 } = 1 :- R = 1..9, C = 1..9.
sudoku(R,C,V) :- initial(R,C,V).
:- sudoku(R,C1,V), sudoku(R,C2,V), C1 != C2.
:- sudoku(R1,C,V), sudoku(R2,C,V), R1 != R2.
:- sudoku(R1,C1,V), sudoku(R2,C2,V), R1 != R2,
   (R1-1)/3 == (R2-1)/3, (C1-1)/3 == (C2-1)/3.
#show sudoku/3.
"""

BRIDGE = """
initial(R,C,V) :- (R,C,V) = @initial().
"""


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

        context = Context(board)

        ctl.add("base", [], SUDOKU_ENCODING)
        ctl.add("base", [], BRIDGE)
        for f in lp_files:
            ctl.load(f)

        ctl.ground([("base", [])], context=context)
        ctl.solve(on_model=lambda m: None)


if __name__ == "__main__":
    clingo.clingo_main(SudokuApp(), sys.argv[1:])
