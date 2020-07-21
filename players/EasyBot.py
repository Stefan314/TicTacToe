from players.Player import *


class EasyBot(Player):

    def __init__(self, id):
        super().__init__(id)

    # Output:
    #   Square that would finish a line of its own;
    #   else a square that could possibly finish a line next turn;
    #   else a random square
    def choose_square(self, field):
        self.field = field
        chosen_square = None

        # Finish a line of its own
        finishing_squares = self.finish_squares(self.id)
        if chosen_square is None:
            chosen_square = tactical_element(finishing_squares)

        # Start a line
        starting_squares = self.start_line_squares(self.id)
        if chosen_square is None:
            chosen_square = tactical_element(starting_squares)

        # Random square
        if chosen_square is None:
            chosen_square = self.choose_random_square()
        return chosen_square
