import tkinter as tk
from tkinter import messagebox

class NumberGridGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Grid Game")

        # Game variables
        self.grid_size = 10
        self.max_number = 100
        self.current_number = 1
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.labels = {}
        self.button_size = 25  # Each label will be 25x25 pixels to fit within 250x250

        # Initialize UI
        self.create_grid()
        self.create_controls()

        # Start game immediately
        self.start_game()

    def create_grid(self):
        frame = tk.Frame(self.root, width=250, height=250)
        frame.grid(row=0, column=0, padx=10, pady=10)

        # Set up a grid with each label precisely sized to fit within 250x250 pixels
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                lbl = tk.Label(
                    frame,
                    text="",
                    width=2,
                    height=1,
                    font=("Helvetica", 10, "bold"),
                    fg="red",
                    bg="white",
                    borderwidth=1,
                    relief="solid"
                )
                lbl.place(x=col * self.button_size, y=row * self.button_size, width=self.button_size, height=self.button_size)
                lbl.bind("<Button-1>", lambda e, r=row, c=col: self.place_number(r, c))
                self.labels[(row, col)] = lbl

    def create_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=1, column=0, pady=10)

        restart_button = tk.Button(control_frame, text="Restart", command=self.restart_game)
        restart_button.grid(row=0, column=0, padx=5)

    def start_game(self):
        # Reset game state
        self.current_number = 1
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Enable labels only on the four corners
        for (r, c), lbl in self.labels.items():
            if (r, c) in [(0, 0), (0, 9), (9, 0), (9, 9)]:
                lbl.config(text="", state="normal", fg="red")
                lbl.bind("<Button-1>", lambda e, r=r, c=c: self.place_number(r, c))
            else:
                lbl.config(text="", state="disabled", fg="red")
                lbl.unbind("<Button-1>")

    def restart_game(self):
        # Reset all labels and restart game
        for lbl in self.labels.values():
            lbl.config(text="", state="normal", fg="red")
        self.start_game()

    def place_number(self, row, col):
        if self.grid[row][col] is None and self.is_valid_move(row, col):
            self.grid[row][col] = self.current_number
            # Set the number and color explicitly
            self.labels[(row, col)].config(text=str(self.current_number), fg="red")

            if self.current_number == self.max_number:
                messagebox.showinfo("Congratulations!", "You've reached 100!")
                self.end_game()
            else:
                self.current_number += 1
                # Enable moves based on the next valid positions
                self.update_labels(row, col)

                # Check if player is stuck after placing a number
                if not self.has_valid_moves():
                    if 90 <= self.current_number <= 99:
                        messagebox.showinfo("Game Over", "Better luck next time!")
                    self.end_game()

    def is_valid_move(self, row, col):
        if self.current_number == 1:
            # First number can only be placed in one of the four corners
            return (row, col) in [(0, 0), (0, 9), (9, 0), (9, 9)]

        # Check 3-space vertical/horizontal or 2-space diagonal
        for r, c in [(row-3, col), (row+3, col), (row, col-3), (row, col+3),
                     (row-2, col-2), (row-2, col+2), (row+2, col-2), (row+2, col+2)]:
            if 0 <= r < self.grid_size and 0 <= c < self.grid_size:
                if self.grid[r][c] == self.current_number - 1:
                    return True
        return False

    def has_valid_moves(self):
        # Check all cells to see if there's a valid move for the current number
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.grid[row][col] is None and self.is_valid_move(row, col):
                    return True
        return False

    def update_labels(self, row, col):
        # Disable all labels initially
        for lbl in self.labels.values():
            lbl.config(state="disabled")

        # Enable labels based on valid moves
        for r, c in [(row-3, col), (row+3, col), (row, col-3), (row, col+3),
                     (row-2, col-2), (row-2, col+2), (row+2, col-2), (row+2, col+2)]:
            if 0 <= r < self.grid_size and 0 <= c < self.grid_size and self.grid[r][c] is None:
                self.labels[(r, c)].config(state="normal")
                self.labels[(r, c)].bind("<Button-1>", lambda e, r=r, c=c: self.place_number(r, c))

    def end_game(self):
        # Disable all labels at the end of the game
        for lbl in self.labels.values():
            lbl.config(state="disabled")

# Create the main application window
root = tk.Tk()
game = NumberGridGame(root)
root.mainloop()