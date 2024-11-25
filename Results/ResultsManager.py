import csv 
from CVRPTW_params import *
from CVRPTW_chromosome import Chromosome

class ResultsManager :
    def __init__(self, ag_best_chromosome : Chromosome, tabou_best_chromosome : Chromosome, csv_path : str) -> None:
        self.csv_path = csv_path
        self.params_csv = {
            'instance_name' : INSTANCE_NAME,
            'clients_number' : CLIENTS_NUMBER,
            'ag_nb_iterations' : AG_NB_ITERATIONS,
            'ag_population_size' : AG_POPULATION_SIZE,
            'ag_wait_coeff' : AG_WAIT_COEFF,
            'ag_delay_coeff' : AG_DELAY_COEFF,
            'ag_nb_vehicules_coeff' : AG_NB_VEHICULES_COEFF,
            'ag_cx_proba' : AG_CX_PROBA,
            'ag_mut_proba' : AG_MUT_PROBA,
            'ag_fitness_result' : ag_best_chromosome.fitness,
            'ag_distance_result' : ag_best_chromosome.total_travel_distance,
            'ag_is_valid_result' : ag_best_chromosome.is_valid,
            'ag_late_time_penality_result' : ag_best_chromosome.lateTimePen,
            'ag_early_time_penality_result' : ag_best_chromosome.earlyTimePen,
            'ag_number_of_vehicules_result' : ag_best_chromosome.nb_vehicules,
            'ag_chromosome_result' : ag_best_chromosome.chromosome,
            'tabou_list_size_max' : TABOU_LIST_SIZE_MAX,
            'tabou_neighbourdhood_size' : TABOU_NEIGHBOURHOOD_SIZE,
            'tabou_nb_iterations' : TABOU_NB_ITERATIONS,
            'tabou_fitness_result' : tabou_best_chromosome.fitness,
            'tabou_distance_result' : tabou_best_chromosome.total_travel_distance,
            'tabou_is_valid_result' : tabou_best_chromosome.is_valid,
            'tabou_late_time_penality_result' : tabou_best_chromosome.lateTimePen,
            'tabou_early_time_penality_result' : tabou_best_chromosome.earlyTimePen,
            'tabou_number_of_vehicules_result' : tabou_best_chromosome.nb_vehicules,
            'tabou_chromosome_result' : tabou_best_chromosome.chromosome,
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