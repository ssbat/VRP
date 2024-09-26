import pygame
from CVRPTW_chromosome import Chromosome
from CVRPTW_info import CVRPTWInfo


class Interface:

    def __init__(self, chromosome: Chromosome):
        self.win = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("VRP visualizer")  
        self.chromosome = chromosome 
        self.info = chromosome.info
        #self.run()

    def run(self):
        clock = pygame.time.Clock()
        quit = False

        while not quit :
            self.win.fill((50,50,50))
            self.display()
            clock.tick(30)
            pygame.display.update()

    def display(self, frame: int):
        pass





info = CVRPTWInfo('instances/R101.25.txt')
print(info.clients_number)
routes = info.make_random_paths()
chromosome = Chromosome(info, routes)
Interface(chromosome)