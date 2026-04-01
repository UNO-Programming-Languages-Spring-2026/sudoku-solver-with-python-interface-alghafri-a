import sys
import clingo
from sudoku_board import Sudoku


SUDOKU_LP = """\
{ sudoku(R,C,V) : V = 1..9 } = 1 :- R = 1..9, C = 1..9.
sudoku(R,C,V) :- initial(R,C,V).
:- sudoku(R,C1,V), sudoku(R,C2,V), C1 != C2.
:- sudoku(R1,C,V), sudoku(R2,C,V), R1 != R2.
:- sudoku(R1,C1,V), sudoku(R2,C2,V),
   R1 != R2, (R1-1)/3 == (R2-1)/3, (C1-1)/3 == (C2-1)/3.
#show sudoku/3.
"""


class SudokuApp(clingo.Application):
    program_name = "sudoku4"

    def print_model(self, model, printer):
        sudoku = Sudoku.from_model(model)
        print(str(sudoku))

    def main(self, ctl, files):
        ctl.add("base", [], SUDOKU_LP)
        for f in files:
            ctl.load(f)
        ctl.ground([("base", [])])
        ctl.solve(on_model=lambda m: None)


if __name__ == "__main__":
    clingo.clingo_main(SudokuApp(), sys.argv[1:])
