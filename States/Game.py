from States.Settings import Settings
from States.State import *

FIELD_BG_COLOUR = "#000000"

SQUARE_COLOUR = "#ffffff"


class Game(State):

    def __init__(self, root):
        super().__init__(root)
        game_frame = Frame(self.root, bg=BG_COLOUR)
        self.states["Game"] = game_frame
        game_frame.grid(row=0, column=0, sticky="nsew")

        create_button(Button(game_frame, command=self.clear_field), "Clear Field", 0, 0)
        create_button(Button(game_frame, command=self.update_players), "Update Players", 0, 1)
        player_name = "[PLAYER]"
        self.turnlabel = create_label(Label(game_frame), "It's " + player_name + "'s turn", row=1, columnspan=2)

        field_frame = Frame(game_frame, bg=FIELD_BG_COLOUR)
        self.field_labels = [[], [], []]
        self.field = [[], [], []]
        for i in range(len(self.field)):
            for j in range(len(self.field)):
                self.create_square(field_frame, i, j)
        field_frame.grid(row=2, column=0, columnspan=3)

        self.field_frame = field_frame
        self.game_frame = game_frame

    def create_square(self, parent, row, column):
        # Inspired by Tom in thread https://stackoverflow.com/questions/16363292/label-width-in-tkinter
        new_frame = Frame(parent, width=SQUARE_SIZE, height=SQUARE_SIZE)
        new_frame.pack_propagate(0)
        new_label = Label(new_frame, text=" ", bg=SQUARE_COLOUR)
        new_label.bind("<Button-1>", lambda e: self.square_clicked(row, column))
        self.field_labels[row].append(new_label)
        self.field[row].append(0)
        new_label.pack(fill=BOTH, expand=1)
        new_frame.grid(row=row, column=column, padx=SQUARE_DST / 2, pady=SQUARE_DST / 2)

    def square_clicked(self, x, y):
        # TODO: add check for player
        player_id = 0
        text = "I"
        if player_id == 1:
            text = "x"
        elif player_id == 2:
            text = "o"
        self.field_labels[x][y].configure(text=text)
        self.field[x][y] = player_id

    def clear_field(self):
        for i in range(len(self.field_labels)):
            for j in range(len(self.field_labels[i])):
                self.field_labels[i][j].configure(text=" ")
                self.field[i][j] = 0

    def update_players(self):
        next_frame = "Settings"
        if not next_frame in self.states.keys():
            Settings(self.root)
        self.show_frame(next_frame)
