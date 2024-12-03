from main import main_optimize
from utils import save_parameters_to_file

parameters = {
    "INSTANCE_NAME": "R101",
    "CLIENTS_NUMBER": 25,
    "AG_NB_ITERATIONS": 10000,
    "AG_POPULATION_SIZE": 300,
    "AG_WAIT_COEFF": 0.5,
    "AG_DELAY_COEFF": 9,
    "AG_NB_VEHICULES_COEFF": 50.0,
    "AG_CX_PROBA": 0.8,
    "AG_MUT_PROBA": 0.5,
    "METHOD": "Genetic Algorithm + Tabou Research",
    "TABOU_LIST_SIZE_MAX": 10,
    "TABOU_NEIGHBOURHOOD_SIZE": 200,
    "TABOU_NB_ITERATIONS": 3000,
    "TABOU_SEARCH_ON": True
}
save_parameters_to_file(parameters)

main_optimize()