from tkinter import *

SQUARE_SIZE = 100
SQUARE_DST = 10
SQUARE_COLOUR = "#ffffff"

BG_COLOUR = "#e05e00"
FIELD_BG_COLOUR = "#000000"

WIN_FONT = ("consolas", 9)

WIDGET_PADDING = 5

PLAYER_TYPES = ["Human", "RandomBot", "SimpleBot"]
HUMAN, RANDOM, SIMPLE = 0, 1, 2

STATES = ["Settings", "Game"]
SETTINGS, GAME = 0, 1


# Requirements:
#   The widget must have an assigned parent;
#   The widget can only be a label;
#   The widget must also be assigned in a grid environment.
def create_label(widget, text, row=0, column=0, columnspan=1, padx=WIDGET_PADDING):
    widget.configure(text=text, bg=BG_COLOUR)
    widget.grid(row=row, column=column, columnspan=columnspan, padx=padx)
    return widget


# Requirements:
#   The widget must have an assigned parent and command;
#   The widget can only be a button;
#   The widget must also be assigned in a grid environment.
def create_button(widget, text, row, column, columnspan=1, padx=WIDGET_PADDING, pady=WIDGET_PADDING):
    widget.configure(text=text)
    widget.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)
    return widget


# Requirements:
#   The widget must have an assigned parent;
#   The widget can only be an entry;
#   The widget must also be assigned in a grid environment.
def create_entry(widget, row=0, column=1, columnspan=1):
    widget.grid(row=row, column=column, columnspan=columnspan)
    return widget


# Requirements:
#   The widget must have an assigned parent, variable and options;
#   The widget can only be an OptionMenu;
#   The widget must also be assigned in a grid environment.
def create_dropdown(widget, row=0, column=1, columnspan=1):
    widget.grid(row=row, column=column, columnspan=columnspan)
    return


# Creates the requested state, if it doesn't exist it throws an exception
# Requirements:
#   state must be given as a string
def state_factory(state, root):
    if state == STATES[SETTINGS]:
        return Settings(root)
    elif state == STATES[GAME]:
        return Game(root)
    else:
        raise Exception("Wrong name")


class State:

    def __init__(self, root, state):
        self.states = {}
        self.players = []
        self.current_state = STATES[SETTINGS]
        self.root = root

        settings_state = state_factory(state, root)
        self.states[STATES[SETTINGS]] = settings_state

    # Puts the correct frame on top.
    # Requirements:
    #   frame_key must be a key of frames
    def show_frame(self, frame_key):
        self.states[frame_key].main_frame.tkraise()
        return

    # Makes sure that the names are stored and that the game starts.
    def start_game(self):
        current_state = self.states[STATES[SETTINGS]]
        player1_entry = current_state.player1_name_entry.get()
        player2_entry = current_state.player2_name_entry.get()
        player1_name = "Player 1" if not player1_entry else player1_entry
        player2_name = "Player 2" if not player2_entry else player2_entry
        if not self.players:
            self.players.extend([{"name": player1_name, "player_type": current_state.player1},
                                {"name": player2_name, "player_type": current_state.player2}])
        self.update_state(STATES[GAME])

    # Makes sure that the requested stated will be the new one.
    # If the requested state already exists it will update to that one.
    # Requirements:
    #   state_name must be in state_factory
    def update_state(self, state_name):
        if not self.states.keys().__contains__(state_name):
            new_state = state_factory(state_name, self.root)
            self.states[state_name] = new_state
            if state_name == STATES[GAME]:
                new_state.update_button.configure(command=lambda: self.update_state(STATES[SETTINGS]))
        self.current_state = state_name
        self.show_frame(state_name)

    # Inputs:
    #   player_id: x or o, depending on who's playing
    # Updates the label that says who's turn it is to the requested player's name
    def update_turnlabel(self, player_name, player_id):
        self.states[STATES[GAME]].turnlabel.configure(text=("It's " + player_name + "'s turn. (" + player_id + ")"))


class Game:

    # Creates the main frame of the game state with all widgets
    def __init__(self, root):
        game_frame = Frame(root, bg=BG_COLOUR)
        game_frame.grid(row=0, column=0, sticky="nsew")

        self.reset_button = create_button(Button(game_frame), "Reset Game", 0, 0)
        self.update_button = create_button(Button(game_frame), "Update Players", 0, 1)
        player_name = "[PLAYER]"
        self.turnlabel = create_label(Label(game_frame), "It's " + player_name + "'s turn", row=1, columnspan=2)

        field_frame = Frame(game_frame, bg=FIELD_BG_COLOUR)
        self.field_labels = [[], [], []]
        self.field = [[], [], []]
        for i in range(len(self.field)):
            for j in range(len(self.field)):
                self.create_square(field_frame, i, j)
        field_frame.grid(row=2, column=0, columnspan=3)

        win_frame = Frame(game_frame, bg=BG_COLOUR)
        win_text = ""
        info_text = "Press r to reset the game"
        self.win_label = create_label(Label(win_frame, font=WIN_FONT), win_text, row=0, columnspan=3)
        create_label(Label(win_frame, font=WIN_FONT), info_text, row=1, columnspan=3)

        self.win_frame = win_frame
        self.field_frame = field_frame
        self.main_frame = game_frame

    # Creates one square of the field
    # Inputs:
    #   parent = master widget of the requested square
    def create_square(self, parent, row, column):
        # Inspired by Tom in thread https://stackoverflow.com/questions/16363292/label-width-in-tkinter
        new_frame = Frame(parent, width=SQUARE_SIZE, height=SQUARE_SIZE)
        new_frame.pack_propagate(0)
        new_label = Label(new_frame, text=" ", bg=SQUARE_COLOUR)
        self.field_labels[row].append(new_label)
        self.field[row].append(None)
        new_label.pack(fill=BOTH, expand=1)
        new_frame.grid(row=row, column=column, padx=SQUARE_DST / 2, pady=SQUARE_DST / 2)

    # Sets all field elements to -1, and empties all field labels and makes them white
    def clear_field(self):
        for i in range(len(self.field_labels)):
            for j in range(len(self.field_labels[i])):
                self.field_labels[i][j].configure(text=" ", bg=SQUARE_COLOUR)
                self.field[i][j] = None


class Settings:

    # Creates the main frame of the settings state with all widgets
    def __init__(self, root):
        settings_frame = Frame(root, bg=BG_COLOUR)
        settings_frame.grid(row=0, column=0, sticky="nsew")

        player1_dropdown_frame = Frame(settings_frame, bg=BG_COLOUR)
        player1_entry_frame = Frame(settings_frame, bg=BG_COLOUR)
        player2_dropdown_frame = Frame(settings_frame, bg=BG_COLOUR)
        player2_entry_frame = Frame(settings_frame, bg=BG_COLOUR)

        create_label(Label(settings_frame), "Enter the info for the players", columnspan=2)
        create_label(Label(player1_dropdown_frame), "Player 1", padx=WIDGET_PADDING * 4)
        create_label(Label(player1_entry_frame), "Name player 1:")
        create_label(Label(player2_dropdown_frame), "Player 2", padx=WIDGET_PADDING * 4)
        create_label(Label(player2_entry_frame), "Name player 2:")

        player1 = StringVar()
        player1.set(PLAYER_TYPES[0])
        create_dropdown(OptionMenu(player1_dropdown_frame, player1, *PLAYER_TYPES))
        self.player1 = player1

        player2 = StringVar()
        player2.set(PLAYER_TYPES[0])
        create_dropdown(OptionMenu(player2_dropdown_frame, player2, *PLAYER_TYPES))
        self.player2 = player2

        self.player1_name_entry = create_entry(Entry(player1_entry_frame))
        self.player2_name_entry = create_entry(Entry(player2_entry_frame))

        self.start_button = create_button(Button(settings_frame), "Go!",
                                          5, 0, 2, pady=WIDGET_PADDING * 2)

        # Putting the frames in the main_frame
        player1_dropdown_frame.grid(row=1, pady=(WIDGET_PADDING * 4, WIDGET_PADDING))
        player1_entry_frame.grid(row=2)
        player2_dropdown_frame.grid(row=3, pady=(WIDGET_PADDING * 4, WIDGET_PADDING))
        player2_entry_frame.grid(row=4)

        self.main_frame = settings_frame
