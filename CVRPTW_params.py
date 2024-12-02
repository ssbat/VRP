from constant import ClientNumber
from utils import *


# INSTANCE_NAME= 'R101'
# CLIENTS_NUMBER = ClientNumber.TwentyFive.value
# FULL_INSTANCE_NAME = f'instances/{INSTANCE_NAME}.{CLIENTS_NUMBER}.txt'
# NB_ITERATIONS = 5000
# POPULATION_SIZE = 300
# INSTANCE_NAME= 'R101'
# CLIENTS_NUMBER = ClientNumber.TwentyFive.value
# FULL_INSTANCE_NAME = f'instances/{INSTANCE_NAME}.{CLIENTS_NUMBER}.txt'
# NB_ITERATIONS = 5000
# POPULATION_SIZE = 300

# WAIT_COEFF = 0.5
# DELAY_COEFF = 1.6
# NB_VEHICULES_COEFF = 50

# CX_PROBA = 0.85
# MUT_PROBA = 0.5
# WAIT_COEFF = 0.5
# DELAY_COEFF = 1.6
# NB_VEHICULES_COEFF = 50

# CX_PROBA = 0.85
# MUT_PROBA = 0.5

# Constantes pour la méthode tabou

# TABOU_LIST_SIZE_MAX = 10
# TABOU_NEIGHBOURHOOD_SIZE = 200
# TABOU_NB_ITERATIONS = 3000

CSV_PATH = 'Results/params.csv'


# !! Load params from JSON file
parameters = load_parameters_from_file()

INSTANCE_NAME = parameters.get("INSTANCE_NAME", "R101")
CLIENTS_NUMBER = parameters.get("CLIENTS_NUMBER", ClientNumber.TwentyFive.value)
FULL_INSTANCE_NAME = f"instances/{INSTANCE_NAME}.{CLIENTS_NUMBER}.txt"

AG_NB_ITERATIONS = parameters.get("AG_NB_ITERATIONS", 5000)
AG_POPULATION_SIZE = parameters.get("AG_POPULATION_SIZE", 300)

AG_WAIT_COEFF = parameters.get("AG_WAIT_COEFF", 0.5)
AG_DELAY_COEFF = parameters.get("AG_DELAY_COEFF", 1.6)
AG_NB_VEHICULES_COEFF = parameters.get("AG_NB_VEHICULES_COEFF", 50)

AG_CX_PROBA = parameters.get("AG_CX_PROBA", 0.85)
AG_MUT_PROBA = parameters.get("AG_MUT_PROBA", 0.5)

# Tabou research parameters
TABOU_LIST_SIZE_MAX = parameters.get("TABOU_LIST_SIZE_MAX", 10)
TABOU_NEIGHBOURHOOD_SIZE = parameters.get("TABOU_NEIGHBOURHOOD_SIZE", 200)
TABOU_NB_ITERATIONS = parameters.get("TABOU_NB_ITERATIONS", 3000)

# Selected method
METHOD = parameters.get("METHOD", "Genetic Alogorithm")

TABOU_SEARCH_ON = parameters.get("TABOU_SEARCH_ON", False)