
from CVRPTW import CVRPTW
from CVRPTW_info import CVRPTWInfo
from Parameters import Parameters
from Tabou import Tabou
from CVRPTW_params import *
from Results.ResultsManager import ResultsManager

def main():
    info = CVRPTWInfo(Parameters.get(FULL_INSTANCE_NAME),Parameters.get(CLIENTS_NUMBER))
    AG = CVRPTW(info)
    AG.optimize()

    tabou_best_chromosome = None

    if Parameters.get(TABOU_SEARCH_ON) and AG.population.best_solution.is_valid:
        TABOU = Tabou(AG.population.best_solution)
        TABOU.optimize()
        tabou_best_chromosome = TABOU.best_chromosome

    RESULTS_MANAGER = ResultsManager(AG.population.best_solution, tabou_best_chromosome, CSV_PATH)
    RESULTS_MANAGER.save_results_to_csv()