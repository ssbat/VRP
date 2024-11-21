import copy
import pygame
from CVRPTW_info import CVRPTWInfo
from CVRPTW_params import *
from CVRPTW_population import Population
from CVRPTW_chromosome import Chromosome
import random
import matplotlib.pyplot as plt

from Simulation import Interface


class CVRPTW:
    def __init__(self,info: CVRPTWInfo):
        self.info = info
        self.best_routes=[]
        self.best_solution = None 
        fitness_history = []
        self.population = Population(info)
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

                children.append(Chromosome(child_1))
                children.append(Chromosome(child_2))
            else:
                children.append(Chromosome(parent_1.chromosome.copy()))
                children.append(Chromosome(parent_2.chromosome.copy()))

        return children

    def cx_partially_matched(self,childrens: list):
        ind1 = childrens[0].chromosome.copy()  # copy to avoid modifying original
        ind2 = childrens[1].chromosome.copy()  # copy to avoid modifying original
        cxpoint1, cxpoint2 = sorted(random.sample(range(min(len(ind1), len(ind2))), 2))
        part1 = ind2[cxpoint1:cxpoint2+1]
        part2 = ind1[cxpoint1:cxpoint2+1]
        
        rule1to2 = list(zip(part1, part2))
        is_fully_merged = False
        while not is_fully_merged:
            rule1to2, is_fully_merged = merge_rules(rules=rule1to2)
        
        rule2to1 = {rule[1]: rule[0] for rule in rule1to2}
        rule1to2 = dict(rule1to2)
        
        ind3 = [gene if gene not in part1 else rule1to2[gene] for gene in ind1[:cxpoint1]] + part1 + \
            [gene if gene not in part1 else rule1to2[gene] for gene in ind1[cxpoint2+1:]]

        ind4 = [gene if gene not in part2 else rule2to1[gene] for gene in ind2[:cxpoint1]] + part2 + \
            [gene if gene not in part2 else rule2to1[gene] for gene in ind2[cxpoint2+1:]]

        return [Chromosome(ind3),Chromosome(ind4)]

    def mutation(self,chromosomes:list[Chromosome],taux_mutation=0.8):
        taille_chromsome=self.info.clients_number
        for k in range(2):
            for i in range(len(chromosomes)):
                random_value = random.random()
                if random_value < taux_mutation:
                    index_1=-1
                    index_2=-1
                    while index_1 == index_2:
                        index_1 = random.randint(0,taille_chromsome - 1 )
                        index_2 = random.randint(0,taille_chromsome - 1)
                    chromosomes[i].chromosome[index_1],chromosomes[i].chromosome[index_2]=chromosomes[i].chromosome[index_2],chromosomes[i].chromosome[index_1]


    def optimize(self):
        nb_enfant= 2
        self.population.best_solution=copy.deepcopy(self.population.chromosomes[0])
        for generation in range(NB_ITERATIONS) :
            self.population.sort()
            self.population.fitness_history[generation] = self.population.chromosomes[0].fitness
            if self.population.chromosomes[0].fitness < self.population.best_solution.fitness:# and self.population.chromosomes[0].is_valid==True:    
                self.population.best_solution=copy.deepcopy(self.population.chromosomes[0])
            parents=self.population.rank_selection_sorted(nb_enfant)
            if random.random()< CX_PROBA:
                childrens = self.cx_partially_matched(parents)
            #childrens=self.croisement_OX(parents)
            for child in childrens:
                if random.random()< MUT_PROBA:
                    child.mutation_scramble()
            #self.mutation(childrens)
            for children in childrens:
                children.update()

            # To do -> replace by ranking
            self.population.chromosomes[-nb_enfant:]= childrens
            if generation % 10000 == 0:
                print(f"Generation: {generation} best fitness: {self.population.best_solution.fitness}")
            pass
        print(self.population.best_solution)
        self.plotHistory()
        """Interface(self.population.best_solution, True)
        pygame.display.quit()
        pygame.quit()
        quit()"""
        pass

    def plotHistory(self):
        x_values = list(self.population.fitness_history.keys())
        y_values = list(self.population.fitness_history.values())

        # Create the plot
        plt.figure(figsize=(6, 4))
        plt.plot(x_values, y_values, marker='o')

        # Add labels and title
        plt.xlabel("generations")
        plt.ylabel("fitness")
        plt.title("fitness of the best chromosome")
        # Display the plot
        plt.grid(True)
        plt.show()
    
def merge_rules(rules):
    is_fully_merged = True
    for round1 in rules:
        if round1[0] == round1[1]:
            rules.remove(round1)
            is_fully_merged = False
        else:
            for round2 in rules:
                if round2[0] == round1[1]:
                    rules.append((round1[0], round2[1]))
                    rules.remove(round1)
                    rules.remove(round2)
                    is_fully_merged = False
    return rules, is_fully_merged


# liste2 = [[1, 2,3,4,5,6], [6,5,4,3,2,1]]
# liste2 = cx_partially_matched(liste2)  # Update liste2 with the returned value
# print(liste2)