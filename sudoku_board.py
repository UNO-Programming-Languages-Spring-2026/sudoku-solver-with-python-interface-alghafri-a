import clingo
try:
    import clingo.solving
except Exception:
    pass


class Sudoku:

    def __init__(self, board: dict):
        self.board = board
        self.sudoku = board

    @classmethod
    def from_model(cls, model) -> 'Sudoku':
        board = {}
        for sym in model.symbols(shown=True):
            if sym.name == "sudoku" and len(sym.arguments) == 3:
                row = sym.arguments[0].number
                col = sym.arguments[1].number
                val = sym.arguments[2].number
                board[(row, col)] = val
        return cls(board)

    @classmethod
    def from_str(cls, s: str) -> 'Sudoku':
        sudoku = {}
        lines = [line for line in s.splitlines() if line.strip() != ""]
        row = 1
        for line in lines:
            tokens = line.split()
            col = 1
            for token in tokens:
                if token != "-":
                    sudoku[(row, col)] = int(token)
                col += 1
            row += 1
        return cls(sudoku)

    def __str__(self) -> str:
        s = ""
        for row in range(1, 10):
            if row in (4, 7):
                s += "\n"
            row_str = ""
            for col in range(1, 10):
                if col in (4, 7):
                    row_str += " "
                val = self.board.get((row, col), "-")
                row_str += str(val)
                if col < 9:
                    row_str += " "
            s += row_str + "\n"
        return s.rstrip("\n")
