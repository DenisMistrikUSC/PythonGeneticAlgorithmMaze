import tkinter as tk
import numpy as np
import geneticalgo as ga
import datanalysis
#define the ttinker gui for inputs into genetic algo
#setting to draw the best path in a current generation to display red 

MAZE_WIDTH = 500.0
MAZE_HEIGHT = 500.0
GOAL = np.array([450.0, 450.0])
START = np.array([50.0, 50.0])
WALLS = [
    np.array([np.array([100.0,100.0]), np.array([300.0,300.0])])
]

MAX_GENES = 200         
class GeneticGUI:
    def __init__(self, window):
        self.window = window
        window.title("Genetic Algorithm Simulator")

        #input fields
        row = 0
        tk.Label(window, text="Population:").grid(row=row, column=0, sticky="e")
        self.pop_entry = tk.Entry(window)
        self.pop_entry.insert(0, "20")
        self.pop_entry.grid(row=row, column=1)
        row += 1
        tk.Label(window, text="Cutoff:").grid(row=row, column=0, sticky="e")
        self.cutoff_entry = tk.Entry(window)
        self.cutoff_entry.insert(0, "0.2")
        self.cutoff_entry.grid(row=row, column=1)
        row += 1
        tk.Label(window, text="Mutation Rate:").grid(row=row, column=0, sticky="e")
        self.mutation_entry = tk.Entry(window)
        self.mutation_entry.insert(0, "0.3")
        self.mutation_entry.grid(row=row, column=1)
        row += 1
        tk.Label(window, text="Straggler Count:").grid(row=row, column=0, sticky="e")
        self.straggler_entry = tk.Entry(window)
        self.straggler_entry.insert(0, "1")
        self.straggler_entry.grid(row=row, column=1)
        row += 1
        tk.Label(window, text="Agent Speed:").grid(row=row, column=0, sticky="e")
        self.speed_entry = tk.Entry(window)
        self.speed_entry.insert(0, "150")
        self.speed_entry.grid(row=row, column=1)
        row += 1
        tk.Label(window, text="Turn Rate:").grid(row=row, column=0, sticky="e")
        self.turn_rate_entry = tk.Entry(window)
        self.turn_rate_entry.insert(0, "0.7")
        self.turn_rate_entry.grid(row=row, column=1)
        row += 1
        tk.Label(window, text="Genetic Sequence Length:").grid(row=row, column=0, sticky="e")
        self.sequence_length_entry = tk.Entry(window)
        self.sequence_length_entry.insert(0, "40")
        self.sequence_length_entry.grid(row=row, column=1)
        row += 1
        tk.Button(window, text="Start", command=self.start_button).grid(row=row, column=0, columnspan=2)
        row += 1
        self.gen_label = tk.Label(window, text="Generation: 0")
        self.gen_label.grid(row=row, column=0, columnspan=2)
        row += 1
        self.canvas = tk.Canvas(window, width=MAZE_WIDTH, height=MAZE_HEIGHT, bg="white")
        self.canvas.grid(row=row, column=0, columnspan=2)
        self.canvas.create_oval(
                        START[0] - 4, START[1] - 4, START[0] + 4, START[1] + 4,
                        fill="blue", tags="start"
                    )
        self.canvas.create_rectangle(GOAL[0], GOAL[1], MAZE_WIDTH, MAZE_HEIGHT, fill="red", tags="goal")
        self.draw_obstacles()

    def draw_obstacles(self):
        for obstacle in WALLS:
            self.canvas.create_rectangle(obstacle[0][0], obstacle[0][1], obstacle[1][0], obstacle[1][1], fill="gray", tags="maze")
    def start_button(self):
        self.window.after(0,self.start_sim)
    def start_sim(self):
        #stragglers cannot exceed the number of agents being cut
        parameters = ga.GeneticAlgoParameters(
            GENETIC_SEQUENCE_LENGTH=int(self.sequence_length_entry.get()),
            AGENT_SPEED=float(self.speed_entry.get()),
            MAZE_BOUNDS=np.array([[1.0, 1.0],[MAZE_WIDTH,MAZE_HEIGHT]]),
            TURN_RATE=float(self.turn_rate_entry.get()),
            MUTATION_RATE=np.clip(float(self.mutation_entry.get()), 0.0, 1.0),
            CUTOFF=np.clip(float(self.cutoff_entry.get()), 0.0, 1.0),
            NUM_AGENTS=int(self.pop_entry.get()),
            STRAGGLER_COUNT=np.clip(int(self.straggler_entry.get()), 0, int(int(self.pop_entry.get()) * (1 - float(self.cutoff_entry.get())))),
            START_POSITION=START,
            GOAL_POSITION=GOAL,
            OBSTACLES=WALLS
        )
        self.simulation = ga.GeneticSimulator(parameters=parameters,canvas=self.canvas, master=window, label_update=self.update_label, popup=self.open_graph_popup)      
        self.simulation.start_simulation()
    def update_label(self, gen_count):
        self.gen_label.config(text=f"Generation: {gen_count}")
    def open_graph_popup(self):
        popup = tk.Toplevel(self.window)
        data = datanalysis.DataAnalyzer(self.simulation.all_agents)
        popup.geometry ("350x250")
        popup.title("Data Analysis")
        tk.Button(popup, text="Show Generational Fitness", command=data.show_fitness_graph).grid(row=0, column=3, columnspan=2, sticky='ew')
        tk.Button(popup, text="Show Path Heatmap", command=data.show_heatmap).grid(row=2, column=3, columnspan=2, sticky='ew')
        tk.Button(popup, text="Show End Position Heatmap", command=lambda: data.show_bottleneck_graph(MAZE_HEIGHT, MAZE_WIDTH, 25)
        ).grid(row=4, column=3, columnspan=2, sticky='ew')
        for child in popup.winfo_children():
            child.grid_configure(padx=35, pady=25)


window = tk.Tk()
app = GeneticGUI(window)
window.mainloop()