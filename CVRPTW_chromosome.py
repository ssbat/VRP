from CVRPTW_info import CVRPTWInfo


class Chromosome(object):
    def __init__(self, info: CVRPTWInfo,routes=[]) :
        self.is_valid = False
        
        # routes=[[1,2,3,4,1],[1,5,6,7]]
        #[1,2,3,4,1] -> camion
        self.routes=routes
        self.info=info
        pass


    def fitness(self):
        # if (valid):
            # distance
        # else:
            # finess = (erreur capactiy + erreur timewindow) +  max distance
        pass

    def fitness_2(self):
        pass
    
    # To Do (add the necessary parameters)
    def croisement(self):
        pass
    
    # Je ne suis pas sur pour l'id s'il le faut ou pas ou si on peut récupérer la route du camion autrement
    def isValid(self):

        for truck in self.routes:
            time = 0
            capacity = self.info.capacity

            for city in range(len(truck) - 1):
                city_travelled = truck[city]
                next_city = truck[city + 1]

                time += self.info.distances[city_travelled][next_city]

                if not (self.info.ready_times[next_city] <= time <= self.info.due_dates[next_city]):
                    return False
                
                if capacity < self.info.demand[next_city]:
                    return False
                
                time += self.info.service_times[next_city]
                capacity -= self.info.demand[next_city]
        
        return True

    # Extra
    def chromosome_correction(self):
        pass

    def mutation(self):
        pass

