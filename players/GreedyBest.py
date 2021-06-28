import copy

from players.Player import *

LOSS, DRAW, WIN = -1, 0, 1


def dict_coord_to_tuple(dict_coord):
    return dict_coord["row"], dict_coord["column"]


def tuple_coord_to_dict(tuple_coord):
    return {"row": tuple_coord[0], "column": tuple_coord[1]}


# Output:
#   1 if id is 0 else 0
def next_id(id):
    return 1 if id == 0 else 0


# Copies the field and places a square
#   Output:
#       Returns the changed field
def place_square(field, id, square):
    copied_field = copy.deepcopy(field)
    copied_field[square["row"]][square["column"]] = id
    return copied_field


# Adds the value to the curr_square and returns it
def outcome(curr_square, value):
    curr_square["value"] = value
    return curr_square


class GreedyBest(Player):

    def __init__(self, init_id):
        super().__init__(init_id)

    def choose_square(self, field):
        return self.greedy(field, self.id)

    # TODO: get rid of symmetric copies
    # Output:
    #   Dictionary where the key is the coordinate and the value is the value of the coordinate between 0 and 1
    def greedy(self, field, id, square=None):
        end_value = self.end_value(field)
        if end_value is not None:
            square["value"] = end_value
            return square

        r_opts = self.rank_options(available_squares(field))
        bad_options = []
        while not r_opts:
            new_id = next_id(id)
            eval_opt = self.greedy(place_square(field, new_id, r_opts[0]), new_id, r_opts[0])

            if self.id == id:
                if eval_opt["value"] == WIN:
                    return eval_opt
            elif eval_opt["value"] == LOSS:
                return eval_opt
            bad_options.append(eval_opt)
            r_opts.remove()
        # TODO: check for all loss, and all win
        return self.rank_options(bad_options)[0]

    # Output:
    #   Outputs a value associated with the end-state, if the state is not the end, then it returns None
    #       if loss then it returns LOSS,
    #       if draw then it returns DRAW,
    #       if draw then it returns WIN,
    def end_value(self, field):
        end_id = is_win(field)
        if end_id is not None:
            return WIN if end_id == self.id else LOSS
        return DRAW if field_is_filled(field) else None

    # TODO: rank (finishing squares, block squares, start, stop)
    def rank_options(self, squares):
        return squares
