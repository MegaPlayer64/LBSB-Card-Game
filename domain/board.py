class Board:

    def __init__(self, width=5, height=3):
        self.width = width
        self.height = height

        self.grid = [
            [None for _ in range(height)]
            for _ in range(width)
        ]

    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.width and 0 <= y < self.height

    def get_unit(self, position):
        x, y = position
        return self.grid[x][y]

    def place_unit(self, unit, position):
        x, y = position
        self.grid[x][y] = unit

    def remove_unit(self, position):
        x, y = position
        self.grid[x][y] = None

    def move_unit(self, from_pos, to_pos):
        unit = self.get_unit(from_pos)
        self.remove_unit(from_pos)
        self.place_unit(unit, to_pos)