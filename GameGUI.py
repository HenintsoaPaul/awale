import tkinter as tk
from tkinter import messagebox
from Game import Game

class GameGUI:
    def __init__(self, game):
        self.nb_turn = 0
        self.game = game
        self.window = tk.Tk()
        self.buttons = []
        self.labels = []  # Store the labels for each box
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
            label_row = []  # Store the labels for each box in a row
            for id_box in range(game._nb_boxes_per_side):
                # Create a frame for each box and its label
                box_frame = tk.Frame(frame)
                box_frame.pack(side=tk.LEFT)

                # Add label for box id
                box_label = tk.Label(box_frame, text=str(id_box))
                box_label.pack()

                # Create button for each box
                button = tk.Button(box_frame, command=lambda side=side, id_box=id_box: self.on_button_click(side, id_box))
                button.pack()

                row.append(button)
                label_row.append(box_label)

            self.buttons.append(row)
            self.labels.append(label_row)

    def on_button_click(self, side, id_box):
        if self.current_turn == "player" and side == 1:  # Only allow player's move when it's their turn and on player's side
            box = self.game._player_boxes[id_box]
            if box.get_item() > 0:  # Check if the box contains more than 0 items
                self.game.move(side, id_box)
                print("player move => ", id_box)
                self.update_buttons()

                self.current_turn = "ai"  # Switch to AI's turn
                self.game.move_ai()  # AI makes its move
                print("ai move => ", id_box)
                self.update_buttons()

                self.current_turn = "player"  # Switch back to player's turn
                self.nb_turn += 1
                print("---")
                print("turn no: ", self.nb_turn)

    def update_buttons(self):
        for side in range(2):
            for id_box in range(self.game._nb_boxes_per_side):
                box = self.game._ai_boxes[id_box] if side == 0 else self.game._player_boxes[id_box]
                self.buttons[side][id_box].config(text=str(box.get_item()), state=tk.DISABLED if side == 0 else tk.NORMAL)
                self.labels[side][id_box].config(text=str(id_box))  # Update the label with the box id

                # Adjust the order of the boxes based on the box order
                if box.get_degree() == 1:
                    self.buttons[side][id_box].lower()  # Move the box behind other boxes
                else:
                    self.buttons[side][id_box].lift()  # Move the box in front of other boxes

    def run(self):
        self.check_game_over()
        self.window.mainloop()

    def check_game_over(self):
        if self.game.check_game_over():
            winner = self.game.get_winner()
            messagebox.showinfo("Game Over", f"The winner is {winner}!")
            self.window.quit()

game = Game()
game.init()
gui = GameGUI(game)
gui.run()
