row(1..9).
col(1..9).
val(1..9).

% each cell has exactly one value
1 { sudoku(R,C,V) : val(V) } 1 :- row(R), col(C).

% keep the given clues
sudoku(R,C,V) :- initial(R,C,V).

% no repeated value in a row
:- sudoku(R,C1,V), sudoku(R,C2,V), C1 != C2.

% no repeated value in a column
:- sudoku(R1,C,V), sudoku(R2,C,V), R1 != R2.

% no repeated value in a 3x3 block
block(1,1). block(1,4). block(1,7).
block(4,1). block(4,4). block(4,7).
block(7,1). block(7,4). block(7,7).

in_block(R,C,BR,BC) :-
    row(R), col(C), block(BR,BC),
    R >= BR, R < BR+3,
    C >= BC, C < BC+3.

:- sudoku(R1,C1,V), sudoku(R2,C2,V),
   (R1,C1) != (R2,C2),
   in_block(R1,C1,BR,BC),
   in_block(R2,C2,BR,BC).

#show sudoku/3.
