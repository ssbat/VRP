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
    

    def isValid(self):
        pass

    # Extra
    def chromosome_correction(self):
        pass

    def mutation(self):
        pass
    

