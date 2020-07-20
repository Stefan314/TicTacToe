from players.Player import *


class MediumBot(Player):

    def __init__(self, player_id):
        super().__init__(player_id)

    # Output:
    #   Square that would finish a line of its own;
    #   else a square that would block its opponents line;
    #   else a random square
    def choose_square(self, field):
        self.field = field
        chosen_square = None

        # Finish a line of its own
        finishing_squares = self.finish_squares(self.id)
        if chosen_square is None:
            chosen_square = random_element_from_list(finishing_squares)

        # Block a line of the opponent
        blocking_squares = self.start_line_squares(self.id)
        if chosen_square is None:
            chosen_square = random_element_from_list(blocking_squares)

        # Random square
        if chosen_square is None:
            chosen_square = self.choose_random_square()
        return chosen_square
