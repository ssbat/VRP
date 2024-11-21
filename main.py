
from CVRPTW import CVRPTW
from CVRPTW_info import CVRPTWInfo
from Tabou import Tabou
from CVRPTW_params import *

info = CVRPTWInfo(FULL_INSTANCE_NAME,CLIENTS_NUMBER)
AG = CVRPTW(info)
AG.optimize()

TABOU = Tabou(AG.population.best_solution)
TABOU.optimize()