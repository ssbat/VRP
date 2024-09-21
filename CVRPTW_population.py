from CVRPTW_chromosome import Chromosome
from CVRPTW_info import CVRPTWInfo


class Population:
    def __init__(self, nb_generation, info: CVRPTWInfo):
        self.nb_generation=nb_generation
        self.info = info
        self.chromosomes:list[Chromosome]=[]

        pass
    
    def create_initial_population(self):
        pass
