from players.Player import *


class HardBot(Player):

    def __init__(self, player_id):
        super().__init__(player_id)

    # Output:
    #   Square that would finish a line of its own;
    #   else a square that blocks an opponents line and start a line of its own;
    #   else a square that would block its opponents line;
    #   else a square that starts a line
    #   else a random square.
    def choose_square(self, field):
        self.field = field
        chosen_square = None

        # Finish a line of its own
        finishing_squares = self.finish_squares(self.id)
        if chosen_square is None:
            chosen_square = random_element_from_list(finishing_squares)

        blocked_squares = self.block_squares()
        start_line_squares = self.start_line_squares(self.id)

        # If there is overlap in the blocked squares and the square that would start a line, return this element
        for square in blocked_squares:
            if square in start_line_squares:
                return square

        # Block a line of the opponent
        if chosen_square is None:
            chosen_square = random_element_from_list(blocked_squares)

        # Start a line
        if chosen_square is None:
            chosen_square = random_element_from_list(start_line_squares)

        if chosen_square is None:
            chosen_square = self.choose_random_square()
        return chosen_square
