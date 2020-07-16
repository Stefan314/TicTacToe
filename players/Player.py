# Parent class for the players
import random


# Parent class to the players
class Player:

    def __init__(self, id):
        self.field = None
        self.id = id
        return

    # Output:
    #   coordinates given in a dictionary, with keys "row" and "column"
    #   a random square
    def choose_square(self, field):
        self.field = field
        return self.choose_random_square()

    # Finds a random available square and returns it
    def choose_random_square(self):
        converted_field = []
        for i, row in enumerate(self.field):
            for j, element in enumerate(row):
                if element is None:
                    converted_field.append((i, j))
        random_square = converted_field[random.randint(0, (len(converted_field) - 1))]
        coordinate = {"row": random_square[0], "column": random_square[1]}
        return coordinate

    # Output:
    #   Coordinate of square that would directly block a line of an opponent
    #       if that doesn't exist it outputs None
    def block_square(self):
        return self.finish_square(0 if self.id == 1 else 1)

    # Output:
    #   Coordinate of square that would directly finish a line of the given id
    #       if that doesn't exist it outputs None
    def finish_square(self, id):
        chosen_square = None

        # Checks the rows
        for i, row in enumerate(self.field):
            if row.count(id) == 2:
                for j in range(len(row)):
                    if row[j] is None:
                        return {"row": i, "column": j}

        # Checks the columns
        for j in range(len(self.field[0])):
            id_counter = 0
            for i in range(len(self.field)):
                element = self.field[i][j]
                if element == id:
                    id_counter += 1
                elif element is None:
                    chosen_square = {"row": i, "column": j}
            if id_counter == 2 and chosen_square is not None:
                return chosen_square
            else:
                chosen_square = None

        # Checks the diagonal line upper-left to bottom-right
        id_counter = 0
        for i in range(len(self.field)):
            element = self.field[i][i]
            if element == id:
                id_counter += 1
            elif element is None:
                chosen_square = {"row": i, "column": i}
        if id_counter == 2 and chosen_square is not None:
            return chosen_square
        else:
            chosen_square = None

        # Checks the diagonal line upper-right to bottom-left
        id_counter = 0
        for i in range(len(self.field)):
            column = len(self.field) - 1 - i
            element = self.field[i][column]
            if element == id:
                id_counter += 1
            elif element is None:
                chosen_square = {"row": i, "column": column}
        if id_counter == 2 and chosen_square is not None:
            return chosen_square
        else:
            chosen_square = None

        return chosen_square

    # Output:
    #   coordinates of the element that would start a line, which could be finished the next turn
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
