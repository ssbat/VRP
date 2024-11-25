from CVRPTW_chromosome import Chromosome
import matplotlib.pyplot as plt
from CVRPTW_params import *
import random

class Tabou:
    def __init__(self, chromosome: Chromosome) -> None:
        self.chromosome = chromosome
        self.tabou_list = []
        self.neighbourhood = []
        self.chromosomes_history = dict()
        self.best_chromosome = None

    # On définit le voisinage d'un chromosome
    def set_neighbourhood(self) -> None:
        for _ in range(TABOU_NEIGHBOURHOOD_SIZE):
            copy_chromosome = self.chromosome.chromosome.copy()
            neighbour_chromosome = self.get_valid_neighbour(copy_chromosome)
            self.neighbourhood.append(neighbour_chromosome)
    
    # Sert à s'assurer de générer un voisin qui est valide, c'est à dire qui n'est pas dans la liste tabou
    def get_valid_neighbour(self, chromosome : list) -> list:
        while True:
            neighbour_chromosome = self.set_cities_permutations(chromosome)
            if neighbour_chromosome not in self.tabou_list:
                return neighbour_chromosome

    # La politique pour les mutations selon une probabilité   
    def set_cities_permutations(self, chromosome: list) -> list:  
        random_number = random.random()

        if random_number < 1/3:
            self.permutation_successive_cities(chromosome)
        elif random_number < 2/3:
            self.permutation_any_cities(chromosome)
        else:
            self.permutation_one_city(chromosome)

        return chromosome
            
    # Inversion de deux éléments successifs dans le chromosome
    def permutation_successive_cities(self, chromosome : list) -> None:
        random_city_index = random.randrange(len(chromosome) - 1)
        chromosome[random_city_index], chromosome[random_city_index + 1] = chromosome[random_city_index + 1], chromosome[random_city_index]
    
    # Permutation de deux éléments quelconques distincts
    def permutation_any_cities(self, chromosome : list) -> None:
        city_index_1, city_index_2 = random.sample(range(len(chromosome)), 2)
        chromosome[city_index_1], chromosome[city_index_2] = chromosome[city_index_2], chromosome[city_index_1]

    # Déplacement d’un élément de sa place d’origine à une nouvelle
    def permutation_one_city(self, chromosome : list) -> None:
        city_source_index, city_target_index = random.sample(range(len(chromosome)), 2)
        city = chromosome.pop(city_source_index)
        chromosome.insert(city_target_index, city)
      
    # Fonction principale
    def optimize(self):
        for generation in range(TABOU_NB_ITERATIONS):
            self.set_neighbourhood()

            self.neighbourhood = [Chromosome(chromosome) for chromosome in self.neighbourhood]

            valid_neighbours = [chromosome for chromosome in self.neighbourhood if chromosome.is_valid]

            best_neighbour = min(valid_neighbours, key=lambda chromosome: chromosome.fitness, default=None)

            if best_neighbour :
                if len(self.tabou_list) >= TABOU_LIST_SIZE_MAX:
                    self.tabou_list.pop(0)
                self.tabou_list.append(self.chromosome.chromosome.copy())
                self.chromosome = best_neighbour

            self.chromosomes_history[generation] = self.chromosome

            self.neighbourhood.clear()

        self.plotHistory()
        self.best_chromosome = min(self.chromosomes_history.values(), key=lambda chromo: chromo.total_travel_distance)
        print("Meilleure solution (distance la plus petite) :", self.best_chromosome)

    def plotHistory(self):
        x_values = list(self.chromosomes_history.keys())
        y_values = [chromosome.fitness for chromosome in self.chromosomes_history.values()]
        plt.figure(figsize=(6, 4))
        plt.plot(x_values, y_values, marker='o')
        plt.xlabel("generations")
        plt.ylabel("fitness")
        plt.title("fitness of the best chromosome")
        plt.grid(True)
        plt.show()