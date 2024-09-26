from CVRPTW_info import CVRPTWInfo
from CVRPTW_population import Population


class CVRPTW:
    def __init__(self,info: CVRPTWInfo,nb_generation):
        self.info = info
        self.best_routes=[]
        self.best_solution = None 
        fitness_history = []
        self.population = Population(nb_generation, info)
        pass

    def optimize(self):
        pass
    

