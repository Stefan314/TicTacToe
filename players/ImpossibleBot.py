from players.Player import *


class ImpossibleBot(Player):

    def __init__(self, id):
        super().__init__(id)

    '''
    # Output:
    #   Square that would finish a line of its own;
    #   else a square that blocks an opponents line, starts a line of its own
    #       and stops a line from starting from the enemy
    #   else a square that blocks an opponents line and start a line of its own;
    #   else a square that would block its opponents line;
    #   else a square that starts a line of its own, and stop a line from starting of the enemy;
    #   else a square that could possibly finish a line next turn;
    #   else a square that stops a line from starting of the enemy;
    #   else a random square.
    def choose_square(self, field):
        self.field = field
        chosen_square = None

        # Finish a line of its own
        finishing_squares = self.finish_squares(self.id)
        if chosen_square is None:
            chosen_square = tactical_element(finishing_squares)

        blocked_squares = self.block_squares()
        start_line_squares = self.start_line_squares(self.id)
        stop_line_squares = self.block_start_line_squares()

        # Lists that save the elements that are in common with the lists above
        block_start = []
        start_stop = []
        for start_square in start_line_squares:
            if start_square in blocked_squares:
                block_start.append(start_square)
                if start_square in stop_line_squares:
                    return start_square
            if start_square in stop_line_squares:
                start_stop.append(start_square)

        # Square that both blocks an opponents line and starts a line of its own
        if chosen_square is None:
            chosen_square = tactical_element(block_start)

        # Block a line of the opponent
        if chosen_square is None:
            chosen_square = tactical_element(blocked_squares)

        # Square that both starts a line of its own and stops a line from the opponent of starting
        if chosen_square is None:
            chosen_square = random_element(start_stop)

        # Start a line
        if chosen_square is None:
            chosen_square = tactical_element(start_line_squares)

        # Stops a line from starting of the enemy
        if chosen_square is None:
            chosen_square = tactical_element(stop_line_squares)

        return chosen_square if chosen_square is not None else self.choose_semi_random_square()'''
