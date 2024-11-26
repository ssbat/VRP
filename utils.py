import json

def load_parameters_from_file(file_path="parameters.json"):
    """
    Charge les paramètres depuis un fichier JSON.
    
    :param file_path: Chemin du fichier JSON contenant les paramètres.
    :return: Dictionnaire contenant les paramètres chargés.
    """
    try:
        with open(file_path, 'r') as file:
            parameters = json.load(file)
        print(f"Paramètres chargés depuis {file_path}")
        return parameters
    except FileNotFoundError:
        print(f"Erreur : le fichier {file_path} est introuvable.")
        return {}
    except json.JSONDecodeError:
        print(f"Erreur : le fichier {file_path} contient des données JSON invalides.")
        return {}
    
def save_parameters_to_file(parameters, file_path="parameters.json"):
    with open(file_path, 'w') as file:
        json.dump(parameters, file, indent=4)
    print(f"Paramètres enregistrés dans {file_path}")