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
    #show a heatmap like graph of where the final positions of each agent are
    def show_bottleneck_graph():
        pass

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

        