import random


# TODO: Make check into nested methods in is_win()
# Output:
#   id of repeated element in a column or None if there is none
def vertical_check(field):
    for i in range(len(field[0])):
        counter = 0
        first_element = field[0][i]
        for j in range(len(field)):
            element = field[j][i]
            if first_element != element or element is None:
                break
            else:
                counter += 1
        if counter == len(field):
            return first_element
    return None


# Output:
#   id of repeated element in a row or None if there is none
def horizontal_check(field):
    for row in field:
        counter = 0
        first_element = row[0]
        for element in row:
            if element != first_element or element is None:
                break
            else:
                counter += 1
        if counter == len(row):
            return first_element
    return None


# Output:
#   id of repeated element in a diagonal line (from upper-left to bottom-right or upper-right to bottom-left)
#       or None if there is none
def diagonal_check(field):
    # Upper-left to bottom-right
    first_element = field[0][0]
    counter = 0
    for i in range(len(field)):
        element = field[i][i]
        if first_element != element or element is None:
            break
        else:
            counter += 1
    if counter == len(field):
        return first_element

    # Upper-right to bottom-left
    first_element = field[0][len(field) - 1]
    counter = 0
    for i in range(len(field)):
        element = field[i][len(field) - 1 - i]
        if first_element != element or element is None:
            break
        else:
            counter += 1
    if counter == len(field):
        return first_element
    return None


# Checks if a player has won
# Output:
#   id of repeated element in a row, column or diagonal line (see diagonal_check())
#       or None if there is none
def is_win(field):
    win_id = horizontal_check(field)
    if win_id is not None:
        return win_id

    win_id = vertical_check(field)
    if win_id is not None:
        return win_id

    return diagonal_check(field)


def field_is_filled(field):
    for row in field:
        if row.__contains__(None):
            return False
    return True


# Output:
#   Element from the list. Preferences is as follows:
#       Middle-element > Corner > Rest
#   If the list is empty, it returns None.
def tactical_element(squares):
    if len(squares) == 0:
        return None

    corner_squares = []
    for element in squares:
        row = element["row"]
        col = element["column"]
        if row == 0:
            if col != 1:
                corner_squares.append(element)
        elif row == 1:
            if col == 1:
                return element
        elif row == 2:
            if col != 1:
                corner_squares.append(element)

    return random.choice(corner_squares) if len(corner_squares) != 0 else random.choice(squares)


# Output:
#   Random element from the list.
#   If list is empty, it returns None
def random_element(a_list):
    if len(a_list) == 0:
        return None
    return random.choice(a_list)


# Output:
#   List of all elements in the field that are None
def available_squares(field):
    squares = []
    for i, row in enumerate(field):
        for j, element in enumerate(row):
            if element is None:
                squares.append({"row": i, "column": j})

    return squares


def fields_are_same(field1, field2):
    """
    Checks whether the field are exactly the same.
    """
    if len(field1) != len(field2):
        return False
    for i in range(len(field1)):
        if len(field1[i]) != len(field2[i]):
            return False
        for j in range(len(field1[i])):
            if field1[i][j] != field2[i][j]:
                return False
    return True


# TODO 1: IMPLEMENT THIS
def fields_are_similar(field1, field2):
    """
    Copying, rotating 4 times (also the mirrored version) one field and checking
    whether it is the same as the other field.
    :param field1: The first field.
    :param field2: The second field, which will be copied and this copy will be altered.
    :return: Whether the given field are the same, a rotation of one another, symmetric to each other,
    or that a rotation of one is symmetric to the other
    """
    field_copy = copy_field(field1)
    return True


def copy_field(original_field):
    """
    Copies the original field
    :param original_field:
    :return:
    """
    copied_field = [[], [], []]
    for i in range(len(original_field)):
        for j in range(len(original_field[i])):
            copied_field[i].append(original_field[i][j])
    return copied_field


# Parent class to the players
class Player:

    def __init__(self, init_id):
        self.field = None
        self.id = init_id
        return

    # Output:
    #   coordinates given in a dictionary, with keys "row" and "column"
    #   a random square in this class
    def choose_square(self, field):
        self.field = field
        return self.choose_random_square()

    # Finds a random available square and returns it
    def choose_random_square(self):
        return random.choice(available_squares(self.field))

    # Output:
    #   Random square with the same preference as tactical_element()
    def choose_semi_random_square(self):
        return tactical_element(available_squares(self.field))

    # Output:
    #   List of coordinates that would block a line of the opponent.
    def block_squares(self):
        return self.finish_squares(0 if self.id == 1 else 1)

    # Output:
    #   List of coordinates that can finish a line of the given id.
    def finish_squares(self, this_id):
        chosen_square = None
        finishing_squares = []

        # Checks the rows
        for i, row in enumerate(self.field):
            if row.count(this_id) == 2:
                for j in range(len(row)):
                    if row[j] is None:
                        finishing_squares.append({"row": i, "column": j})

        # Checks the columns
        for j in range(len(self.field[0])):
            id_counter = 0
            for i in range(len(self.field)):
                element = self.field[i][j]
                if element == this_id:
                    id_counter += 1
                elif element is None:
                    chosen_square = {"row": i, "column": j}
            if id_counter == 2 and chosen_square is not None:
                finishing_squares.append(chosen_square)
            else:
                chosen_square = None

        # Checks the diagonal line upper-left to bottom-right
        chosen_square = None
        id_counter = 0
        for i in range(len(self.field)):
            element = self.field[i][i]
            if element == this_id:
                id_counter += 1
            elif element is None:
                chosen_square = {"row": i, "column": i}
        if id_counter == 2 and chosen_square is not None:
            finishing_squares.append(chosen_square)

        # Checks the diagonal line upper-right to bottom-left
        chosen_square = None
        id_counter = 0
        for i in range(len(self.field)):
            column = len(self.field) - 1 - i
            element = self.field[i][column]
            if element == this_id:
                id_counter += 1
            elif element is None:
                chosen_square = {"row": i, "column": column}
        if id_counter == 2 and chosen_square is not None:
            finishing_squares.append(chosen_square)

        return finishing_squares

    # Output:
    #   List of coordinates that the enemy can use to start a line
    def block_start_line_squares(self):
        return self.start_line_squares(0 if self.id == 1 else 1)

    # Output:
    #   List of coordinates that would start a line of the given id, which could be finished the next turn
    def start_line_squares(self, this_id):
        potential_squares = []

        # Checks the rows
        for i, row in enumerate(self.field):
            if row.count(this_id) == 1 and row.count(None) == 2:
                for j in range(len(row)):
                    if row[j] is None:
                        potential_squares.append({"row": i, "column": j})

        # Checks the columns
        for j in range(len(self.field[0])):
            id_counter = 0
            column_squares = []
            for i in range(len(self.field)):
                element = self.field[i][j]
                if element == this_id:
                    id_counter += 1
                elif element is None:
                    column_squares.append({"row": i, "column": j})
            if id_counter == 1 and len(column_squares) == 2:
                potential_squares.extend(column_squares)

        # Checks the diagonal line upper-left to bottom-right
        id_counter = 0
        dia_squares = []
        for i in range(len(self.field)):
            element = self.field[i][i]
            if element == this_id:
                id_counter += 1
            elif element is None:
                dia_squares.append({"row": i, "column": i})
        if id_counter == 1 and len(dia_squares) == 2:
            potential_squares.extend(dia_squares)

        # Checks the diagonal line upper-right to bottom-left
        id_counter = 0
        dia_squares.clear()
        for i in range(len(self.field)):
            column = len(self.field) - 1 - i
            element = self.field[i][column]
            if element == this_id:
                id_counter += 1
            elif element is None:
                chosen_square = {"row": i, "column": column}
                dia_squares.append(chosen_square)
        if id_counter == 1 and len(dia_squares) == 2:
            potential_squares.extend(dia_squares)

        return potential_squares
