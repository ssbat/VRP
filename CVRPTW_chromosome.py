from CVRPTW_info import CVRPTWInfo

class Chromosome(object):
    def __init__(self, info: CVRPTWInfo,routes=[]) :
        self.is_valid = False
        
        # routes=[[1,2,3,4,1],[1,5,6,7]]
        #[1,2,3,4,1] -> camion
        self.routes=routes
        self.info=info
        self.fitness = 0
        pass


    def calculFitness(self):
        #calcul fitness by distance
        for i in range (len(self.routes)):
            self.fitness += sum(self.info.distances[self.routes[i][j]][self.routes[i][j + 1]] for j in range(len(self.routes[i]) - 1))

            #change the flag of is_valid if the chromosome is correct
            if self.isValid():
                    self.is_valid = True
            #add time and capacity penalties if the chromosome is incorrect
            else:
                self.fitness += 25 * (self.timePen + self.capacityPen)

            return self.fitness

    def fitness_2(self):
        pass
    
    # Je ne suis pas sur pour l'id s'il le faut ou pas ou si on peut récupérer la route du camion autrement
    def isValid(self):
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
                if not (self.info.ready_times[next_city] <= time <= self.info.due_dates[next_city]):
                    if time < self.info.ready_times[next_city]:
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

