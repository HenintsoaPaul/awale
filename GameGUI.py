import tkinter as tk
from Box import Box
from Game import Game

class GameGUI:
    def __init__(self, game):
        self.game = game
        self.window = tk.Tk()
        self.buttons = []

        for side in range(2):
            row = []
            for id_box in range(game._nb_boxes_per_side):
                button = tk.Button(self.window, command=lambda side=side, id_box=id_box: self.on_button_click(side, id_box))
                button.grid(row=side, column=id_box)
                row.append(button)
            self.buttons.append(row)

    def on_button_click(self, side, id_box):
        self.game.move(side, id_box)
        self.update_buttons()

    def update_buttons(self):
        for side in range(2):
            for id_box in range(self.game._nb_boxes_per_side):
                box = self.game._ai_boxes[id_box] if side == 0 else self.game._player_boxes[id_box]
                self.buttons[side][id_box].config(text=str(box.get_item()))

    def run(self):
        self.window.mainloop()

game = Game()
game.init()
gui = GameGUI(game)
gui.run()