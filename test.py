from main import main_optimize
from utils import save_parameters_to_file
import random

# Définir les plages de paramètres, avec des valeurs fixes pour AG_DELAY_COEFF et AG_WAIT_COEFF
parameters_ranges = {
    "INSTANCE_NAME": ["R101", "R102", "R103", "R104", "R105"],
    "CLIENTS_NUMBER": [100],
    "AG_NB_ITERATIONS": range(100000, 1000001, 100000),  
    "AG_POPULATION_SIZE": range(100, 1001, 100),
    "AG_NB_VEHICULES_COEFF": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    "AG_CX_PROBA": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    "AG_MUT_PROBA": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    "TABOU_SEARCH_ON": [True],
    "TABOU_LIST_SIZE_MAX": range(2, 21), 
    "TABOU_NEIGHBOURHOOD_SIZE": range(100, 801, 100), 
    "TABOU_NB_ITERATIONS": range(1000, 5001, 1000),
    "AG_DELAY_COEFF": range(9, 21, 1),   
    "AG_WAIT_COEFF": [round(x, 2) for x in [0.05 * i for i in range(1, 6)]],
}

# Nombre d'expériences
num_experiments = 500

# Générer les paramètres
all_random_parameters = [
    {key: random.choice(value) for key, value in parameters_ranges.items()}
    for _ in range(num_experiments)
]

# Exécuter les expériences
for i, params in enumerate(all_random_parameters):
    print(f"\nRunning experiment {i + 1}/{num_experiments} with parameters: {params}")
    save_parameters_to_file(params)
    main_optimize()
