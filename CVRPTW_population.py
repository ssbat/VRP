from CVRPTW_chromosome import Chromosome
from CVRPTW_info import CVRPTWInfo


class Population:
    def __init__(self, nb_generation, info: CVRPTWInfo):
        self.nb_generation=nb_generation
        self.info = info
        self.chromosomes:list[Chromosome]=[]
        self.create_initial_population()

        pass
    
    def create_initial_population(self):
        self.chromosomes=[self.info.make_random_paths() for _ in range(800)]
        pass

    def sort():
        # [c1:204 valid,c2:200 non valide,c3:210 valide,c4: 230: non valid]
        # return [c1,c3,c3,c4]
        pass