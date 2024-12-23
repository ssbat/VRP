import tkinter as tk
from tkinter import ttk

from CVRPTW_chromosome import Chromosome
from CVRPTW_info import CVRPTWInfo
from CVRPTW_params import CLIENTS_NUMBER, FULL_INSTANCE_NAME, INSTANCE_NAME
from Parameters import Parameters

AlgorithmConfigurator = None

class SecondFrame:
    def __init__(self, root, previous_frame):
        self.root = root
        self.root.title("Chromosome Info")
        self.root.resizable(False, False)
        self.create_styles()
        self.previous_frame = previous_frame
        self.frame = ttk.Frame(self.root, width=1000, height=700)
        self.frame.place(x=0, y=0)
        

        # Title Label
        ttk.Label(
            self.frame, text="Informations sur chromosome", font=("Arial", 20, "bold")
        ).place(x=350, y=20)  # Adjusted position and size

        # Chromosome Input
        ttk.Label(self.frame, text="Enter Chromosome:", font=("Arial", 13, "bold"), background="#f3f4f6").place(x=50, y=80)
        self.chromosome_input = ttk.Entry(self.frame, font=("Arial", 13))
        self.chromosome_input.place(x=200, y=80, width=650, height=35)
        
        # Info Button
        ttk.Button(
            self.frame, text="Voir", command=self.display_info, style="TButton"
        ).place(x=860, y=80, width=80, height=35)

        # Zone d'affichage des informations
        self.info_frame = ttk.Frame(self.frame, width=900, height=500, relief="ridge", padding=10)
        self.info_frame.place(x=50, y=150)
        
        ttk.Button(
            self.frame, text="Retour", command=self.go_back, style="TButton"
        ).place(x=50, y=670, width=100, height=30)

        # Informations par défaut
        self.labels = {}

    def display_info(self):
        # Retreive chromosome entered by user
        user_input = self.chromosome_input.get().strip()
        try:
            # Remplacer les points par des virgules
            chromosome = list(map(int, user_input.split(',')))  # Convertir en liste d'entiers
        except ValueError:
            self.show_error("Invalid chromosome input! Please enter a list of integers separated by commas.")
            return

        # Initialisation de l'objet Chromosome
        try:
            # Charger l'info CVRPTW
            info = CVRPTWInfo(Parameters.get(FULL_INSTANCE_NAME), Parameters.get(CLIENTS_NUMBER))
            Chromosome.set_info_object(info)

            # Créer un chromosome et calculer ses informations
            c = Chromosome(chromosome=chromosome)
            c.decode_chromosome(c.chromosome)
            c.calculFitness()
        except Exception as e:
            self.show_error(f"Error while processing chromosome: {e}")
            return
        
        # Formater les routes
        formatted_routes = self.format_routes(c.routes)
        
        # Récupérer les informations à afficher
        info = {
            "Fitness": c.fitness,
            "Distance": c.total_travel_distance,
            "Is valid": c.is_valid,
            "Late time penalty": c.lateTimePen,
            "Early time penalty": c.earlyTimePen,
            "Number of vehicles": c.nb_vehicules,
            "Chromosome": str(c.chromosome),
            "Routes": str(formatted_routes),
        }

        # Effacer les anciens labels
        for label in self.labels.values():
            label.destroy()

        # Ajouter les nouvelles informations avec des styles et couleurs
        self.labels = {}
        y_offset = 0
        for key, value in info.items():
            # Étiquette de la clé
            label_key = ttk.Label(
                self.info_frame,
                text=f"{key}:",
                font=("Arial", 13, "bold"),
                anchor="w",
                background="#f3f4f6"
            )
            label_key.place(x=10, y=y_offset, width=200, height=30)
            self.labels[f"{key}_key"] = label_key

            # Valeur de la clé
            if key == "Is valid":
                # Colorer la valeur pour True/False
                color = "green" if value else "red"
                label_value = tk.Label(
                    self.info_frame,
                    text=str(value),
                    font=("Arial", 13),
                    anchor="w",
                    fg=color,
                    bg="#f3f4f6"
                )
            else:
                label_value = ttk.Label(
                    self.info_frame,
                    text=str(value),
                    font=("Arial", 13),
                    anchor="w",
                    background="#f3f4f6"
                )
            if key == "Routes":
                # Supprimer les anciens labels de Routes
                if key in self.labels:
                    self.labels[key].destroy()

                # Créer un Text widget pour afficher les routes proprement
                text_widget = tk.Text(
                    self.info_frame,
                    font=("Arial", 13),
                    wrap="word",
                    height=10,  # Nombre de lignes visibles
                    bg="#f3f4f6",
                    relief="flat"
                )
                text_widget.insert("1.0", str(value))  # Ajouter le contenu des routes
                text_widget.configure(state="disabled")  # Empêcher l'édition
                text_widget.place(x=220, y=y_offset, width=650, height=200)
                self.labels[f"{key}_value"] = text_widget

                y_offset += 220  # Ajuster l'espace pour l'élément suivant
            else:
                label_value.place(x=220, y=y_offset, width=650, height=30)
                self.labels[f"{key}_value"] = label_value

            y_offset += 40  # Ajouter un espacement pour la prochaine ligne
    
    def go_back(self):
        self.frame.place_forget()  # Hide current frame*
        self.previous_frame.place(x=0, y=0)  # Show previous frame
    
    def create_styles(self):
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 12), padding=5)
        self.style.configure("TEntry", font=("Arial", 12), padding=5)
        self.style.configure("TButton", font=("Arial", 12, "bold"), padding=5)
        self.style.configure("TCombobox", font=("Arial", 12), padding=5)
        self.style.configure("TFrame", background="#f3f4f6")
        self.root.configure(bg="#f3f4f6")
        
    def show_error(self, message):
        # Afficher une boîte de dialogue d'erreur
        error_popup = tk.Toplevel(self.root)
        error_popup.title("Error")
        tk.Label(error_popup, text=message, fg="red", font=("Arial", 12, "bold")).pack(pady=10, padx=20)
        ttk.Button(error_popup, text="Fermer", command=error_popup.destroy).pack(pady=5)
    
    def format_routes(self, routes):
        """
        Formate les routes pour un affichage sur plusieurs lignes.
        """
        formatted_routes = "\n".join([f"Route {i+1}: {route}" for i, route in enumerate(routes)])
        return formatted_routes

if __name__ == "__main__":
    from main_view import AlgorithmConfigurator
    root = tk.Tk()
    app = SecondFrame(root, AlgorithmConfigurator(root))
    root.mainloop()