from players.Player import Player


class EasyBot(Player):

    def __init__(self, player_id):
        super().__init__(player_id)

    # Output:
    #   Square that would finish a line of its own;
    #   else a square that would block its opponents line;
    #   else a square that could possibly finish a line next turn;
    #   else a random square
    def choose_square(self, field):
        self.field = field

        # Finish a line of its own
        chosen_square = self.finish_square(self.id)

        # Start a line
        if chosen_square is None:
            chosen_square = self.start_line_square()

        if chosen_square is None:
            chosen_square = self.choose_random_square()
        return chosen_square
