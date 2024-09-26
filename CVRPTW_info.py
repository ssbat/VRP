
import math
import random
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
        pass
    


    def read_instance_file(self):
        with open(self.filename) as f:
            file_lines= f.readlines()
            self.vehicules_number = int(file_lines[4].split()[0])
            self.capacity = int(file_lines[4].split()[1])
            self.clients_number = len(file_lines) - 11
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


    def make_random_paths(self) ->list[list[int]]:
        # return [[0,1,2,3,4,0],[0,9,8,7,0],...]
        max_route_len = 6
        unserviced = [i for i in range(1, self.clients_number + 1)]
        #print(unserviced)
        random.shuffle(unserviced)
        routes = []
        cur_route = [0]
        route_demand = 0
        route_length = 0
        while unserviced:
            # choose the closest unserviced node from the last node of the current node
            i = min([i for i in range(len(unserviced))], \
                    key=lambda x: self.distances[cur_route[-1] if random.uniform(0, 1) < 0.9 else 1][unserviced[x]])
            node = unserviced[i]
            if route_length <=max_route_len and route_demand + self.demand[node] <= self.capacity:
                cur_route += [node]
                route_length += 1
                route_demand += self.demand[node]
                del unserviced[i]
                continue
            # to return to the depot
            cur_route += [0]
            routes += [cur_route]
            cur_route = [0]
            route_demand = 0
            route_length = 0
        routes += [cur_route + [0]]
        return routes