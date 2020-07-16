import random

from players.Player import Player


# Chooses a square that would either be a finishing move or a block
class HardBot(Player):

    def __init__(self, id):
        super().__init__(id)

    def choose_square(self, field):
        self.field = field

        # Finish a line of its own
        chosen_square = self.finish_square(self.id)

        # Block a line of the opponent
        if chosen_square is None:
            chosen_square = self.block_square()

        # Start a line
        if chosen_square is None:
            chosen_square = self.start_line_square()

        if chosen_square is None:
            chosen_square = self.choose_random_square()
        return chosen_square

    def start_line_square(self):
        chosen_square = None
        potential_squares = []

        # Checks the rows
        for i, row in enumerate(self.field):
            if row.count(self.id) == 1 and row.count(None) == 2:
                for j in range(len(row)):
                    if row[j] is None:
                        potential_squares.append({"row": i, "column": j})

        # Checks the columns
        for j in range(len(self.field[0])):
            id_counter = 0
            column_squares = []
            for i in range(len(self.field)):
                element = self.field[i][j]
                if element == self.id:
                    id_counter += 1
                elif element is None:
                    chosen_square = {"row": i, "column": j}
                    column_squares.append(chosen_square)
            if id_counter == 1 and len(column_squares) == 2:
                potential_squares.extend(column_squares)
            else:
                chosen_square = None

        # Checks the diagonal line upper-left to bottom-right
        id_counter = 0
        dia_squares = []
        for i in range(len(self.field)):
            element = self.field[i][i]
            if element == self.id:
                id_counter += 1
            elif element is None:
                chosen_square = {"row": i, "column": i}
                dia_squares.append(chosen_square)
        if id_counter == 1 and len(dia_squares) == 2:
            potential_squares.extend(dia_squares)
        else:
            chosen_square = None

        # Checks the diagonal line upper-right to bottom-left
        id_counter = 0
        dia_squares.clear()
        for i in range(len(self.field)):
            column = len(self.field) - 1 - i
            element = self.field[i][column]
            if element == self.id:
                id_counter += 1
            elif element is None:
                chosen_square = {"row": i, "column": column}
                dia_squares.append(chosen_square)
        if id_counter == 1 and len(dia_squares) == 2:
            potential_squares.extend(dia_squares)
        else:
            chosen_square = None

        if len(potential_squares) > 0:
            chosen_square = potential_squares[random.randint(0, len(potential_squares) - 1)]
        return chosen_square
