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
