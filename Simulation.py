import pygame
from CVRPTW_chromosome import Chromosome
from CVRPTW_info import CVRPTWInfo


class Interface:

    screen_dimensions = (1920,1080)

    white = (200, 200, 200)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)

    def __init__(self, chromosome: Chromosome):
        pygame.init()
        self.win = pygame.display.set_mode(Interface.screen_dimensions, pygame.FULLSCREEN)
        pygame.display.set_caption("VRP visualizer")  
        self.chromosome = chromosome 
        self.info = chromosome.info
        self.quit = False
        clock = pygame.time.Clock()
        self.t = 0
        self.zoom = 11

        self.build_instances()

        # MAIN LOOP
        while not self.quit :
            self.manage_events()
            self.display()
            self.t += 1
            clock.tick(60)
            pygame.display.update()

    def build_instances(self):
        self.clients = []
        for i in range(1, self.info.clients_number):
            coord = self.info.coords[i]
            ready_time = self.info.ready_times[i]
            due_date = self.info.due_dates[i]
            service_time = self.info.service_times[i]
            self.clients.append(Client(coord, ready_time, due_date, service_time))


    def display(self):
        self.win.fill((100,100,100))
        for c in self.clients:
            c.draw(self)
            
    
    def convert_to_screen(self, coord):
        x, y = coord
        return x*self.zoom + 480, y*self.zoom + 60


    def manage_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit = True


class Client:

    def __init__(self, coord, ready_time, du_date, service_time):
        self.coord = coord
        self.ready_time = ready_time
        self.du_date = du_date
        self.service_time = service_time
        self.serviced = False

    def draw(self, interface):
        if interface.t < self.ready_time:
            color = Interface.white
        elif interface.t <= self.du_date:
            color = Interface.blue
        elif self.serviced:
            color = Interface.green
        else:
            color = Interface.red

        x, y = interface.convert_to_screen(self.coord)
        pygame.draw.rect(interface.win, (255,255,255), (x - 6, y - 6, 12, 12))
        pygame.draw.rect(interface.win, color, (x - 5, y - 5, 10, 10))




info = CVRPTWInfo('instances/RC208.100.txt')
routes = info.make_random_paths()
print(info.clients_number)
chromosome = Chromosome(info, routes)
Interface(chromosome)

pygame.display.quit()
pygame.quit()
quit()