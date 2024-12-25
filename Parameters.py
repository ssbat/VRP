import json
import os

from CVRPTW_params import PARAMETERS_PATH

class Parameters:
    _data = None
    _last_modified_time = None

    @staticmethod
    def _is_file_modified(file_path):
        """Vérifie si le fichier JSON a été modifié depuis le dernier chargement."""
        current_modified_time = os.path.getmtime(file_path)
        if Parameters._last_modified_time != current_modified_time:
            Parameters._last_modified_time = current_modified_time
            return True
        return False

    @staticmethod
    def reload_if_modified(file_path=PARAMETERS_PATH):
        with open(file_path, "r") as file:
                Parameters._data = json.load(file)

    @staticmethod
    def get(key, default_value=None):
        """Récupère un paramètre, en rechargeant si nécessaire."""
        Parameters.reload_if_modified()
        if key =="INSTANCE_NAME":
            default_value = "R101"
        if key =="CLIENTS_NUMBER":
            default_value = 25
        if key =="AG_NB_ITERATIONS":
            default_value = 5000
        if key == "AG_POPULATION_SIZE":
            default_value = 300
        if key == "AG_WAIT_COEFF":
            default_value = 0.5
        if key == "AG_DELAY_COEFF":
            default_value = 1.6
        if key == "AG_NB_VEHICULES_COEFF":
            default_value = 50
        if key == "AG_CX_PROBA":
            default_value = 0.85
        if key == "AG_MUT_PROBA":
            default_value = 0.5
        if key == "METHOD":
            default_value = "Genetic Alogorithm"
        if key == "TABOU_SEARCH_ON":
            default_value = False
        if key == "TABOU_LIST_SIZE_MAX":
            default_value = 10
        if key == "TABOU_NEIGHBOURHOOD_SIZE":
            default_value = 200
        if key == "TABOU_NB_ITERATIONS":
            default_value = 3000
        if key != "FULL_INSTANCE_NAME":
            return Parameters._data.get(key, default_value)
        else :
            return "instances/"+ str(Parameters._data.get("INSTANCE_NAME", "R101"))+"."+str(Parameters._data.get("CLIENTS_NUMBER", 25))+".txt"
