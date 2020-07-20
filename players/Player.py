import random


# Returns an element from the list. If the list is empty, it returns None
def random_element_from_list(given_list):
    if len(given_list) == 0:
        return None
    return random.choice(given_list)


# Parent class to the players
class Player:

    def __init__(self, id):
        self.field = None
        self.id = id
        return

    # Output:
    #   coordinates given in a dictionary, with keys "row" and "column"
    #   a random square in this class
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
    #   List of coordinates that would block a line of the opponent.
    def block_squares(self):
        return self.finish_squares(0 if self.id == 1 else 1)

    # Output:
    #   List of coordinates that can finish a line of the given id.
    def finish_squares(self, player_id):
        chosen_square = None
        finishing_squares = []

        # Checks the rows
        for i, row in enumerate(self.field):
            if row.count(player_id) == 2:
                for j in range(len(row)):
                    if row[j] is None:
                        finishing_squares.append({"row": i, "column": j})

        # Checks the columns
        for j in range(len(self.field[0])):
            id_counter = 0
            for i in range(len(self.field)):
                element = self.field[i][j]
                if element == player_id:
                    id_counter += 1
                elif element is None:
                    chosen_square = {"row": i, "column": j}
            if id_counter == 2 and chosen_square is not None:
                finishing_squares.append(chosen_square)
            else:
                chosen_square = None

        # Checks the diagonal line upper-left to bottom-right
        chosen_square = None
        id_counter = 0
        for i in range(len(self.field)):
            element = self.field[i][i]
            if element == player_id:
                id_counter += 1
            elif element is None:
                chosen_square = {"row": i, "column": i}
        if id_counter == 2 and chosen_square is not None:
            finishing_squares.append(chosen_square)

        # Checks the diagonal line upper-right to bottom-left
        chosen_square = None
        id_counter = 0
        for i in range(len(self.field)):
            column = len(self.field) - 1 - i
            element = self.field[i][column]
            if element == player_id:
                id_counter += 1
            elif element is None:
                chosen_square = {"row": i, "column": column}
        if id_counter == 2 and chosen_square is not None:
            finishing_squares.append(chosen_square)

        return finishing_squares

    # Output:
    #   List of coordinates that the enemy can use to start a line
    def block_start_line_squares(self):
        return self.start_line_squares(0 if self.id == 1 else 1)

    # Output:
    #   List of coordinates that would start a line of the given id, which could be finished the next turn
    def start_line_squares(self, player_id):
        potential_squares = []

        # Checks the rows
        for i, row in enumerate(self.field):
            if row.count(player_id) == 1 and row.count(None) == 2:
                for j in range(len(row)):
                    if row[j] is None:
                        potential_squares.append({"row": i, "column": j})

        # Checks the columns
        for j in range(len(self.field[0])):
            id_counter = 0
            column_squares = []
            for i in range(len(self.field)):
                element = self.field[i][j]
                if element == player_id:
                    id_counter += 1
                elif element is None:
                    column_squares.append({"row": i, "column": j})
            if id_counter == 1 and len(column_squares) == 2:
                potential_squares.extend(column_squares)

        # Checks the diagonal line upper-left to bottom-right
        id_counter = 0
        dia_squares = []
        for i in range(len(self.field)):
            element = self.field[i][i]
            if element == player_id:
                id_counter += 1
            elif element is None:
                dia_squares.append({"row": i, "column": i})
        if id_counter == 1 and len(dia_squares) == 2:
            potential_squares.extend(dia_squares)

        # Checks the diagonal line upper-right to bottom-left
        id_counter = 0
        dia_squares.clear()
        for i in range(len(self.field)):
            column = len(self.field) - 1 - i
            element = self.field[i][column]
            if element == player_id:
                id_counter += 1
            elif element is None:
                chosen_square = {"row": i, "column": column}
                dia_squares.append(chosen_square)
        if id_counter == 1 and len(dia_squares) == 2:
            potential_squares.extend(dia_squares)

        return potential_squares
