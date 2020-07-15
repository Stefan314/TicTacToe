from players.Player import Player


# Randomly chooses the squares
class RandomBot(Player):

    def __init__(self, id):
        super().__init__(id)

    def choose_square(self, field):
        self.field = field
        print(self.id)
        return self.choose_random_square()
