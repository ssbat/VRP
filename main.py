
from CVRPTW import CVRPTW
from CVRPTW_info import CVRPTWInfo
from Parameters import Parameters
from Tabou import Tabou
from CVRPTW_params import *
from Results.ResultsManager import ResultsManager

import tkinter as tk
from tkinter import ttk

def show_error_popup(root, message):
    """
    Affiche une fenêtre pop-up d'erreur avec un message donné.
    """
    error_popup = tk.Toplevel(root)
    error_popup.title("Erreur")
    error_popup.geometry("300x150") 

    label = ttk.Label(error_popup, text=message, font=("Arial", 12), foreground="red")
    label.pack(pady=20)

    close_button = ttk.Button(error_popup, text="Fermer", command=error_popup.destroy)
    close_button.pack(pady=10)

def main_optimize(root=None):
    info = CVRPTWInfo(Parameters.get(FULL_INSTANCE_NAME),Parameters.get(CLIENTS_NUMBER))
    AG = CVRPTW(info)
    AG.optimize()

    tabou_best_chromosome = None
    
    # Vérification de la validité de la meilleure solution
    if root!=None and not AG.population.best_solution.is_valid:
        # Afficher une pop-up d'erreur si la solution n'est pas valide
        show_error_popup(root, "La meilleure solution trouvée n'est pas valide, réessayez avec d'autres paramètres !")

    if Parameters.get(TABOU_SEARCH_ON) and AG.population.best_solution.is_valid:
        
        print("\n*************************")
        print("Taboo is being executed")
        print("************************")

        TABOU = Tabou(AG.population.best_solution)
        TABOU.optimize()
        tabou_best_chromosome = TABOU.best_chromosome

    RESULTS_MANAGER = ResultsManager(AG.population.best_solution, tabou_best_chromosome, CSV_PATH)
    RESULTS_MANAGER.save_results_to_csv() 


if __name__ == "__main__":
    print("Please run main_view.py")