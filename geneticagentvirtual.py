#virtual class for both types of genetic agent
from abc import ABC, abstractmethod
class GeneticAgent(ABC):
    #mutate function
    @abstractmethod
    def mutate(self,rate) -> None:
        pass
        #get the fitness based on goal position
    @abstractmethod
    def get_fitness(self, goal) -> float:
        pass
    
    #copy the genes for a new instance
    @abstractmethod
    def copy(self, generation) -> object:
        pass

    #create a child by mixing genes
    @abstractmethod
    def crossover(self, parent1, parent2, generation) -> object:
        pass
    

    #move the agent in the game loop
    @abstractmethod
    def move(self, delta_time) -> tuple:
        pass