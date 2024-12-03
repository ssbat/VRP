import random
from CVRPTW_chromosome import Chromosome
from CVRPTW_info import CVRPTWInfo
from CVRPTW_params import *
from Parameters import Parameters


class Population:
    def __init__(self, info: CVRPTWInfo):
        self.info = info
        self.chromosomes:list[Chromosome]=[]
        self.fitness_sum = 0
        self.fitness_history = dict()
        self.best_solution:Chromosome = None
        Chromosome.set_info_object(info)
        self.create_initial_population()
        self.sort()
        random.seed()

        pass
    
    def create_initial_population(self):
        chromosome_random = list(range(1, self.info.clients_number+1))
        self.chromosomes=[Chromosome(random.sample(chromosome_random,len(chromosome_random))) for _ in range(Parameters.get(AG_POPULATION_SIZE))]

    def sort(self) :
       self.chromosomes.sort(key=lambda chromosome: (not chromosome.is_valid, chromosome.fitness))
       #self.chromosomes.sort(key = lambda chromosome: chromosome.fitness, reverse=False)
    
    def roulette_wheel_selection(self,num=2):
        selected_chromomes=[]
        max_fitness = max(chromosome.fitness for chromosome in self.chromosomes)
        inverted_fitnesses = [max_fitness - chromosome.fitness for chromosome in self.chromosomes]
        # Handle the case where all fitness values are equal (to avoid division by zero)
        total_fitness = sum(inverted_fitnesses)
        if total_fitness == 0:
          return random.sample(self.chromosomes, num)
        
        rel_fitness = [f/total_fitness  for f in inverted_fitnesses]
        # Generate probability intervals for each individua;
        probs = [sum(rel_fitness[:i+1]) for i in range(len(rel_fitness))]
        for n in range(num):
                r = random.rand()
                for (i, individual) in enumerate(self.chromosomes):
                    if r <= probs[i]:
                        selected_chromomes.append(individual)
                        break
        return selected_chromomes
    
    def rank_selection_sorted(self,num):
        """ Rank selection for a pre-sorted population.
            Individuals are selected based on their rank in the sorted population.
        """
        ranks = list(range(1, len(self.chromosomes) + 1))
        
        # Calculate total ranks
        total_ranks = sum(ranks)

        # Calculate selection probabilities based on ranks
        selection_probs = [(len(self.chromosomes) - rank + 1) / total_ranks for rank in ranks]

        # Generate cumulative probabilities
        cumulative_probs = [sum(selection_probs[:i+1]) for i in range(len(selection_probs))]

        selected_chromomes=[]
        for n in range(num):
            r = random.random()  
            for i, individual in enumerate(self.chromosomes):
                if r <= cumulative_probs[i]:
                    selected_chromomes.append(individual)  # Append the individual
                    break

        return selected_chromomes
        
