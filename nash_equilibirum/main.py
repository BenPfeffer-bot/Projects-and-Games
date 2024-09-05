import tkinter as tk
from game_system import GameSystem
from config import WINDOW_SIZE
import importlib
import players
importlib.reload(players)

def main():
    """
    Main function to start the Trade Game application.
    """
    # Create the main window
    root = tk.Tk()
    root.title("Trade Game Simulator")
    root.geometry(WINDOW_SIZE)

    # Create and start the game system
    game = GameSystem(root)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()