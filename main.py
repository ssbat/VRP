from CVRPTW import CVRPTW
from CVRPTW_info import CVRPTWInfo


info = CVRPTWInfo('instances/C101.100.txt')
ng_generation = 1000000
AG = CVRPTW(info,ng_generation)
AG.optimize()