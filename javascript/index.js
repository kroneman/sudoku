const Sudoku = require('./sudoku');

const sudokuInstance = new Sudoku([
    // [6,  5,  9,  8,  1,  2,  3,  7,  4],
    // [8,  7,  3,  5,  6,  4,  1,  9,  2],
    // [2,  4,  1,  3,  9,  7,  5,  8,  6],

    // [4,  8,  6,  1,  2,  3,  7,  5,  9],
    // [5,  2,  7,  9,  4,  6,  8,  3,  1]
]);

sudokuInstance.generateGame();
console.log(sudokuInstance.print);