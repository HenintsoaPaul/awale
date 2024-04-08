import tkinter as tk
from tkinter import messagebox

class GameGUI:
    def __init__(self, game):
        self.nb_turn = 0
        self.game = game
        self.window = tk.Tk()
        self.buttons = []
        self.labels = []  # Store the labels for each box
        self.current_turn = "player"  # Track the current turn

        # Boxes layout
        self.boxes_simple()
        # self.boxes_2_degree()

        # Add "Let AI move" button
        self.ai_move_button = tk.Button(self.window, text="Let AI move", command=self.on_ai_move_button_click, state=tk.DISABLED)
        self.ai_move_button.grid(row=2, column=0, columnspan=game._nb_boxes_per_side)

    def on_button_click(self, side, id_box):
        if self.current_turn == "player" and side == 1:  # Only allow player's move when it's their turn and on player's side
            box = self.game._player_boxes[id_box]
            if box.get_item() > 0:  # Check if the box contains more than 0 items
                self.game.move(side, id_box)
                print("player move => ", id_box)
                self.update_buttons()
                self.check_game_over()

                # Enable "Let AI move" button after player's move
                self.current_turn = "ai"
                self.ai_move_button.config(state=tk.NORMAL)

    def on_ai_move_button_click(self):
        if self.current_turn == "ai":
            AI_best_move = self.game.get_ai_move()
            self.game.move(side=0, id_box=AI_best_move)  # AI makes its move
            print("ai move => ", AI_best_move)
            self.update_buttons()
            self.check_game_over()

            self.current_turn = "player"  # Switch back to player's turn
            self.nb_turn += 1
            print("---")
            print("turn no: ", self.nb_turn)

            # Disable "Let AI move" button after AI's move
            self.ai_move_button.config(state=tk.DISABLED)

    def update_buttons(self):
        self.update_simple()
        # self.update_2_degree()
    
    def run(self):
        self.window.mainloop()

    def check_game_over(self):
        if self.game.is_game_over:
            winner = self.game.get_winner()
            messagebox.showinfo("Game Over", f"The winner is {winner}!")
            self.window.quit()

    # BOXES LAYOUTS
    # Simple
    def boxes_simple(self):
        for side in range(2):
            # Create a frame for each side (AI or player)
            frame = tk.Frame(self.window)
            frame.grid(row=side, column=0, columnspan=self.game._nb_boxes_per_side)

            # Add label for AI or player
            label_text = "AI" if side == 0 else "Player"
            label = tk.Label(frame, text=label_text)
            label.pack()

            row = []
            label_row = []  # Store the labels for each box in a row
            for id_box in range(self.game._nb_boxes_per_side):
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

    def update_simple(self):
        for side in range(2):
            for id_box in range(self.game._nb_boxes_per_side):
                box = self.game._ai_boxes[id_box] if side == 0 else self.game._player_boxes[id_box]
                self.buttons[side][id_box].config(text=str(box.get_item()), state=tk.DISABLED if side == 0 else tk.NORMAL)
                self.labels[side][id_box].config(text=str(id_box))  # Update the label with the box id

    # With degree
    def boxes_2_degree(self):
        for side in range(2):
            # Create a frame for each side (AI or player)
            side_frame = tk.Frame(self.window)
            side_frame.grid(row=side, column=0, columnspan=self.game._nb_boxes_per_side)

            # Add label for AI or player
            label_text = "AI" if side == 0 else "Player"
            label = tk.Label(side_frame, text=label_text)
            label.pack()

            for degree in range(2):
                # Create a frame for each degree (0 or 1)
                degree_frame = tk.Frame(side_frame)
                degree_frame.pack()

                row = []
                label_row = []  # Store the labels for each box in a row
                for id_box in range(self.game._nb_boxes_per_side):
                    # Only create a box if it has the correct degree
                    if (side == 0 and degree == id_box % 2) or (side == 1 and degree != id_box % 2):
                        # Create a frame for each box and its label
                        box_frame = tk.Frame(degree_frame)
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

    def update_2_degree(self):
        for side in range(2):
            for degree in range(2):
                for id_box in range(self.game._nb_boxes_per_side):
                    # Only update a box if it has the correct degree
                    if (side == 0 and degree == id_box % 2) or (side == 1 and degree != id_box % 2):
                        box = self.game.get_box(side, id_box)
                        item = box.get_item()
                        # Convert item to string only if it's not None
                        text = str(item) if item is not None else ''
                        self.buttons[side][degree][id_box].config(text=text, state=tk.DISABLED if side == 0 else tk.NORMAL)
                        self.labels[side][degree][id_box].config(text=str(id_box))  # Update the label with the box id