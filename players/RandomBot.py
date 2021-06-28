from players.Player import Player


class RandomBot(Player):

    def __init__(self, init_id):
        super().__init__(init_id)

    # Output:
    #   A random square
    def choose_square(self, field):
        self.field = field
        return self.choose_random_square()
