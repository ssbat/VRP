from main import main_optimize
from utils import save_parameters_to_file
import random

# Définir les plages de paramètres
parameters_ranges = {
    "INSTANCE_NAME": ["R101", "R102", "R103", "R104", "R105"],
    "CLIENTS_NUMBER": [50],
    "AG_NB_ITERATIONS": range(10000, 300001, 10000),  
    "AG_POPULATION_SIZE": range(50, 501, 50),
    "AG_NB_VEHICULES_COEFF": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    "AG_CX_PROBA": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    "AG_MUT_PROBA": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    "TABOU_SEARCH_ON": [True],
    "TABOU_LIST_SIZE_MAX": range(2, 21), 
    "TABOU_NEIGHBOURHOOD_SIZE": range(100, 801, 100), 
    "TABOU_NB_ITERATIONS": range(1000, 5001, 1000), 
}

num_experiments = 500

all_random_parameters = []
for _ in range(num_experiments):
    random_value = random.randint(1, 10)
    
    if random.choice([True, False]):
        ag_delay_coeff = random_value
        ag_wait_coeff = 1
    else:
        ag_delay_coeff = 1
        ag_wait_coeff = random_value
    
    params = {
        **{key: random.choice(value) for key, value in parameters_ranges.items()},
        "AG_DELAY_COEFF": ag_delay_coeff,
        "AG_WAIT_COEFF": ag_wait_coeff
    }
    all_random_parameters.append(params)

for i, params in enumerate(all_random_parameters):
    print(f"\nRunning experiment {i + 1}/{num_experiments} with parameters: {params}")
    
    save_parameters_to_file(params)
    
    main_optimize()
