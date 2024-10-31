import random
from CVRPTW_info import CVRPTWInfo
from constant import ClientNumber

class Chromosome(object):
    def __init__(self, info: CVRPTWInfo,chromosome=[],routes=None) :
        self.is_valid = False
        
        #for 6 clients
        #chromosome exemple [1,4,2,5,7,6,2]
        self.chromosome=chromosome

        #decoded chromosome (transorm the chromosome to valid routes)
        # routes=[[1,2,3,4,1],[1,5,6,7]]
        self.routes=[[0]]
        self.info=info
        self.decode_chromosome(self.chromosome)
        self.calculFitness()
        pass


    def update(self):
        self.decode_chromosome(self.chromosome)
        self.calculFitness()

    def intitialize_decoding_variables(self):
        # useful for decoding
        self.vehicles_count = 1
        self.route_rounds = 0
        self.total_travel_dist = 0
        self.routes=[[0]]
        self.total_elapsed_time = 0
        self.current_load = 0
        self.elapsed_time = 0
        self.max_elapsed_time = 0

    def initialize_fitness_variables(self):
        self.fitness = 0
        self.earlyTimePen = 0
        self.lateTimePen = 0
        self.travel_distance=0
        self.total_travel_distance=0
        self.elapsed_time_fitness = 0
        self.is_valid = False

        
    # To Change
    def calculFitness(self, w1=0.1, w2=2):
        self.initialize_fitness_variables()
        self.fitnessRoute = []
        for route in self.routes:
            self.timeRoute = 0
            for source, dest in pairwise(route):
                self.calcul_penality_fitness(source,dest)
                self.travel_distance = self.info.distances[source][dest]
                self.total_travel_distance+=self.travel_distance
                self.fitness += self.travel_distance

            self.fitnessRoute.append(self.timeRoute)
            self.elapsed_time_fitness += self.timeRoute
            
        #change the flag of is_valid if the chromosome is correct
        if self.lateTimePen == 0:
            self.is_valid = True
        #add time and capacity penalties if the chromosome is incorrect
        
        self.fitness += w1 * self.earlyTimePen + w2 * self.lateTimePen

        return self.fitness

    def fitness_2(self):
        pass

    # Extra
    def chromosome_correction(self):
        pass

    # route that respect capacity and due time without respecting arrival time
    def decode_chromosome(self,chromosome):
        self.intitialize_decoding_variables()
        random_indices=[0]+chromosome+[0]
        for source, dest in pairwise(random_indices):
            
            if self.current_load + self.info.demand[dest] <= self.info.capacity:
                if self.check_time(source, dest):
                    self.move_vehicle(source,dest,self.info.distances[source][dest])
                else:
                    self.move_vehicle(source,0)
                    self.initialize_new_route()
                    self.move_vehicle(0,dest)
            else:
                self.move_vehicle(source, 0)
                self.initialize_new_route()
                if not self.check_time(0,dest):
                    self.move_vehicle(0,dest,self.info.distances[0][dest])
        #print(f"{chromosome} => {self.routes}")
        #print()

    def check_time(self, source: int, dest: int, distance: float=None):
        elapsed_new = self.info.distances[source][dest]+self.elapsed_time
        if elapsed_new <= self.info.due_dates[dest]:
              # to check if i can return to the depot before the due date if i visited dest
              return_time = self.info.distances[dest][0]
              if elapsed_new + self.info.service_times[dest] + return_time <= self.info.due_dates[0]:
                  return True
              else:
                  return False
        else:
            return False

    def calcul_penality_fitness(self, source: int, dest: int):
        self.timeRoute += self.info.distances[source][dest]
        # add early time penalty if the vehicle arrives before the ready time
        if self.timeRoute < self.info.ready_times[dest]:
            self.earlyTimePen += self.info.ready_times[dest] - self.timeRoute
            self.timeRoute += self.info.ready_times[dest]  - self.timeRoute + self.info.service_times[dest]
        # add late time penalty if the vehicle arrives after the due date
        else:
            if self.timeRoute > self.info.due_dates[dest]:
                self.lateTimePen += self.timeRoute + self.info.service_times[dest] - self.info.due_dates[dest]
            self.timeRoute += self.info.service_times[dest]
            
                  

    def move_vehicle(self, source: int, dest: int, distance: float=None):
        if distance is None:
            distance = self.info.distances[source][dest]
        self.total_travel_dist += distance
        self.elapsed_time += distance + self.info.service_times[dest]
        self.max_elapsed_time = max(self.elapsed_time, self.max_elapsed_time)
        self.routes[-1].append(dest)
        if dest == 0:
            self.route_rounds += 1
            self.current_load = 0
        else:
            self.current_load += self.info.demand[dest]

    def initialize_new_route(self):
        self.vehicles_count += 1
        self.routes.append([0])
        self.elapsed_time = 0
        self.current_load = 0

    def __str__(self):
        return f'''fitness: {self.fitness}\n
        distance: {self.total_travel_distance}\n
        is valid: {self.is_valid}\n
        late time penality: {self.lateTimePen}\n
        early time penality: {self.earlyTimePen}\n
        chromsome:\n
        {self.chromosome}\n
        routes:\n
        {self.routes}'''

    def mutation_slice_points(self):
        chromosome_len=len(self.chromosome)
        slice_point_1 = random.randint(0, chromosome_len - 3)
        slice_point_2 = random.randint(slice_point_1 + 2, chromosome_len - 1)
        return slice_point_1, slice_point_2


    def mutation_inversion(self) -> list:
        slice_point_1, slice_point_2 = self.mutation_slice_points()
        self.chromosome = self.chromosome[:slice_point_1] + list(reversed(self.chromosome[slice_point_1:slice_point_2])) + self.chromosome[slice_point_2:]


    def mutation_scramble(self) -> list:
        slice_point_1, slice_point_2 = self.mutation_slice_points()
        scrambled = self.chromosome[slice_point_1:slice_point_2]
        random.shuffle(scrambled)
        self.chromosome= self.chromosome[:slice_point_1] + scrambled + self.chromosome[slice_point_2:]
        pass

def pairwise(a: list) -> iter:
    """
    Iterate list items two by two
    Source: https://stackoverflow.com/a/5764948/4744051
    :param a: Given list, e.g.: a = [5, 7, 11, 4, 5]
    :return: Iterable pairs: [5, 7], [7, 11], [11, 4], [4, 5]
    """
    return zip(a[:-1], a[1:])


# instance_name = 'C201'
# clients_number = ClientNumber.Hundred.value
# info = CVRPTWInfo(f'instances/{instance_name}.{clients_number}.txt',clients_number)
# c=Chromosome(info)

#optimum solution => 828
# c.chromosome=[81, 78, 76, 71, 70, 73, 77, 79, 80, 57, 55, 54, 53, 56, 58, 60, 59, 98, 96, 95, 94, 92, 93, 97, 100, 99, 32, 33, 31, 35, 37, 38, 39, 36, 34, 13, 17, 18, 19, 15, 16, 14, 12, 90, 87, 86, 83, 82, 84, 85, 88, 89, 91, 43, 42, 41, 40, 44, 46, 45, 48, 51, 50, 52, 49, 47, 67, 65, 63, 62, 74, 72, 61, 64, 68, 66, 69, 5, 3, 7, 8, 10, 11, 9, 6, 4, 2, 1, 75, 20, 24, 25, 27, 29, 30, 28, 26, 23, 22, 21]

#optimum solution => 591
# c.chromosome=[93,5,75,2,1,99,100,97,92,94,95,98,7,3,4,89,91,88,84,86,83,82,85,76,71,70,73,80,79,81,78,77,96,87,90,67,63,62,74,72,61,64,66,69,68,65,49,55,54,53,56,58,60,59,57,40,44,46,45,51,50,52,47,43,42,41,48,20,22,24,27,30,29,6,32,33,31,35,37,38,39,36,34,28,26,23,18,19,16,14,12,15,17,13,25,9,11,10,8,21]





# c.decode_chromosome(c.chromosome)
# c.calculFitness()
# print(c)
# pass









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
# pass
