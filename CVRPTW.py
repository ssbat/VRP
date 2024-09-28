from CVRPTW_info import CVRPTWInfo
from CVRPTW_population import Population


class CVRPTW:
    def __init__(self,info: CVRPTWInfo,nb_generation):
        self.info = info
        self.best_routes=[]
        self.best_solution = None 
        fitness_history = []
        self.population = Population(nb_generation, info)
        self.nb_generation = nb_generation
        pass


    def croisement(self,chromsomes):
        pass

    def optimize(self):
        nb_enfant= 4
        for generation in range(self.nb_generation) :
            parents=self.population.rank_selection_sorted(nb_enfant)
            pass
        pass
    

