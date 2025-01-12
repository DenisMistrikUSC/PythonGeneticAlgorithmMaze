import random
import numpy as np
# define an agent, fitness, mutation, crossover, etc.
# movement will be based on a game loop system, genes will be vectors of direction, difference in direction will require longer turns
# direction can change at most each 0.5 second (adjustable turn rate) turning will require time, 
# at each iteration of the game loop, determine what the current index of gene direction and lerp between that vector and the succeeding one
#fitness will be based on collision penalty + distance from goal node
#mutation, simply take 

#parameters
#collision penalty
#mutation rate
#genetic sequence length
#time between turns
#speed of agent
#

class GeneticAgent:
    def __init__(self, sequence_length, speed, start, turn_rate):
        self.sequence_length = sequence_length
        self.genes = np.random.uniform(-1.0, 1.0, (sequence_length, 2))
        self.speed = speed
        self.path = [] #total path taken per frame,
        self.final_position = np.array([0,0]) #this is either where it collides
        self.curr_iteration = 0 #index of the genetic direction currently being used
        self.position = np.array([start[0], start[1]])
        self.start_position = np.array([start[0], start[1]])
        self.curr_direction = self.genes[0]
        self.turn_rate = turn_rate
        self.iteration_delta_time = 0 #the amount of time that has passed since the current iteration started
        self.has_collided = False #stop moving agents that hit a wall already

    def mutate(self,rate) -> None:
        for i in range(self.sequence_length):
            if random.uniform(0.0,1.0) < rate:
                self.genes[i] = (random.uniform(-1.0,1.0),random.uniform(-1.0,1.0))
    
    def get_fitness(self, goal) -> float:
        dx = goal[0] - self.position[0]
        dy = goal[1] - self.position[1]
        fitness = 1 / (dx ** 2 + dy ** 2 + 1)
        return fitness
    
    def copy(self) -> object:
        clone = GeneticAgent(self.sequence_length, self.speed, self.start_position, self.turn_rate)
        clone.genes = self.genes[:]
        return clone
    
    def crossover(self, parent1, parent2) -> object:
        child = GeneticAgent(self.sequence_length, self.speed, self.start_position, self.turn_rate)
        for i in range(self.sequence_length):
            if random.random() < 0.5:
                child.genes[i] = parent1.genes[i]
            else:
                child.genes[i] = parent2.genes[i]
        return child
    #check if delta_time puts it over turn rate, if so increase iteration by 1,
    # determine the turn rate by lerping the current iteration with the succeeding one (edge case on last one to not go over size)
    # determine velocity 
    # move 
    #collision check? do in main loop()
    def move(self, delta_time) -> tuple:
        old_position = self.position.copy()
        self.iteration_delta_time += delta_time
        if self.iteration_delta_time > self.turn_rate:
            self.curr_iteration = min(self.curr_iteration + 1, self.sequence_length - 2)
            self.iteration_delta_time = (self.iteration_delta_time - delta_time) - self.turn_rate
        i = self.curr_iteration
        x_dir = np.interp(self.iteration_delta_time, [0, self.turn_rate], [self.genes[i][0], self.genes[i + 1][0]])
        y_dir = np.interp(self.iteration_delta_time, [0, self.turn_rate], [self.genes[i][1], self.genes[i + 1][1]])
        self.curr_direction = np.array([x_dir,y_dir])
        velocity = self.curr_direction * self.speed
        self.position += velocity * delta_time
        self.path.append(self.position.copy())
       #
        return (old_position, self.position)

