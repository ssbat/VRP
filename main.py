
from CVRPTW import CVRPTW
from CVRPTW_info import CVRPTWInfo
from Tabou import Tabou
from CVRPTW_params import *
from Results.ResultsManager import ResultsManager

info = CVRPTWInfo(FULL_INSTANCE_NAME,CLIENTS_NUMBER)
AG = CVRPTW(info)
AG.optimize()

TABOU = Tabou(AG.population.best_solution)
TABOU.optimize()

csv_path = 'Results/params.csv'
RESULTS_MANAGER = ResultsManager(AG.population.best_solution, TABOU.best_chromosome, csv_path)
RESULTS_MANAGER.save_results_to_csv()