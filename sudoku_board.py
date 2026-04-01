from typing import Tuple
import clingo


class Sudoku:
    def __init__(self, sudoku: dict[Tuple[int, int], int]):
        self.sudoku = sudoku

    def __str__(self) -> str:
        rows = []
        for r in range(1, 10):
            cells = []
            for c in range(1, 10):
                cells.append(str(self.sudoku[(r, c)]))
            row = " ".join(cells[0:3]) + "  " + " ".join(cells[3:6]) + "  " + " ".join(cells[6:9])
            rows.append(row)

        s = "\n".join(rows[0:3]) + "\n\n" + "\n".join(rows[3:6]) + "\n\n" + "\n".join(rows[6:9])
        return s

    @classmethod
    def from_str(cls, s: str) -> "Sudoku":
        sudoku = {}
        lines = [line.strip() for line in s.splitlines() if line.strip() != ""]

        for r, line in enumerate(lines, start=1):
            tokens = line.split()
            for c, token in enumerate(tokens, start=1):
                if token != "-":
                    sudoku[(r, c)] = int(token)

        return cls(sudoku)

    @classmethod
    def from_model(cls, model: clingo.solving.Model) -> "Sudoku":
        sudoku = {}
        for sym in model.symbols(shown=True):
            if sym.name == "sudoku" and len(sym.arguments) == 3:
                row = sym.arguments[0].number
                col = sym.arguments[1].number
                val = sym.arguments[2].number
                sudoku[(row, col)] = val

        return cls(sudoku)
