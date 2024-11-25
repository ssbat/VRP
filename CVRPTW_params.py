from constant import ClientNumber
from utils import *


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

# Constantes pour la méthode tabou

# TABOU_SEARCH_ON = True
TABOU_LIST_SIZE_MAX = 10
# TABOU_NEIGHBOURHOOD_SIZE = 200
# TABOU_NB_ITERATIONS = 3000


# !! Load params from JSON file
parameters = load_parameters_from_file()

INSTANCE_NAME = parameters.get("INSTANCE_NAME", "R101")
CLIENTS_NUMBER = parameters.get("CLIENTS_NUMBER", ClientNumber.TwentyFive.value)
FULL_INSTANCE_NAME = f"instances/{INSTANCE_NAME}.{CLIENTS_NUMBER}.txt"

NB_ITERATIONS = parameters.get("NB_ITERATIONS", 5000)
POPULATION_SIZE = parameters.get("POPULATION_SIZE", 300)

WAIT_COEFF = parameters.get("WAIT_COEFF", 0.5)
DELAY_COEFF = parameters.get("DELAY_COEFF", 1.6)
NB_VEHICULES_COEFF = parameters.get("NB_VEHICULES_COEFF", 50)

CX_PROBA = parameters.get("CX_PROBA", 0.85)
MUT_PROBA = parameters.get("MUT_PROBA", 0.5)

# Tabou research parameters
TABOU_LIST_SIZE_MAX = parameters.get("TABOU_LIST_SIZE_MAX", 10)
TABOU_NEIGHBOURHOOD_SIZE = parameters.get("TABOU_NEIGHBOURHOOD_SIZE", 200)
TABOU_NB_ITERATIONS = parameters.get("TABOU_NB_ITERATIONS", 3000)

# Selected methode
METHOD = parameters.get("METHOD", "Algorithme Génétique")

CSV_PATH = 'Results/params.csv'