
import random
from CVRPTW_chromosome import Chromosome
from CVRPTW_info import CVRPTWInfo

import pygame, colorsys, pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button

from constant import ClientNumber


class Interface:

    screen_dimensions = (1920,1080)

    white = (255, 255, 255)
    blue = (0, 0, 255)
    red = (255, 0, 0)
    green = (0, 200, 0)
    grey = (100,100,100)
    black = (0, 0, 0)
    purple = (200, 0, 255)

    def __init__(self, chromosome: Chromosome, close_at_end = False):
        pygame.init()
        self.win = pygame.display.set_mode(Interface.screen_dimensions, pygame.FULLSCREEN)
        pygame.display.set_caption("VRP visualizer")  
        self.close_at_end = close_at_end
        self.chromosome = chromosome 
        self.info = chromosome.info
        self.quit = False
        clock = pygame.time.Clock()
        self.t = 0
        self.max_t = self.info.due_dates[0]
        self.zoom = 11
        self.speed = 1
        self.show_routes = True
        self.show_clients = True
        self.show_trucks = True

        self.build_instances()
        self.generate_background()
        self.build_widgets()

        # MAIN LOOP
        while not self.quit :
            self.display()
            self.manage_events()
            new_t = self.t + self.speed
            if new_t < 0:
                self.t = 0
            elif new_t > self.max_t:
                if self.close_at_end:
                    self.quit = True
                self.t = self.max_t
            else:
                self.t = new_t
            self.t_slider.setValue(self.t)
            clock.tick(30)
            pygame.display.update()

    
    def play(self):
        self.speed_slider.setValue(1)

    def pause(self):
        self.speed_slider.setValue(0)

    def reverse(self):
        self.speed_slider.setValue(-1)

    def show_hide_clients(self):
        self.show_clients = not self.show_clients

    def show_hide_routes(self):
        self.show_routes = not self.show_routes
    
    def show_hide_trucks(self):
        self.show_trucks = not self.show_trucks


    def build_widgets(self):
        self.speed_slider = Slider(self.win, 60, 400, 250, 20, min=-30, max=30, step = 1, initial = self.speed)
        self.speed_display = TextBox(self.win, 150, 350, 130, 35)

        self.t_slider = Slider(self.win, 60, 150, 250, 20, min=0, max=self.max_t, step = 1, initial = 0)
        self.t_display = TextBox(self.win, 150, 100, 130, 35)

        self.play_button = Button(
            self.win, 60,  600,  250,  50,
            text='Play', 
            fontSize=30, 
            margin=20,
            inactiveColour= Interface.white,  
            pressedColour=Interface.black, 
            radius=20, 
            onClick=lambda: self.play()
        )      

        self.pause_button = Button(
            self.win, 60,  700,  250,  50,
            text='Pause', 
            fontSize=30, 
            margin=20,
            inactiveColour= Interface.white,  
            pressedColour=Interface.black, 
            radius=20, 
            onClick=lambda: self.pause()
        ) 

        self.reverse_button = Button(
            self.win, 60,  800,  250,  50,
            text='Reverse', 
            fontSize=30, 
            margin=20,
            inactiveColour= Interface.white,  
            pressedColour=Interface.black, 
            radius=20, 
            onClick=lambda: self.reverse()
        ) 

        self.show_clients_button = Button(
            self.win, 1610,  600,  250,  50,
            text='Show/hide clients', 
            fontSize=30, 
            margin=20,
            inactiveColour= Interface.white,  
            pressedColour=Interface.black, 
            radius=20, 
            onClick=lambda: self.show_hide_clients()
        ) 

        self.show_routes_button = Button(
            self.win, 1610,  700,  250,  50,
            text='Show/hide routes', 
            fontSize=30, 
            margin=20,
            inactiveColour= Interface.white,  
            pressedColour=Interface.black, 
            radius=20, 
            onClick=lambda: self.show_hide_routes()
        ) 

        self.show_trucks_button = Button(
            self.win, 1610,  800,  250,  50,
            text='Show/hide trucks', 
            fontSize=30, 
            margin=20,
            inactiveColour= Interface.white,  
            pressedColour=Interface.black, 
            radius=20, 
            onClick=lambda: self.show_hide_trucks()
        ) 


    def build_instances(self):
        self.clients = []
        for i in range(1, self.info.clients_number):
            coord = self.info.coords[i]
            ready_time = self.info.ready_times[i]
            due_date = self.info.due_dates[i]
            service_time = self.info.service_times[i]
            self.clients.append(Client(coord, ready_time, due_date, service_time))

        self.trucks = []
        step = 1 / (len(self.chromosome.routes) + 10) 
        for i in range(0, len(self.chromosome.routes)):
            r, g, b = colorsys.hsv_to_rgb(step * i , 1, 1)
            r, g , b = int(r*255), int(g*255), int(b*255)
            self.trucks.append(Truck(self.chromosome.routes[i], (r, g, b), self.info))



    def generate_background(self):
        background  = pygame.Surface((Interface.screen_dimensions))
        background.fill(Interface.grey)

        x, y = self.convert_to_screen(self.info.coords[0])
        pygame.draw.rect(background, Interface.white, (x - 11, y - 11, 22, 22))
        pygame.draw.rect(background, Interface.black, (x - 10, y - 10, 20, 20))

        for t in self.trucks:
            for i in range(len(t.route) - 1):
                origin = self.convert_to_screen(self.info.coords[t.route[i]])
                destination = self.convert_to_screen(self.info.coords[t.route[i + 1]])
                pygame.draw.line(background, t.color, origin, destination, 1)

        self.background = background


    def display(self):

        if self.show_routes:
            self.win.blit(self.background,(0,0))
        else:
            self.win.fill(Interface.grey)

        if self.show_clients:
            for c in self.clients:
                c.draw(self)

        if self.show_trucks:
            for t in self.trucks:
                t.draw(self)
            
    
    def convert_to_screen(self, coord):
        x, y = coord
        return x*self.zoom + 480, y*self.zoom + 60


    def manage_events(self):
        events = pygame.event.get()
        pygame_widgets.update(events)
        self.speed = self.speed_slider.getValue()
        self.speed_display.setText("Speed = " + str(self.speed))

        self.t = self.t_slider.getValue()
        self.t_display.setText("Time = " + str(self.t))
        
        for event in events:
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
            color = Interface.red
        else:
            color = Interface.green

        x, y = interface.convert_to_screen(self.coord)
        pygame.draw.rect(interface.win, Interface.white, (x - 7, y - 7, 14, 14))
        pygame.draw.rect(interface.win, color, (x - 4, y - 4, 8, 8))


class Truck:

    def __init__(self, route, color, info):
        self.route = route
        self.color = color

        self.segments = []
        for i in range(len(self.route) - 1):
            self.segments.append(info.distances[route[i]][route[i + 1]])
            self.segments.append(info.service_times[route[i + 1]])
        

    def draw(self, interface):
        i = 0
        delta = self.segments[0]
        old_delta = 0

        while delta < interface.t and i < len(self.segments) - 1:
            old_delta = delta
            delta += self.segments[i + 1]
            i += 1

        if i%2:
            x, y = interface.convert_to_screen(interface.info.coords[self.route[i // 2 + 1]])
        else:
            x_origin, y_origin = interface.convert_to_screen(interface.info.coords[self.route[i // 2]])
            x_destination, y_destination = interface.convert_to_screen(interface.info.coords[self.route[i // 2 + 1]])

            length = delta - old_delta
            position = interface.t - old_delta
            coef = position / (length + 1)

            x = int(coef * x_destination + (1 - coef) * x_origin)
            y = int(coef * y_destination + (1 - coef) * y_origin)
            pygame.draw.line(interface.win, self.color, (x_origin, y_origin), (x_destination, y_destination), 2)

        pygame.draw.circle(interface.win, Interface.white, (x,y), 9)
        pygame.draw.circle(interface.win, self.color, (x,y), 8)

""" for prefix in ['R','C','RC']:
    for hundreds in ['10','20']:
        for units in range(1,9):
            for decimals in ['25', '50', '100']:
                try:
                    path = 'instances/' + prefix + hundreds + str(units) + '.' + decimals + '.txt'
                    info = CVRPTWInfo(path)
                    routes = info.make_random_paths()
                    chromosome = Chromosome(info, routes)
                    Interface(chromosome, True)
                except:
                    pass """







# instance_name = 'C101'
# clients_number = ClientNumber.Hundred.value
# info = CVRPTWInfo(f'instances/{instance_name}.{clients_number}.txt',clients_number)
# Chromosome.set_info_object(info)
# c=Chromosome()
# c.chromosome=[81, 78, 76, 71, 70, 73, 77, 79, 80, 57, 55, 54, 53, 56, 58, 60, 59, 98, 96, 95, 94, 92, 93, 97, 100, 99, 32, 33, 31, 35, 37, 38, 39, 36, 34, 13, 17, 18, 19, 15, 16, 14, 12, 90, 87, 86, 83, 82, 84, 85, 88, 89, 91, 43, 42, 41, 40, 44, 46, 45, 48, 51, 50, 52, 49, 47, 67, 65, 63, 62, 74, 72, 61, 64, 68, 66, 69, 5, 3, 7, 8, 10, 11, 9, 6, 4, 2, 1, 75, 20, 24, 25, 27, 29, 30, 28, 26, 23, 22, 21]
# c.decode_chromosome(c.chromosome)
# c.calculFitness()

# Interface(c)
# pygame.display.quit()
# pygame.quit()
# quit()

# path = 'instances/RC208.100.txt'
# info = CVRPTWInfo(path)
# info = CVRPTWInfo('instances/C101.100.txt')
# Chromosome.set_info_object(info)
# c=Chromosome(info)
# c.routes=[[0, 81, 78, 76, 71, 70, 73, 77, 79, 80, 0],
#  [0, 57, 55, 54, 53, 56, 58, 60, 59, 0],
#  [0, 98, 96, 95, 94, 92, 93, 97, 100, 99, 0],
#  [0, 32, 33, 31, 35, 37, 38, 39, 36, 34, 0],
#  [0, 13, 17, 18, 19, 15, 16, 14, 12, 0],
#  [0, 90, 87, 86, 83, 82, 84, 85, 88, 89, 91, 0],
#  [0, 43, 42, 41, 40, 44, 46, 45, 48, 51, 50, 52, 49, 47, 0],
#  [0, 67, 65, 63, 62, 74, 72, 61, 64, 68, 66, 69, 0],
#  [0, 5, 3, 7, 8, 10, 11, 9, 6, 4, 2, 1, 75, 0],
#  [0, 20, 24, 25, 27, 29, 30, 28, 26, 23, 22, 21, 0]]
# c.calculFitness()
# Interface(c, True)


# pygame.display.quit()
# pygame.quit()
# quit()

# instance_name = 'R101'
# clients_number = ClientNumber.TwentyFive.value
# info = CVRPTWInfo(f'instances/{instance_name}.{clients_number}.txt',clients_number)
# Chromosome.set_info_object(info)
# c=Chromosome()

# #optimum solution => 818
# c.chromosome=[14, 15, 13, 7, 8, 17, 12, 9, 20, 1, 5, 16, 6, 11, 19, 10, 23, 22, 4, 2, 21, 3, 24, 25, 18]
# c.decode_chromosome(c.chromosome)
# c.calculFitness()
# print(c)
# Interface(c, True)
# pass

# pygame.display.quit()
# pygame.quit()
# quit()