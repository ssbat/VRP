
from CVRPTW import CVRPTW
from CVRPTW_info import CVRPTWInfo
from Tabou import Tabou
from CVRPTW_params import *
from Results.ResultsManager import ResultsManager

info = CVRPTWInfo(FULL_INSTANCE_NAME,CLIENTS_NUMBER)
AG = CVRPTW(info)
AG.optimize()

tabou_best_chromosome = None

if TABOU_SEARCH_ON and AG.population.best_solution.is_valid:
    TABOU = Tabou(AG.population.best_solution)
    TABOU.optimize()
    tabou_best_chromosome = TABOU.best_chromosome

RESULTS_MANAGER = ResultsManager(AG.population.best_solution, tabou_best_chromosome, CSV_PATH)
RESULTS_MANAGER.save_results_to_csv()