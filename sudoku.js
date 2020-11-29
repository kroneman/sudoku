const lodash = require("lodash");
const range = [1, 2, 3, 4, 5, 6, 7, 8, 9];
const regionStart = {
  1: {
    row: 0,
    col: 0,
  },
  2: {
    row: 0,
    col: 3,
  },
  3: {
    row: 0,
    col: 6,
  },
  4: {
    row: 3,
    col: 0,
  },
  5: {
    row: 3,
    col: 3,
  },
  6: {
    row: 3,
    col: 6,
  },
  7: {
    row: 6,
    col: 0,
  },
  8: {
    row: 6,
    col: 3,
  },
  9: {
    row: 6,
    col: 6,
  },
};

module.exports = class Sudoku {
  constructor(grid = []) {
    this.grid = [...grid];
  }

  /**
   * Visual representation
   */
  get print() {
    const visualPuzzle = this.grid.reduce(
      (result, row) => `${result}
            ${row.join(" | ")}`,
      ""
    );
    console.log(visualPuzzle);
  }

  /**
   * Progressively generates a game (recursively)
   */
  generateGame() {
    this.addRow();
    if (this.grid.length < 9) {
      return this.generateGame();
    }
  }

  addRow() {
    let isValid = false;
    let row = null;

    while (!isValid) {
      row = this.generateRow();
      isValid = this.validatesGrid(row);
    }

    this.grid = [...this.grid, row];
    console.log(this.print);
  }

  generateRow() {
    return range.reduce((currentRow, current, col) => {
      const currentColumn = this.grid.length
        ? this.grid.map((row) => row[col])
        : [];
      const possibleRowValues = lodash.difference(range, currentRow);
      const possibleColValue = lodash.difference(possibleRowValues, currentColumn);
      const regionId = this.findRegionByCoordinates(col);
      const regionValues = this.getRegion(regionId);
      const possibleValues = lodash.difference(
        possibleColValue,
        regionValues
      );

      const currentValue = lodash.sample(possibleValues);
      return [
        ...currentRow,
        currentValue
      ];
    }, []);
  }

  validatesGrid(row) {
    const newGrid = [
      ...this.grid,
      row
    ];

    if (!this.validateRow(newGrid, row)) {
      return false;
    }

    if (!this.validateColumns(newGrid, row)) {
      return false;
    }

    if (!this.validateRegions(newGrid, row)) {
      return false;
    }

    return true;
  }

  validateRow(newGrid, row) {
    return row.every(val => !!val);
  }

  validateColumns(newGrid, row) {
    const isEveryRowUnique = row.every((item, index) => {
      const column = newGrid.map((gridRow) => gridRow[index]);
      const uniqueColumn = lodash.uniq(column);
      const columnLength = column.length;
      const uniqueLength = uniqueColumn.length;
      return columnLength === uniqueLength;
    });

    return isEveryRowUnique;
  }

  validateRegions(newGrid, row) {
    const isRegionValid = range.every((regionId) => {
      const region = this.getRegion(regionId, newGrid);
      const uniqueRegion = lodash.uniq(region);
      return region.length === uniqueRegion.length;
    });

    return isRegionValid;
  }

  findRegionByCoordinates(col, row = this.grid.length) {
    if (row < 3) {
      if (col < 3) {
        return 1;
      }

      if (col < 6) {
        return 2;
      }

      return 3;
    }

    if (row < 6) {
      if (col < 3) {
        return 4;
      }

      if (col < 6) {
        return 5;
      }

      return 6;
    }

    if (col < 3) {
      return 7;
    }

    if (col < 6) {
      return 8;
    }

    return 9;
  }

  getRegion(id = 1, grid = this.grid) {
    const { row, col } = regionStart[id];
    const result = [];
    let numRows = 3;
    let numRow = 0;
    while (numRow < numRows) {
      const currentRow = grid[numRow + row];

      if (currentRow) {
        let numColumns = 3;
        let numColumn = 0;
        while (numColumn < numColumns) {
          const value = currentRow[numColumn + col];
          result.push(value);
          numColumn += 1;
        }
      }

      numRow += 1;
    }
    return result;
  }
};
