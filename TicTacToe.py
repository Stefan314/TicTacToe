import random

from States.State import *
from players.EasyBot import EasyBot
from players.ExtremeBot import ExtremeBot
from players.GreedyBest import GreedyBest
from players.HardBot import HardBot
from players.RandomBot import RandomBot
from players.MediumBot import MediumBot

HIGHLIGHT_COLOUR = "#f4ffb0"
PLAYERS = {0: "x", 1: "o"}

DEFAULT_FONT = "consolas 12"
DEFAULT_FONT_COLOUR = "#001670"

WINDOW_COORD = "+600+100"


def player_factory(player_type_name, player_id):
    if player_type_name == PLAYER_TYPES[HUMAN]:
        return None
    elif player_type_name == PLAYER_TYPES[RANDOM]:
        return RandomBot(player_id)
    elif player_type_name == PLAYER_TYPES[EASY]:
        return EasyBot(player_id)
    elif player_type_name == PLAYER_TYPES[MEDIUM]:
        return MediumBot(player_id)
    elif player_type_name == PLAYER_TYPES[HARD]:
        return HardBot(player_id)
    elif player_type_name == PLAYER_TYPES[EXTREME]:
        return ExtremeBot(player_id)
    elif player_type_name == PLAYER_TYPES[GREEDY]:
        return GreedyBest(player_id)


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


# Main class of the game
def player_is_human(player):
    human_player = PLAYER_TYPES[HUMAN]
    return True if player["player_type"].get() == human_player else False


class TicTacToe:

    # Sets up the root and some fields and launches the State class
    def __init__(self):
        self.players = {}
        self.end = False
        self.current_player_id = None
        self.current_coord = {}

        root = Tk()
        root.option_add("*font", DEFAULT_FONT)
        root.option_add("*foreground", DEFAULT_FONT_COLOUR)

        # Default root attributes
        width = (SQUARE_SIZE + SQUARE_DST) * 3
        height = width + 2 * SQUARE_SIZE

        root.configure(bg=BG_COLOUR)
        root.geometry(str(width) + "x" + str(height) + WINDOW_COORD)
        root.title("TicTacToe")
        root.iconbitmap("Images/game_icon.ico")
        root.bind("<Key>", self.key_listener)

        self.state = State(root, "Settings")

        settings_state = self.state.states[STATES[SETTINGS]]
        settings_state.start_button.configure(command=self.start_game)

        root.mainloop()

    # Main key_listener bound to the root
    # Escape: exits the program
    # If the current state is the settings-state then the following applies for the key-presses:
    #   Enter: starts the game
    # If the current state is the game-state then the following applies for the key-presses:
    #   Enter: selects the highlighted square
    #   Arrow-keys: moves the highlighted square
    #   r: resets the field
    #   u: lets the user alter the names and the player-kind
    def key_listener(self, event):
        if event.keysym == 'Escape':
            sys.exit()

        if self.state.current_state == STATES[SETTINGS]:
            if event.keysym == 'Return':
                self.start_game()

        elif self.state.current_state == STATES[GAME]:
            x = self.current_coord["x"]
            y = self.current_coord["y"]
            current_label = self.state.states[STATES[GAME]].field_labels[y][x]

            # Move the highlighted square
            if event.keysym == 'Up':
                if y > 0:
                    self.current_coord["y"] -= 1
                self.highlight_square(current_label)
            if event.keysym == 'Right':
                if x < 2:
                    self.current_coord["x"] += 1
                self.highlight_square(current_label)
            if event.keysym == 'Down':
                if y < 2:
                    self.current_coord["y"] += 1
                self.highlight_square(current_label)
            if event.keysym == 'Left':
                if x > 0:
                    self.current_coord["x"] -= 1
                self.highlight_square(current_label)

            # Resets the game
            if event.keysym == 'r':
                self.clear_field()

            # Goes back to the settings menu to alter values there
            if event.keysym == 'u':
                self.state.update_state(STATES[SETTINGS])

            if player_is_human(self.state.players[self.current_player_id]):
                # Select the highlighted square
                if event.keysym == 'Return':
                    self.square_selected()

    # Launches and displays the game state
    def start_game(self):
        # Checks if the game state has already been altered accordingly before
        first_time = False
        if not self.state.states.keys().__contains__(STATES[GAME]):
            first_time = True

        self.state.start_game()
        # Edits the game state by adding appropriate commands
        if first_time:
            game_state = self.state.states[STATES[GAME]]
            game_state.reset_button.configure(command=self.clear_field)
            for i, field_row in enumerate(game_state.field_labels):
                for j, element in enumerate(field_row):
                    # Because of the scopes of the variables in the loops,
                    #   it is required to create an extra function
                    def command(row, column):
                        return lambda e: self.square_selected(row=row, column=column)

                    element.bind("<Button-1>", command(i, j))
                    # self.add_command(game_state.field_labels[i][j], j, i)

        # Start off with default coordinate which is right in the middle
        self.current_coord["x"] = 1
        self.current_coord["y"] = 1

        # Adding player classes
        state_players = self.state.players
        for i, player in enumerate(state_players):
            self.players[i] = player_factory(player["player_type"].get(), i)

        self.state.states[STATES[GAME]].reset_results()
        self.clear_field()

    # Alters the screen and the field accordingly, also checks whether a player has won
    def square_selected(self, row=None, column=None):
        column = self.current_coord["x"] if column is None else column
        row = self.current_coord["y"] if row is None else row

        prev_label = self.state.states[STATES[GAME]].field_labels[self.current_coord["y"]][self.current_coord["x"]]
        # Update the current square
        self.current_coord["x"] = column
        self.current_coord["y"] = row

        game_state = self.state.states[STATES[GAME]]
        field = game_state.field
        # Can only alter the field if there is nothing in it and the game is not won
        if field[row][column] is None and not self.end:
            self.highlight_square(prev_label)
            field[row][column] = self.current_player_id
            game_state.field_labels[row][column].configure(text=PLAYERS[self.current_player_id])
            win_id = self.is_win()

            if win_id is not None:
                self.set_end(self.state.players[self.current_player_id]["name"])
            elif self.field_is_filled():
                self.set_end()
            else:
                self.next_player()

    # Checks if a player has won
    # Output:
    #   id of repeated element in a row, column or diagonal line (see diagonal_check())
    #       or None if there is none
    def is_win(self):
        field = self.state.states[STATES[GAME]].field

        win_id = horizontal_check(field)
        if win_id is not None:
            return win_id

        win_id = vertical_check(field)
        if win_id is not None:
            return win_id

        win_id = diagonal_check(field)
        if win_id is not None:
            return win_id

        return win_id

    # Puts a label on the screen, saying that the player has won
    # Inputs:
    #   player_name as a string, if it's not given then it's recorded as a tie
    def set_end(self, player_name=None):
        self.end = True
        end_text = "The field is filled and the result is a tie"
        player_id = 2
        if player_name is not None:
            end_text = "Congratulations, " + player_name + ", you have won"
            player_id = self.current_player_id
        self.state.states[STATES[GAME]].add_win(player_id)
        game_state = self.state.states[STATES[GAME]]
        game_state.win_label.configure(text=end_text)
        game_state.win_frame.grid(row=4, column=0, columnspan=3)

    def field_is_filled(self):
        for row in self.state.states[STATES[GAME]].field:
            if row.__contains__(None):
                return False
        return True

    # Clears the field, the squares, the label that said a player has won and calls update_players()
    def clear_field(self):
        game_state = self.state.states[STATES[GAME]]
        game_state.clear_field()
        game_state.win_frame.grid_forget()
        self.update_players()

    # Makes sure that a random starting player is selected
    def update_players(self):
        self.end = False
        self.current_player_id = random.randint(0, 1)
        self.next_player()

    def next_player(self):
        self.current_player_id = 0 if self.current_player_id == 1 else 1
        current_player = self.state.players[self.current_player_id]
        self.state.update_turnlabel(current_player["name"], PLAYERS[self.current_player_id])
        current_label = self.state.states[STATES[GAME]].field_labels[self.current_coord["y"]][self.current_coord["x"]]
        self.highlight_square(current_label)
        if not player_is_human(current_player):
            player = self.players[self.current_player_id]
            coordinates = player.choose_square(self.state.states[STATES[GAME]].field)
            row = coordinates["row"]
            column = coordinates["column"]
            self.square_selected(row=row, column=column)
            return

    def highlight_square(self, prev_label):
        prev_label.configure(bg=SQUARE_COLOUR)
        x = self.current_coord["x"]
        y = self.current_coord["y"]
        if player_is_human(self.state.players[self.current_player_id]):
            self.state.states[STATES[GAME]].field_labels[y][x].configure(bg=HIGHLIGHT_COLOUR)


def launch(): TicTacToe()


launch()
