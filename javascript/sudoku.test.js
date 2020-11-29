const Sudoku = require("./sudoku");
const { expect } = require("chai");

describe("Sudoku", () => {
  describe("Identifying a quadrant", () => {
    it("Finds region One", () => {
      const puzzle = new Sudoku();
      const region = puzzle.findRegionByCoordinates(2, 2);
      expect(region).to.equal(1);
    });

    it("Finds region Two", () => {
      const puzzle = new Sudoku();
      const region = puzzle.findRegionByCoordinates(4, 2);
      expect(region).to.equal(2);
    });

    it("Finds region Three", () => {
      const puzzle = new Sudoku();
      const region = puzzle.findRegionByCoordinates(6, 2);
      expect(region).to.equal(3);
    });

    it("Finds region Four", () => {
      const puzzle = new Sudoku();
      const region = puzzle.findRegionByCoordinates(2, 4);
      expect(region).to.equal(4);
    });

    it("Finds region Five", () => {
      const puzzle = new Sudoku();
      const region = puzzle.findRegionByCoordinates(4, 4);
      expect(region).to.equal(5);
    });

    it("Finds region Six", () => {
      const puzzle = new Sudoku();
      const region = puzzle.findRegionByCoordinates(6, 4);
      expect(region).to.equal(6);
    });

    it("Finds region Seven", () => {
      const puzzle = new Sudoku();
      const region = puzzle.findRegionByCoordinates(2, 6);
      expect(region).to.equal(7);
    });

    it("Finds region Eight", () => {
      const puzzle = new Sudoku();
      const region = puzzle.findRegionByCoordinates(4, 6);
      expect(region).to.equal(8);
    });

    it("Finds region Nine", () => {
      const puzzle = new Sudoku();
      const region = puzzle.findRegionByCoordinates(6, 6);
      expect(region).to.equal(9);
    });
  });

  describe("Retrieving a quadrant", () => {
    it("It can retrieve a quadrant", () => {
      const puzzle = new Sudoku([
        [2 , 3 , 6 , 5 , 1 , 8 , 7 , 4 , 9],
        [8 , 5 , 4 , 9 , 7 , 6 , 2 , 1 , 3],
        [7 , 1 , 9 , 2 , 3 , 4 , 8 , 6 , 5],

        [1 , 9 , 2 , 3 , 5 , 7 , 6 , 8 , 4],
        [6 , 4 , 5 , 1 , 8 , 9 , 3 , 2 , 7],
        [3 , 8 , 7 , 4 , 6 , 2 , 5 , 9 , 1],

        [5 , 6 , 1 , 8 , 9 , 3 , 4 , 7 , 2],
        [4 , 7 , 3 , 6 , 2 , 1 , 9 , 5 , 8]
      ]);

      const region = puzzle.getRegion(7);
      expect(region).to.deep.equal([5, 6, 1, 4, 7, 3]);
    });  
  });
  
});
