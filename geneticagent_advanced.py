'''
More advanced genetic agent with the following properties:

This genetic agent shoots out N linecasts of a certain length radially from itself 
It then uses these distances to determine its genetic code

genetic sequence element is a tuple of (np.array of distances of N size, and np.array direction)

For each iteration of turning (similar concept in basic agent) it will shoot out the linecasts and get back distances
Then it will iterate through its genetic sequence and see if each element Li of the sequence tuple is more than or equal to 
its corresponding line cast distance to an obstacle

For example: if the sequence is [([20.0], [0.8,0.8]), ([15.0], [-1,1])]
And it shoots out a singular line cast forward and that linecast returns a distance of 18.0, then it will turn in the direction specified in 
the second element of the tuple [0.8,0.8], otherwise maintain its original course
Both the sequence of distances and the direction vector will be seeded randomly and mutated accordingly 
'''
import random
import numpy as np
from geneticagent_virtual import GeneticAgent
import linecast
class GeneticAgentAdvanced(GeneticAgent):
    def __init__(self, sequence_length, speed, start, turn_rate, obstacles, linecast_length=25.0, linecast_count=8):
        self.sequence_length = sequence_length
        self.speed = speed
        self.linecast_vectors = []
        angles = np.linspace(0, 2*np.pi, linecast_count, endpoint=False)
        self.linecast_vectors = np.array(np.cos(angles), np.sin(angles)).T
        self.path = [] #total path taken per frame,
        self.final_position = np.array([0,0]) #this is either where it collides
        self.curr_iteration = 0 #index of the genetic direction currently being used
        self.position = np.array([start[0], start[1]])
        self.start_position = np.array([start[0], start[1]])
        self.curr_direction = self.genes[0]
        self.turn_rate = turn_rate
        self.iteration_delta_time = 0 #the amount of time that has passed since the current iteration started
        self.has_collided = False #stop moving agents that hit a wall already
        self.generation = 1 #current generation it is running in
        self.inception_generation = 1 #generation where this agent was created 
        self.genes = (np.random.uniform(-linecast_length,linecast_length, 
                                        (sequence_length, len(self.linecast_vectors))),np.random.uniform(-1.0, 1.0, (sequence_length, 2)))
        self.fitness = 0
        self.obstacles = obstacles

    def mutate(self,rate) -> None:
        pass

    def get_fitness(self, goal) -> float:
        dx = goal[0] - self.position[0]
        dy = goal[1] - self.position[1]
        fitness = 1 / (dx ** 2 + dy ** 2 + 1)
        self.fitness = fitness
        return fitness

    def copy(self, generation) -> object:
        pass

    def crossover(self, parent1, parent2, generation) -> object:
        pass

    def move(self, delta_time) -> tuple:
        pass

    #shoot all of your linecasts and return the nearest collision values of each in order
    @staticmethod
    def _shoot_linecasts(linecast_vectors, position, obstacles) -> np.ndarray:
        distances = np.zeros(len(linecast_vectors))
        for i in range(len(linecast_vectors)):
            distances[i] = linecast.cast_line(position, linecast_vectors[i], obstacles)

        return distances