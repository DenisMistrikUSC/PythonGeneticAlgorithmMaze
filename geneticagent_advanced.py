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

class GeneticAgentAdvanced(GeneticAgent):
    def __init__(self, sequence_length, speed, start, turn_rate):
        pass

    def mutate(self,rate) -> None:
        pass

    def get_fitness(self, goal) -> float:
        pass

    def copy(self, generation) -> object:
        pass

    def crossover(self, parent1, parent2, generation) -> object:
        pass

    def move(self, delta_time) -> tuple:
        pass