import tkinter as tk
import json
from tkinter import ttk
from CVRPTW import CVRPTW
from CVRPTW_info import CVRPTWInfo
from Tabou import Tabou
from CVRPTW_params import *
from utils import *
from main import *


# Algorithms execution function
def execute_algorithm():
    selected_method = method_choice.get()
    
    tabou_search_on = False
    instance_name = instance_name_var.get()
    clients_number = int(clients_number_var.get())
    nb_iterations = int(nb_iterations_var.get())
    population_size = int(population_size_var.get())
    wait_coeff = float(wait_coeff_var.get())
    delay_coeff = float(delay_coeff_var.get())
    nb_vehicules_coeff = float(nb_vehicules_coeff_var.get())
    cx_proba = float(cx_proba_var.get())
    mut_proba = float(mut_proba_var.get())
    if selected_method == "Genetic Alogorithm + Tabou Research":
        tabou_search_on = True
        tabou_list_size = int(tabou_list_size_var.get())
        tabou_neighbourhood_size = int(tabou_neighbourhood_size_var.get())
        tabou_nb_iterations = int(tabou_nb_iterations_var.get())

    full_instance_name = f'instances/{instance_name}.{clients_number}.txt'

    parameters = {
        "INSTANCE_NAME": instance_name_var.get(),
        "CLIENTS_NUMBER": clients_number,
        "AG_NB_ITERATIONS": nb_iterations,
        "AG_POPULATION_SIZE": population_size,
        "AG_WAIT_COEFF": wait_coeff,
        "AG_DELAY_COEFF": delay_coeff,
        "AG_NB_VEHICULES_COEFF": nb_vehicules_coeff,
        "AG_CX_PROBA": cx_proba,
        "AG_MUT_PROBA": mut_proba,
        "METHOD": selected_method,
        "TABOU_SEARCH_ON":False
    }

    if tabou_search_on == True :
        parameters.update({
            "TABOU_LIST_SIZE_MAX": tabou_list_size,
            "TABOU_NEIGHBOURHOOD_SIZE": tabou_neighbourhood_size,
            "TABOU_NB_ITERATIONS": tabou_nb_iterations,
            "TABOU_SEARCH_ON":True
        })

    # Sauvegarder les paramètres dans un fichier JSON
    save_parameters_to_file(parameters)
    
    # Printing for log
    print(f"Instance: {instance_name}, Clients: {clients_number}")
    print(f"Nb Iterations: {nb_iterations}, Population Size: {population_size}")
    print(f"Wait Coeff: {wait_coeff}, Delay Coeff: {delay_coeff}, Vehicle Coeff: {nb_vehicules_coeff}")
    print(f"CX Proba: {cx_proba}, MUT Proba: {mut_proba}")
    if tabou_search_on == True :
        print(f"Tabou List Size: {tabou_list_size}, Neighbourhood Size: {tabou_neighbourhood_size}, Nb Iterations: {tabou_nb_iterations}")
    print(f"Selected Method: {selected_method}")
    print("----Parameters from file displaying----")
    for key, value in parameters.items():
        print(f"{key}: {value}")

    # !! Algorithm execution from main
    main()
    
    print("Execution is end.")

# Funtion to display or not tabou research params
def toggle_tabou_params(*args):
    if method_choice.get() == "Genetic Alogorithm + Tabou Research":
        tabou_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky=tk.W)
    else:
        tabou_frame.grid_forget()


# GUI
root = tk.Tk()
root.title("Configuration des Paramètres des Algorithmes")

# Colors setting
root.configure(bg="#f3f4f6")  # Couleur de fond principale
label_bg = "#e8eaf6"         # Fond des labels
frame_bg = "#c5cae9"         # Fond des frames
entry_bg = "#ffffff"         # Fond des champs de saisie
button_bg = "#7986cb"        # Fond des boutons
button_fg = "#000000"        # Couleur du texte des boutons
footer_bg = "#3f51b5"        # Fond de la barre des développeurs
footer_fg = "#ffffff"        # Couleur du texte de la barre des développeurs

parameters = load_parameters_from_file()

# Fields
instance_name_var = tk.StringVar(value=parameters["INSTANCE_NAME"])
clients_number_var = tk.StringVar(value=parameters["CLIENTS_NUMBER"])
nb_iterations_var = tk.StringVar(value=parameters["AG_NB_ITERATIONS"])
population_size_var = tk.StringVar(value=parameters["AG_POPULATION_SIZE"])
wait_coeff_var = tk.StringVar(value=parameters["AG_WAIT_COEFF"])
delay_coeff_var = tk.StringVar(value=parameters["AG_DELAY_COEFF"])
nb_vehicules_coeff_var = tk.StringVar(value=parameters["AG_NB_VEHICULES_COEFF"])
cx_proba_var = tk.StringVar(value=parameters["AG_CX_PROBA"])
mut_proba_var = tk.StringVar(value=parameters["AG_MUT_PROBA"])
tabou_list_size_var = tk.StringVar(value=parameters.get("TABOU_LIST_SIZE_MAX", 10))
tabou_neighbourhood_size_var = tk.StringVar(value=parameters.get("TABOU_NEIGHBOURHOOD_SIZE", 200))
tabou_nb_iterations_var = tk.StringVar(value=parameters.get("TABOU_NB_ITERATIONS", 3000))
method_choice = tk.StringVar(value=parameters["METHOD"])


method_choice.trace_add("write", toggle_tabou_params)

# Main frame
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

# Method choice
ttk.Label(frame, text="Méthode à utiliser : ", background=label_bg).grid(row=0, column=0, sticky=tk.W)
ttk.Combobox(
    frame, textvariable=method_choice, 
    values=["Genetic Alogorithm", "Genetic Alogorithm + Tabou Research"],
    state="readonly"
).grid(row=0, column=1, sticky=tk.W)

# Panel for general params
general_frame = tk.LabelFrame(frame, text="Paramètres Généraux", bg=frame_bg, fg="black", padx=10, pady=10)
general_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))

def create_entry(frame, row, label, text_var):
    tk.Label(frame, text=label, bg=label_bg).grid(row=row, column=0, sticky=tk.W)
    tk.Entry(frame, textvariable=text_var, width=20, bg=entry_bg).grid(row=row, column=1, sticky=tk.W)

create_entry(general_frame, 0, "Nom de l'Instance :", instance_name_var)
create_entry(general_frame, 1, "Nombre de Clients :", clients_number_var)
create_entry(general_frame, 2, "Nombre d'Itérations :", nb_iterations_var)
create_entry(general_frame, 3, "Taille de la Population :", population_size_var)
create_entry(general_frame, 4, "Coeff. d'Attente :", wait_coeff_var)
create_entry(general_frame, 5, "Coeff. de Délai :", delay_coeff_var)
create_entry(general_frame, 6, "Coeff. Véhicules :", nb_vehicules_coeff_var)
create_entry(general_frame, 7, "Taux de Croisement :", cx_proba_var)
create_entry(general_frame, 8, "Taux de Mutation :", mut_proba_var)

# Panel for tabou research panel
tabou_frame = tk.LabelFrame(frame, text="Paramètres Recherche Tabou", bg=frame_bg, fg="black", padx=10, pady=10)
create_entry(tabou_frame, 0, "Taille Max Liste Tabou :", tabou_list_size_var)
create_entry(tabou_frame, 1, "Taille Voisinage :", tabou_neighbourhood_size_var)
create_entry(tabou_frame, 2, "Nombre d'Itérations :", tabou_nb_iterations_var)

# Execution button
tk.Button(frame, text="Exécuter", command=execute_algorithm, bg=button_bg, fg=button_fg, padx=10, pady=5).grid(row=3, column=0, columnspan=2, pady=10)

# Bottom bar
footer_frame = tk.Frame(root, pady=5, bg=footer_bg)
footer_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
developer_label = tk.Label(footer_frame, text="Made by : Saad SBAT, Joël KADABA, Benoit CUENOT, \nQuang Huy DANG and François DELCROIX", anchor="center", bg=footer_bg, fg=footer_fg)
developer_label.pack(fill=tk.X)

# Launching interface
toggle_tabou_params()  # Toggling tabou research params for the first time
root.mainloop()