import csv 
from CVRPTW_params import *
from CVRPTW_chromosome import Chromosome
from Parameters import Parameters

class ResultsManager :
    def __init__(self, ag_best_chromosome : Chromosome, tabou_best_chromosome : Chromosome | None, csv_path : str) -> None:
        self.csv_path = csv_path
        self.params_csv = {
            'instance_name' : Parameters.get(INSTANCE_NAME),
            'clients_number' : Parameters.get(CLIENTS_NUMBER),
            'ag_nb_iterations' : Parameters.get(AG_NB_ITERATIONS),
            'ag_population_size' : Parameters.get(AG_POPULATION_SIZE),
            'ag_wait_coeff' : Parameters.get(AG_WAIT_COEFF),
            'ag_delay_coeff' : Parameters.get(AG_DELAY_COEFF),
            'ag_nb_vehicules_coeff' : Parameters.get(AG_NB_VEHICULES_COEFF),
            'ag_cx_proba' : Parameters.get(AG_CX_PROBA),
            'ag_mut_proba' : Parameters.get(AG_MUT_PROBA),
            'ag_fitness_result' : ag_best_chromosome.fitness,
            'ag_distance_result' : ag_best_chromosome.total_travel_distance,
            'ag_is_valid_result' : ag_best_chromosome.is_valid,
            'ag_late_time_penality_result' : ag_best_chromosome.lateTimePen,
            'ag_early_time_penality_result' : ag_best_chromosome.earlyTimePen,
            'ag_number_of_vehicules_result' : ag_best_chromosome.nb_vehicules,
            'ag_chromosome_result' : ag_best_chromosome.chromosome,
            'is_tabou_executed' : Parameters.get(TABOU_SEARCH_ON),
            'tabou_list_size_max' : Parameters.get(TABOU_LIST_SIZE_MAX) if tabou_best_chromosome else None,
            'tabou_neighbourdhood_size' : Parameters.get(TABOU_NEIGHBOURHOOD_SIZE) if tabou_best_chromosome else None,
            'tabou_nb_iterations' : Parameters.get(TABOU_NB_ITERATIONS) if tabou_best_chromosome else None,
            'tabou_fitness_result' : tabou_best_chromosome.fitness if tabou_best_chromosome else None,
            'tabou_distance_result' : tabou_best_chromosome.total_travel_distance if tabou_best_chromosome else None,
            'tabou_is_valid_result' : tabou_best_chromosome.is_valid if tabou_best_chromosome else None,
            'tabou_late_time_penality_result' : tabou_best_chromosome.lateTimePen if tabou_best_chromosome else None,
            'tabou_early_time_penality_result' : tabou_best_chromosome.earlyTimePen if tabou_best_chromosome else None,
            'tabou_number_of_vehicules_result' : tabou_best_chromosome.nb_vehicules if tabou_best_chromosome else None,
            'tabou_chromosome_result' : tabou_best_chromosome.chromosome if tabou_best_chromosome else None,
        }
        
    def save_results_to_csv(self):

        headers_exist = False
           
        try:
            with open(self.csv_path, 'r') as file:
                headers_exist = True
        except FileNotFoundError:
            pass
          
        with open(self.csv_path, 'a', newline='') as file:
            writer = csv.writer(file)
            if not headers_exist:
                writer.writerow(self.params_csv.keys())
            writer.writerow(self.params_csv.values())

        print(f"Résultats sauvegardés dans {self.csv_path}")      