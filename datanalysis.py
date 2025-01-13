#anaylyze the path data/final position data and plot it with matplot lib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import geneticagent as ga

class DataAnalyzer:
    def __init__(self, agent_list):
        self.agent_list : list [ga.GeneticAgent] = agent_list

    def format_data():
        pass
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
        heatmap, 
        cmap='plasma',
        origin='upper',
        extent=[0, width, 0, height]
        )
        plt.colorbar(label='Frequency')
        plt.title('Frequency Heatmap of 2D Positions')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.show()



    #heatmap of all paths taken
    def show_heatmap():
        pass

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

        