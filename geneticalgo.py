#define the game loop and run it
#run the simulations
#parameters here 
#number of agents 
#population cutoff
#number of stragglers (say for genetic diversity you maintain a random "straggler" agent that would not have met the cutoff)
import geneticagent as ag
import numpy as np
import random
import tkinter as tk
import time
from dataclasses import dataclass, field

@dataclass
class GeneticAlgoParameters:
    GENETIC_SEQUENCE_LENGTH : int = 200
    AGENT_SPEED : float = 10
    MAZE_SIZE : np.ndarray = field(default_factory=lambda: np.array([500.0,500.0]))
    MAZE_BOUNDS: np.ndarray = field(default_factory=lambda:np.array([[0, 0],[500.0,500.0]]))
    TURN_RATE : float = 0.5
    MUTATION_RATE : float = 0.2
    CUTOFF : float = 0.3
    NUM_AGENTS : int = 20
    STRAGGLER_COUNT : int = 0
    START_POSITION : np.ndarray = field(default_factory=lambda:np.array([25.0,25.0]))
    GOAL_POSITION : np.ndarray = field(default_factory=lambda:np.array([400.0,400.0]))
    OBSTACLES: list[tuple] = field(default_factory=lambda:[]) #list because this can change with user input later down the line will be a list of tuples

class GeneticSimulator:
    def __init__(self, parameters : GeneticAlgoParameters, canvas : tk.Canvas, master : tk.Tk):
        self.params = parameters
        self.canvas = canvas
        self.population : list[ag.GeneticAgent] = [] # storage of the current population of agents
        self.end_history = [] #list of every single past agents final position, i.e where it collided 
        self.generation_count = 0
        self.is_running = False
        self.agents_finished = 0
        self.master = master
        

    def collision_check(self, agent : ag.GeneticAgent) -> None:
        #check for collisions, if any found then set has_collided and final position 
        #check maze bounds collision
        has_collided = not np.all((self.params.MAZE_BOUNDS[0] < agent.position) & (agent.position < self.params.MAZE_BOUNDS[1]))
        #check obstacle collision
        #principles of AABB collision
        if not has_collided:
            for obstacle in self.params.OBSTACLES:
                top_left, bottom_right = obstacle
                if np.all((top_left <= agent.position) & (agent.position <= bottom_right)):
                    has_collided = True
                    break
        
        if has_collided:
            agent.has_collided = True
            agent.final_position = agent.position
            self.agents_finished += 1
            self.end_history.append(agent.position)

    def goal_check(self,agent) -> None:
        if np.all((self.params.GOAL_POSITION <= agent.position)):
            self.is_running = False
            

    def crossover(self, parent1, parent2) -> ag.GeneticAgent:
        child = ag.GeneticAgent(self.params.GENETIC_SEQUENCE_LENGTH, self.params.AGENT_SPEED, self.params.START_POSITION, self.params.TURN_RATE)
        for i in range(self.params.GENETIC_SEQUENCE_LENGTH):
            if random.random() < 0.5:
                child.genes[i] = parent1.genes[i]
            else:
                child.genes[i] = parent2.genes[i]
        return child

    def run_generation(self) -> None:
        if not self.is_running:
                return
        self.canvas.delete("agent_path")
        self.agents_finished = 0
        #the game loop
        self.game_loop()
        #generate new generation label
        self.generation_count += 1
        print(self.generation_count)
        #get the fittest and save them
        cutoff_index = int(len(self.population) * self.params.CUTOFF)
        bottom_agents = self.population[cutoff_index:]
        population_remaining = self.population[:cutoff_index]
        self.population = [agent.copy() for agent in population_remaining]
        #reproduce
        needed = self.params.NUM_AGENTS - len(self.population) - self.params.STRAGGLER_COUNT
        new_population = []
        while len(new_population) < needed:
            p1, p2 = random.sample(self.population, 2)
            child = self.crossover(p1, p2)
            child.mutate(self.params.MUTATION_RATE)
            new_population.append(child)
        self.population.extend(new_population)
        #save however many stragglers
        self.population.extend(straggler.copy() for straggler in random.sample(bottom_agents, self.params.STRAGGLER_COUNT))
        #conclude the generation, check if goal was reached and start the next
        print(self.population)
        if not self.is_running:
                return
        self.master.after(30, self.run_generation())

    def game_loop(self) -> None:
        prev_time = time.time()
        while(self.agents_finished < self.params.NUM_AGENTS and self.is_running):
            self.canvas.delete("agent")
            curr_time = time.time()
            delta_time = curr_time - prev_time
            prev_time = curr_time
            for agent in self.population:
                if not agent.has_collided:
                    prev_pos, curr_pos = agent.move(delta_time)
                    self.collision_check(agent)
                    self.goal_check(agent)
                    #draw the line
                    self.canvas.create_line(prev_pos[0], prev_pos[1], agent.position[0], agent.position[1], fill="black", width=1, tags="agent_path")
                    #draw the agent
                    r = 3
                    self.canvas.create_oval(
                        agent.position[0] - r, agent.position[1] - r, agent.position[0] + r, agent.position[1] + r,
                        fill="blue", tags="agent"
                    )
                    self.canvas.update()
            time.sleep(0.1)
        self.population.sort(
                key=lambda a: a.get_fitness(self.params.GOAL_POSITION), 
                reverse=True
            )
        

    def start_simulation(self) -> None:
        self.population = [ag.GeneticAgent(self.params.GENETIC_SEQUENCE_LENGTH, self.params.AGENT_SPEED, self.params.START_POSITION, self.params.TURN_RATE) for _ in range(self.params.NUM_AGENTS)]
        self.generation = 0
        self.is_running = True
        self.run_generation()
