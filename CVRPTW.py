from CVRPTW_info import CVRPTWInfo
from CVRPTW_population import Population
from CVRPTW_chromosome import Chromosome
import random


class CVRPTW:
    def __init__(self,info: CVRPTWInfo,nb_generation):
        self.info = info
        self.best_routes=[]
        self.best_solution = None 
        fitness_history = []
        self.population = Population(nb_generation, info)
        self.nb_generation = nb_generation
        pass


    def croisement_OX(self, chromosomes : list[Chromosome], taux_croisement : float = 0.8) -> list[Chromosome]:
        children = []
        while chromosomes:
            parent_1, parent_2 = random.sample(chromosomes, 2)
            chromosomes.remove(parent_1)
            chromosomes.remove(parent_2)

            random_value = random.random()

            if random_value < taux_croisement:
                size = len(parent_1.chromosome)
                start_index_crossing_point  = size // 3
                end_index_crossing_point = start_index_crossing_point * 2

                child_1 = [None] * size
                child_1[start_index_crossing_point:end_index_crossing_point] = parent_1.chromosome[start_index_crossing_point:end_index_crossing_point]

                index_child = 0
                for city in parent_2.chromosome:
                    if city not in child_1:
                        while child_1[index_child] is not None:
                            index_child += 1
                        child_1[index_child] = city

                child_2 = [None] * len(parent_2.chromosome)
                child_2[start_index_crossing_point:end_index_crossing_point] = parent_2.chromosome[start_index_crossing_point:end_index_crossing_point]
    
                index_child = 0
                for city in parent_1.chromosome:
                    if city not in child_2:
                        while child_2[index_child] is not None:
                            index_child += 1
                        child_2[index_child] = city

                children.append(Chromosome(self.info, child_1))
                children.append(Chromosome(self.info, child_2))
            else:
                children.append(Chromosome(self.info, parent_1.chromosome.copy()))
                children.append(Chromosome(self.info, parent_2.chromosome.copy()))

        return children

    def mutation(self,chromosomes:list[Chromosome],taux_mutation=0.8):
        taille_chromsome=self.info.clients_number
        for i in range(len(chromosomes)):
            random_value = random.random()
            if random_value < taux_mutation:
                index_1=-1
                index_2=-1
                while index_1 == index_2:
                    index_1 = random.randint(0,taille_chromsome)
                    index_2 = random.randint(0,taille_chromsome)
                chromosomes[i].chromosome[index_1],chromosomes[i].chromosome[index_2]=chromosomes[i].chromosome[index_2],chromosomes[i].chromosome[index_1]


    def optimize(self):
        nb_enfant= 2
        for generation in range(self.nb_generation) :
            self.population.sort()
            self.population.fitness_history[generation] = self.population.chromosomes[0].fitness
            parents=self.population.rank_selection_sorted(nb_enfant)
            childrens = self.croisement_OX(parents)
            self.mutation(childrens)

            # To do -> replace by ranking
            self.population.chromosomes[-nb_enfant:]= childrens
            pass
        pass
    

