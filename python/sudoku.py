from constants import number_range, region_start_dict
from pydash import sample
from pydash.arrays import difference
from functools import reduce
from datetime import datetime

class Sudoku:
    # Defaulting grid = [] so that I can start from a partially solved puzzle
    def __init__(self, grid = [], debug = False):
      self.grid = grid
      self.DEBUG = bool(debug)
      self.start_time = datetime.now()

    def time_since_start(self):
      return datetime.now() - self.start_time

    def print(self):
      visual_puzzle = reduce(self.print_row, self.grid, "")
      print(visual_puzzle)

    # using _ to denote unused variables throughout this file
    def print_row(_, result, current):
      # https://www.programiz.com/python-programming/string-interpolation
      # f strings added in python 3.6
      return f'{result}\n{" | ".join(str(i) for i in current)}'

    # Recursively calls itself until all the rows (9 of them) are present
    def generate_game(self):
      self.add_row()
      if (len(self.grid) < 9):
        return self.generate_game()

    # generates a possible row, then validates before adding to the main grid
    # this way when we run into an impossible situation
    # the row gets tossed out and we try again
    def add_row(self):
      is_valid = False
      row = False

      while(is_valid == False):
        row = self.generate_row()
        is_valid = self.validate_grid(row)
        duration = self.time_since_start()
        if duration.seconds > 10:
          print("Long running process") 

      self.grid = [*self.grid, row]
      if self.DEBUG:
        self.print()

    # Uses the initial number_range as a base to loop through
    def generate_row(self):
      result = reduce(self.generate_row_item, number_range, [])
      return result

    # finds possible values for each cell based on validation rules
    # picks a random one using sample
    # if it runs into an impossible solution len(possible_values) < 1
    # places a None value as a placeholder
    # this will get caught by the post-generation validation and the row gets tossed
    def generate_row_item(self, current_row, _):
      col = len(current_row)
      current_column = (
        [],
        list(map(lambda row: row[col], self.grid))
      )[len(self.grid) > 0]
      region_id = self.find_region(col)
      region_values = self.get_region(region_id)

      possible_row_values = difference(number_range, current_row)
      possible_col_values = difference(possible_row_values, current_column)
      possible_values = difference(possible_col_values, region_values)
      current_value = self.sample_or_none(possible_values)

      return [*current_row, current_value]

    # Sample throws an error when an empty array is passed
    def sample_or_none(_, possible_values):
      if (len(possible_values) > 0):
        return sample(possible_values)

      return None

    # Validates a proposed new_grid before finalizing
    # new grid must match row_validation (no duplicates)
    # colum_validation (no duplicates)
    # region validation (no duplicates)
    def validate_grid(self, row):
      new_grid = [*self.grid, row]

      # Checks if all items in the array are true
      return all([
        self.validate_row(row),
        self.validate_columns(new_grid, row),
        self.validate_regions(new_grid)
      ])

    # Checks if each partial column is unique
    def validate_columns(self, new_grid, row):
      return all(self.is_column_unique(new_grid, i) for i, _ in enumerate(row))

    # Checks a partial column for uniqueness
    def is_column_unique(_, new_grid, index):
      column = []
      if (len(new_grid) > 0):
        column = list(map(lambda grid_row: grid_row[index], new_grid))

      unique_column = set([*column])
      return len(column) == len(unique_column)

    # Checks a row for "None" values
    # Tosses it out as a proposed next grid if it doesn't
    def validate_row(_, row):
      return all(bool(item) == True for item in row)

    # Each region or 3x3 grid gets validated for uniqueness
    def validate_regions(self, new_grid):
      return all(self.validate_region(region_id, new_grid) for region_id in number_range)

    # Validates a single region
    def validate_region(self, region_id, new_grid):
      region = self.get_region(region_id, new_grid)
      unique_region = set([*region])
      return len(unique_region) == len(region)

    # Finds a region based on the current column
    # and progress of the grid
    # @todo: clean this up
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

    # Retrieves a given 3x3 grid based on region number
    # grid is optional param so we can get the regions from a proposed grid
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


