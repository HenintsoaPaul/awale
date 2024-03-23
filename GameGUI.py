import tkinter as tk
from Game import Game

class GameGUI:
    def __init__(self, game):
        self.game = game
        self.window = tk.Tk()
        self.buttons = []
        self.current_turn = "player"  # Track the current turn

        for side in range(2):
            # Create a frame for each side (AI or player)
            frame = tk.Frame(self.window)
            frame.grid(row=side, column=0, columnspan=game._nb_boxes_per_side)

            # Add label for AI or player
            label_text = "AI" if side == 0 else "Player"
            label = tk.Label(frame, text=label_text)
            label.pack()

            row = []
            for id_box in range(game._nb_boxes_per_side):
                button = tk.Button(frame, command=lambda side=side, id_box=id_box: self.on_button_click(side, id_box))
                button.pack(side=tk.LEFT)
                row.append(button)
            self.buttons.append(row)

    def on_button_click(self, side, id_box):
        if self.current_turn == "player" and side == 1:  # Only allow player's move when it's their turn and on player's side
            self.game.move(side, id_box)
            self.update_buttons()
            self.current_turn = "ai"  # Switch to AI's turn
            self.game.move_ai()  # AI makes its move
            self.update_buttons()
            self.current_turn = "player"  # Switch back to player's turn

    def update_buttons(self):
        for side in range(2):
            for id_box in range(self.game._nb_boxes_per_side):
                box = self.game._ai_boxes[id_box] if side == 0 else self.game._player_boxes[id_box]
                self.buttons[side][id_box].config(text=str(box.get_item()), state=tk.DISABLED if side == 0 else tk.NORMAL)

    def run(self):
        self.window.mainloop()

game = Game()
game.init()
gui = GameGUI(game)
gui.run()