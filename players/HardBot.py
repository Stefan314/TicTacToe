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

        # Checks the rows
        for i, row in enumerate(self.field):
            if row.count(self.id) == 1 and row.count(None) == 2:
                for j in range(len(row)):
                    if row[j] is None:
                        return {"row": i, "column": j}

        # Checks the columns
        for j in range(len(self.field[0])):
            id_counter = 0
            none_counter = 0
            for i in range(len(self.field)):
                element = self.field[i][j]
                if element == id:
                    id_counter += 1
                elif element is None:
                    none_counter += 1
                    chosen_square = {"row": i, "column": j}
            if id_counter == 1 and none_counter == 2:
                return chosen_square
            else:
                chosen_square = None

        # Checks the diagonal line upper-left to bottom-right
        id_counter = 0
        none_counter = 0
        for i in range(len(self.field)):
            element = self.field[i][i]
            if element == id:
                id_counter += 1
            elif element is None:
                none_counter += 1
                chosen_square = {"row": i, "column": i}
        if id_counter == 1 and none_counter == 2:
            return chosen_square
        else:
            chosen_square = None

        # Checks the diagonal line upper-right to bottom-left
        id_counter = 0
        none_counter = 0
        for i in range(len(self.field)):
            column = len(self.field) - 1 - i
            element = self.field[i][column]
            if element == id:
                id_counter += 1
            elif element is None:
                none_counter += 1
                chosen_square = {"row": i, "column": column}
        if id_counter == 1 and none_counter == 2:
            return chosen_square
        else:
            chosen_square = None

        return chosen_square