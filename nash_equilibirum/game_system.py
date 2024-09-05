import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from settings import Settings
import time

class GameSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Trade Game Visualization")
        self.master.geometry("1000x800")

        self.settings = Settings(population_size=100)
        self.is_running = False

        self.create_widgets()

    def create_widgets(self):
        # Create frames
        self.control_frame = ttk.Frame(self.master, padding="10")
        self.control_frame.pack(fill=tk.X)

        self.visual_frame = ttk.Frame(self.master, padding="10")
        self.visual_frame.pack(expand=True, fill=tk.BOTH)

        self.stats_frame = ttk.Frame(self.master, padding="10")
        self.stats_frame.pack(fill=tk.X)

        # Control widgets
        self.population_label = ttk.Label(self.control_frame, text="Population size:")
        self.population_label.pack(side=tk.LEFT)

        self.population_entry = ttk.Entry(self.control_frame, width=10)
        self.population_entry.insert(0, "100")
        self.population_entry.pack(side=tk.LEFT, padx=5)

        self.rounds_label = ttk.Label(self.control_frame, text="Number of rounds:")
        self.rounds_label.pack(side=tk.LEFT)

        self.rounds_entry = ttk.Entry(self.control_frame, width=10)
        self.rounds_entry.insert(0, "1000")
        self.rounds_entry.pack(side=tk.LEFT, padx=5)

        self.start_button = ttk.Button(self.control_frame, text="Start Game", command=self.start_game)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(self.control_frame, text="Stop Game", command=self.stop_game, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Visual widgets
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.visual_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

        # Statistics widgets
        self.stats_text = tk.Text(self.stats_frame, height=5, width=80)
        self.stats_text.pack(expand=True, fill=tk.BOTH)

    def start_game(self):
        population_size = int(self.population_entry.get())
        num_rounds = int(self.rounds_entry.get())
        
        self.settings = Settings(population_size=population_size)
        self.settings.initialize_population()
        
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        self.run_game(num_rounds)

    def stop_game(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def run_game(self, num_rounds):
        for round in range(num_rounds):
            if not self.is_running:
                break
            
            self.settings.run_game(1)
            results = self.settings.get_results()
            
            self.update_visuals(results)
            self.update_stats(results, round + 1)
            
            self.master.update()
            time.sleep(0.01)  # Small delay to make the visualization smoother
        
        self.stop_game()

    def update_visuals(self, results):
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()

        # Plot player distribution
        player_types = list(results.keys())
        counts = [results[pt]['count'] for pt in player_types]
        self.ax1.bar(player_types, counts)
        self.ax1.set_title("Player Type Distribution")
        self.ax1.set_ylabel("Number of Players")

        # Plot average scores
        avg_scores = [results[pt]['average_score'] for pt in player_types]
        self.ax2.bar(player_types, avg_scores)
        self.ax2.set_title("Average Scores by Player Type")
        self.ax2.set_ylabel("Average Score")

        self.canvas.draw()

    def update_stats(self, results, round_num):
        stats_text = f"Round: {round_num}\n"
        for player_type, data in results.items():
            stats_text += f"{player_type}: Count = {data['count']}, Avg Score = {data['average_score']:.2f}\n"
        
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert(tk.END, stats_text)

if __name__ == "__main__":
    root = tk.Tk()
    game_system = GameSystem(root)
    root.mainloop()