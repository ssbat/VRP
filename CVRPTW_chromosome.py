from CVRPTW_info import CVRPTWInfo

class Chromosome(object):
    def __init__(self, info: CVRPTWInfo,chromosome=[]) :
        self.is_valid = False
        
        #for 6 clients
        #chromosome exemple [1,4,2,5,7,6,2]
        self.chromosome=chromosome

        #decoded chromosome (transorm the chromosome to valid routes)
        # routes=[[1,2,3,4,1],[1,5,6,7]]
        self.routes=[[0]]

        self.info=info
        self.fitness = 0
        self.earlyTimePen = 0
        self.lateTimePen = 0
        
        self.decode_chromosome(self.chromosome)
        self.calculFitness()
        pass


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

    # To Change
    def calculFitness(self, w1=10, w2=5):
        #calcul fitness by distance
        for i in range (len(self.routes)):
            self.fitness += sum(self.info.distances[self.routes[i][j]][self.routes[i][j + 1]] for j in range(len(self.routes[i]) - 1))

            #change the flag of is_valid if the chromosome is correct
            if self.earlyTimePen == 0 and self.lateTimePen == 0:
                    self.is_valid = True
            #add time and capacity penalties if the chromosome is incorrect
            else:
                self.fitness += w1 * self.earlyTimePen + w2 * self.lateTimePen

            return self.fitness

    def fitness_2(self):
        pass
    
    # Je ne suis pas sur pour l'id s'il le faut ou pas ou si on peut récupérer la route du camion autrement
    def isValid(self,respect_arrivalTime:bool=False):
        valid = True
        self.capacityPen = 0
        self.timePen = 0
        for truck in self.routes:
            time = 0
            capacity = self.info.capacity
            for city in range(len(truck) - 1):
                city_travelled = truck[city]
                next_city = truck[city + 1]
                time += self.info.distances[city_travelled][next_city]

                #calcul pénalité de temps
                if not (time <= self.info.due_dates[next_city]) or (respect_arrivalTime and time < self.info.ready_times[next_city] ) :
                        if time < self.info.ready_times[next_city] and respect_arrivalTime:
                            self.timePen += self.info.ready_times[next_city] - time
                        elif time > self.info.due_dates[next_city]:
                            self.timePen += time - self.info.due_dates[next_city]

                time += self.info.service_times[next_city]
                capacity -= self.info.demand[next_city]

            #ajoute la capacité excès à la pénalité de capacité
            if capacity < 0:
                self.capacityPen += abs(capacity)

        if self.capacityPen > 0 or self.timePen > 0:
            valid = False
        return valid

    # Extra
    def chromosome_correction(self):
        pass

    def mutation(self):
        pass

    # route that respect capacity and due time without respecting arrival time
    def decode_chromosome(self,chromosome) ->list[list[int]]:
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
                if not self.check_time(0,dest):
                    self.move_vehicle(0,dest,self.info.distances[0][dest])
        print(f"{chromosome} => {self.routes}")
        print()

    def check_time(self, source: int, dest: int, distance: float=None) -> bool:
        elapsed_new = self.info.distances[source][dest]+self.elapsed_time
        # check if the vehicle arrive before the ready time
        if elapsed_new < self.info.ready_times[dest]:
            self.earlyTimePen += self.info.ready_times[dest] - elapsed_new
            elapsed_new = self.info.ready_times[dest]
            
        if elapsed_new <= self.info.due_dates[dest]:
              # to check if i can return to the depot before the due date if i visited dest
              return_time = self.info.distances[dest][0]
              if elapsed_new + self.info.service_times[dest] + return_time <= self.info.due_dates[0]:
                  return True
              else:
                  self.lateTimePen += elapsed_new + self.info.service_times[dest] + return_time - self.info.due_dates[0]
                  return False
        else:
            self.lateTimePen += elapsed_new + self.info.service_times[dest] - self.info.due_dates[dest]
            return False
                  

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

def pairwise(a: list) -> iter:
    """
    Iterate list items two by two
    Source: https://stackoverflow.com/a/5764948/4744051
    :param a: Given list, e.g.: a = [5, 7, 11, 4, 5]
    :return: Iterable pairs: [5, 7], [7, 11], [11, 4], [4, 5]
    """
    return zip(a[:-1], a[1:])