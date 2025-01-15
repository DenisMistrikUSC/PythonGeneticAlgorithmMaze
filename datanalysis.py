#anaylyze the path data/final position data and plot it with matplot lib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geneticagent as ga
from scipy.stats import gaussian_kde

class DataAnalyzer:
    def __init__(self, agent_list):
        self.agent_list : list [ga.GeneticAgent] = agent_list

    #show a 2d histogram like graph of where the final positions of each agent are
    def show_bottleneck_graph(self, height, width, bins):
        final_positions = np.array([agent.final_position for agent in self.agent_list])
        x_coords = final_positions[:, 0]
        y_coords = final_positions[:, 1]
        if len(x_coords) != len(y_coords):
            raise ValueError('x and y must have the same length.')

        heatmap, xedges, yedges = np.histogram2d(
            x_coords, y_coords,
            bins=bins,
            range=[[0, width], [0, height]]
        )
        plt.imshow(
        heatmap.T, 
        cmap='plasma',
        origin='lower',
        extent=[0, width, 0, height]
        )
        plt.gca().invert_yaxis()
        plt.colorbar(label='Frequency')
        plt.title('Frequency Heatmap of 2D Positions')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.show()



    #heatmap of all paths taken using kde
    def show_heatmap(self):
        all_paths = [agent.path for agent in self.agent_list]
        flattened_positions = np.array([pos for subarray in all_paths for pos in subarray])
        x_coords = flattened_positions[:, 0]
        y_coords = flattened_positions[:, 1]
        xy = np.vstack([x_coords, y_coords])
        kde = gaussian_kde(xy)
        x_min, x_max = x_coords.min(), x_coords.max()
        y_min, y_max = y_coords.min(), y_coords.max()
        x_grid, y_grid = np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100)
        X, Y = np.meshgrid(x_grid, y_grid)
        Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)
        plt.contourf(X, Y, Z, levels=50, cmap='viridis', origin='upper')
        plt.gca().invert_yaxis() 
        plt.colorbar(label='Density')
        plt.title("Heatmap of all paths taken")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()



    #simple line graph of the average fitness per generation
    def show_fitness_graph(self):
        df = pd.DataFrame(columns=["Generation", "Average Fitness"])
        curr_generation = 1
        generation_agent_count = 0
        generation_total_fitness = 0
        #iterate through all agents list, get fitness and average it
        for agent in self.agent_list:
            if agent.generation != curr_generation: 
                df = pd.concat([df, pd.DataFrame({"Generation": [curr_generation], "Average Fitness": [generation_total_fitness / generation_agent_count]})], ignore_index=True)
                curr_generation += 1
                generation_agent_count = 0
                generation_total_fitness = 0
            generation_agent_count += 1
            generation_total_fitness += agent.fitness
        df = pd.concat([df, pd.DataFrame({"Generation": [curr_generation], "Average Fitness": [generation_total_fitness / generation_agent_count]})], ignore_index=True)
        plt.plot(df["Generation"], df["Average Fitness"]) 
        plt.show() 

        