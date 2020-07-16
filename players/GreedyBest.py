from players.Player import Player


# Chooses a square that would either be a finishing move or a block
class GreedyBest(Player):

    def __init__(self, id):
        super().__init__(id)

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