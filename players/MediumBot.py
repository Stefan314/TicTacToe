from players.Player import Player


class MediumBot(Player):

    def __init__(self, id):
        super().__init__(id)

    # Output:
    #   Square that would finish a line of its own;
    #   else a square that would block its opponents line;
    #   else a random square
    def choose_square(self, field):
        self.field = field

        # Finish a line of its own
        chosen_square = self.finish_square(self.id)

        # Block a line of the opponent
        if chosen_square is None:
            chosen_square = self.block_square()

        if chosen_square is None:
            chosen_square = self.choose_random_square()
        return chosen_square
