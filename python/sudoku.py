import functools
import pydash

range = [1, 2, 3, 4, 5, 6, 7, 8, 9]
region_start_dict = {
  1: {
    "row": 0,
    "col": 0,
  },
  2: {
    "row": 0,
    "col": 3,
  },
  3: {
    "row": 0,
    "col": 6,
  },
  4: {
    "row": 3,
    "col": 0,
  },
  5: {
    "row": 3,
    "col": 3,
  },
  6: {
    "row": 3,
    "col": 6,
  },
  7: {
    "row": 6,
    "col": 0,
  },
  8: {
    "row": 6,
    "col": 3,
  },
  9: {
    "row": 6,
    "col": 6,
  }
}

class Sudoku:
    def __init__(self, grid = []):
      self.grid = grid

    def print(self):
      visual_puzzle = functools.reduce(self.print_row, self.grid, "")
      print(visual_puzzle)

    def print_row(self, result, current):
      return "" + result + "\n" + " | ".join(str(i) for i in current)

    def generate_game(self):
      self.add_row()
      if (len(self.grid) < 9):
        return self.generate_game()

    def add_row(self):
      is_valid = False
      row = False

      while(is_valid == False):
        row = self.generate_row()
        is_valid = self.validate_grid(row)

      self.grid = [*self.grid, row]
      self.print()

    def generate_row(self):
      result = functools.reduce(self.generate_row_item, range, [])
      return result

    def generate_row_item(self, current_row, currentItem):
      col = len(current_row)
      current_column = (
        [],
        list(map(lambda row: row[col], self.grid))
      )[len(self.grid) > 0]

      possible_row_values = pydash.arrays.difference(range, current_row)
      possible_col_values = pydash.arrays.difference(possible_row_values, current_column)
      region_id = self.find_region(col)
      region_values = self.get_region(region_id)
      possible_values = pydash.arrays.difference(possible_col_values, region_values)
      current_value = None

      if len(possible_values) > 0:
        current_value = pydash.sample(possible_values)

      return [*current_row, current_value]

    def validate_grid(self, row):
      new_grid = [*self.grid, row]

      if (self.validate_row(new_grid, row) == False):
        return False

      if (self.validate_columns(new_grid, row) == False):
        return False

      if (self.validate_regions(new_grid, row) == False):
        return False

      return True

    def validate_columns(self, new_grid, row):
      return all(self.is_column_unique(new_grid, i) for i, item in enumerate(row))

    def is_column_unique(self, new_grid, index):
      column = []
      if (len(new_grid) > 0):
        column = list(map(lambda grid_row: grid_row[index], new_grid))

      unique_column = pydash.arrays.uniq(column)
      return len(column) == len(unique_column)

    def validate_row(self, new_grid, row):
      return all(bool(item) == True for item in row)

    def validate_regions(self, new_grid, row):
      return all(self.validate_region(region_id, new_grid) for region_id in range)

    def validate_region(self, region_id, new_grid):
      region = self.get_region(region_id, new_grid)
      unique_region = pydash.arrays.uniq(region)
      return len(unique_region) == len(region)

    def find_region(self, col):
      row = len(self.grid)

      if (row < 3):
        if (col < 3):
          return 1
        if (col < 6):
          return 2
        return 3

      if (row < 6):
        if (col < 3):
          return 4
        if (col < 6):
          return 5
        return 6

      if (col < 3):
        return 7

      if (col < 6):
        return 8

      return 9

    def get_region(self, id = 1, grid = None):
      if grid is None:
        grid = self.grid

      result = []
      row = region_start_dict[id]["row"]
      col = region_start_dict[id]["col"]

      num_rows = 3
      num_row = 0

      if len(grid) < 1:
        return result

      len_grid = len(grid)
      while (num_row < num_rows and num_row < len_grid):
        row_index = num_row + row
        if(row_index < len_grid):
          current_row = (
            None,
            grid[row_index]
          )[row_index < len(grid)]

          if(current_row):
            num_columns = 3
            num_column = 0
            while (num_column < num_columns):
              value = current_row[num_column + col]
              result.append(value)
              num_column += 1

        num_row += 1

      return result


