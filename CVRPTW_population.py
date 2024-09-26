from CVRPTW_chromosome import Chromosome
from CVRPTW_info import CVRPTWInfo


class Population:
    def __init__(self, nb_generation, info: CVRPTWInfo):
        self.nb_generation=nb_generation
        self.info = info
        self.chromosomes:list[Chromosome]=[]
        self.create_initial_population()
        self.chromosomes = self.sort()

        pass
    
    def create_initial_population(self):
        self.chromosomes=[Chromosome(self.info, self.info.make_random_paths()) for _ in range(800)]

    def sort(self):
        chromosomeValid, chromosomeInvalid = [], []
        for i in self.chromosomes:
            i.calculFitness()
            if i.is_valid == False:
                chromosomeInvalid.append(i)
            else:
                chromosomeValid.append(i)
        chromosomeInvalid.sort(key = lambda chromosome: chromosome.fitness, reverse=True)
        chromosomeValid.sort(key = lambda chromosome: chromosome.fitness, reverse=True)
        return chromosomeValid + chromosomeInvalid
