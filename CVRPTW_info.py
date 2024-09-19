
import math
class CVRPTWInfo :
    def __init__(self,instance_fileName: str) -> None:
        self.filename: str = instance_fileName
        self.capacity:int = None
        self.vehicules_number : int = None
        self.clients_number : int = None
        self.coords: list[tuple[float,float]] = None
        self.distances:list[list[int]] = []
        self.demand : list[int] = []
        self.ready_times : list[int] = []
        self.due_dates : list[int] = []
        self.service_times : list[int] = []
        self.read_instance_file()
        self.construct_distance_matrix()

    


    def read_instance_file(self):
        with open(self.filename) as f:
            file_lines= f.readlines()
            self.clients_number = int(file_lines[4].split()[0])
            self.capacity = int(file_lines[4].split()[1])
            self.coords=[(-1,-1) for i in range(self.clients_number +1)]
            # data starts from the line 9
            for (index, line) in enumerate(file_lines[9 : 9+self.clients_number +1]):
                line = line.split()
                self.coords[index] = (float(line[1]),float(line[2]))
                self.demand.append(int(line[3]))
                self.ready_times.append(int(line[4]))
                self.due_dates.append(int(line[5]))
                self.service_times.append(int(line[6]))
    
    def compute_euclidean_distance(self, n1, n2):
 
        return round(math.sqrt((n1[0] - n2[0])**2 + (n1[1] - n2[1])**2),2)

    def construct_distance_matrix(self):
        # we add +1 because there is the depot
        for site in range(self.clients_number + 1):
            distance_from_site=[]
            for to_site in range(self.clients_number + 1):
                distance_from_site.append(self.compute_euclidean_distance(self.coords[site],self.coords[to_site]))
            self.distances.append(distance_from_site)
    def print_distance_matrix(self):
        for i in range(len(self.distances)):
            for j in range(len(self.distances[i])):
               print(self.distances[i][j],end=' ')
            print()
            print()

