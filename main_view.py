import tkinter as tk
from tkinter import ttk
from threading import Thread
import sys
from PIL import Image, ImageTk
from utils import *
from main import main_optimize
from second_frame import SecondFrame
import tkinter as tk
from tkinter import  ttk
from Parameters import *

class AlgorithmConfigurator:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuration des Paramètres des Algorithmes")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        self.create_styles()
        self.create_variables()
        self.create_widgets()
        self.original_stdout = None  # For restoring stdout after redirecting

    def create_styles(self):
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 12), padding=5)
        self.style.configure("TEntry", font=("Arial", 12), padding=5)
        self.style.configure("TButton", font=("Arial", 12, "bold"), padding=5)
        self.style.configure("TCombobox", font=("Arial", 12), padding=5)
        self.style.configure("TFrame", background="#f3f4f6")
        self.root.configure(bg="#f3f4f6")

    def create_variables(self):
            self.method_choice = tk.StringVar(value=Parameters.get("METHOD"))
            self.instance_name_var = tk.StringVar(value=Parameters.get("INSTANCE_NAME"))
            self.clients_number_var = tk.StringVar(value=Parameters.get("CLIENTS_NUMBER"))
            self.nb_iterations_var = tk.StringVar(value=Parameters.get("AG_NB_ITERATIONS"))
            self.population_size_var = tk.StringVar(value=Parameters.get("AG_POPULATION_SIZE"))
            self.wait_coeff_var = tk.StringVar(value=Parameters.get("AG_WAIT_COEFF"))
            self.delay_coeff_var = tk.StringVar(value=Parameters.get("AG_DELAY_COEFF"))
            self.nb_vehicules_coeff_var = tk.StringVar(value=Parameters.get("AG_NB_VEHICULES_COEFF"))
            self.cx_proba_var = tk.StringVar(value=Parameters.get("AG_CX_PROBA"))
            self.mut_proba_var = tk.StringVar(value=Parameters.get("AG_MUT_PROBA"))
            self.tabou_list_size_var = tk.StringVar(value=Parameters.get("TABOU_LIST_SIZE_MAX"))
            self.tabou_neighbourhood_size_var = tk.StringVar(value=Parameters.get("TABOU_NEIGHBOURHOOD_SIZE"))
            self.tabou_nb_iterations_var = tk.StringVar(value=Parameters.get("TABOU_NB_ITERATIONS"))

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, width=1000, height=700)
        main_frame.place(x=0, y=0)
        self.main_frame = main_frame  # Keep reference for toggling

        # Configuration Frame
        config_frame = ttk.Frame(main_frame, width=600)
        config_frame.place(x=0, y=0)

        # Header
        header_frame = ttk.Frame(config_frame)
        header_frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        ttk.Label(
            header_frame, text="Configuration des Paramètres des Algorithmes",
            font=("Arial", 16, "bold"), anchor="center"
        ).grid(row=0, column=0)

        # Method Selection
        method_frame = ttk.Frame(config_frame)
        method_frame.grid(row=1, column=0, pady=10, padx=20, sticky="w")
        ttk.Label(method_frame, text="Méthode à utiliser :").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Combobox(
            method_frame,
            textvariable=self.method_choice,
            state="readonly",
            values=["Genetic Algorithm", "Genetic Algorithm + Tabou Research"],
            width=40
        ).grid(row=0, column=1, padx=5, sticky="ew", columnspan=2)
        self.method_choice.trace_add("write", self.toggle_tabou_params)

        # General Parameters Frame
        general_frame = self.create_label_frame(config_frame, "Paramètres Généraux", 2)
        self.add_entry(general_frame, "Nom de l'Instance :", self.instance_name_var, 0, 0)
        self.add_entry(general_frame, "Nombre de Clients :", self.clients_number_var, 1, 0)
        self.add_entry(general_frame, "Nombre d'Itérations :", self.nb_iterations_var, 2, 0)
        self.add_entry(general_frame, "Taille de la Population :", self.population_size_var, 3, 0)
        self.add_entry(general_frame, "Coeff. d'Attente :", self.wait_coeff_var, 4, 0)
        self.add_entry(general_frame, "Coeff. de Délai :", self.delay_coeff_var, 5, 0)
        self.add_entry(general_frame, "Coeff. Véhicules :", self.nb_vehicules_coeff_var, 6, 0)
        self.add_entry(general_frame, "Taux de Croisement :", self.cx_proba_var, 7, 0)
        self.add_entry(general_frame, "Taux de Mutation :", self.mut_proba_var, 8, 0)

        # Tabou Parameters Frame
        self.tabou_frame = self.create_label_frame(config_frame, "Paramètres Recherche Tabou", 3)
        self.add_entry(self.tabou_frame, "Taille Max Liste Tabou :", self.tabou_list_size_var, 0, 0)
        self.add_entry(self.tabou_frame, "Taille Voisinage :", self.tabou_neighbourhood_size_var, 1, 0)
        self.add_entry(self.tabou_frame, "Nombre d'Itérations :", self.tabou_nb_iterations_var, 2, 0)

        # "Go to Chromosom detail" Button
        ttk.Button(
            config_frame, text="Détail Chromosome", command=self.show_second_frame
        ).grid(row=4, column=0, pady=20, padx=10, sticky="w")

        # Execute Button
        ttk.Button(
            config_frame, text="Exécuter", command=self.execute_algorithm
        ).grid(row=4, column=0, pady=20, padx=10, sticky="e")
        self.toggle_tabou_params()

        # Image Frame
        self.image_frame = ttk.Frame(main_frame)
        self.image_frame.place(height=400, width=800, x=500, y=0)
        image = Image.open("images/CVRPTW2.png")
        self.photo = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(self.image_frame, image=self.photo, borderwidth=0)
        self.image_label.place(x=50, y=0)

        # Console Log Frame
        self.console_frame = ttk.LabelFrame(main_frame, text="Console Log", padding=(10, 10))
        self.console_frame.place(x=500, y=350, width=480, height=300)
        self.console_text = tk.Text(self.console_frame, wrap="word", state="disabled", font=("Courier", 10))
        self.console_text.pack(fill="both", expand=True)

    def create_label_frame(self, frame, text, row):
        frame = ttk.LabelFrame(frame, text=text, padding=(10, 10))
        frame.grid(row=row, column=0, pady=10, padx=20, sticky="ew")
        return frame

    def show_second_frame(self):
        self.main_frame.place_forget()  # Hide current frame
        SecondFrame(self.root, self.main_frame)  # Create and show second frame

    def add_entry(self, parent, label, variable, row, column):
        ttk.Label(parent, text=label).grid(row=row, column=column, sticky="w")
        ttk.Entry(parent, textvariable=variable).grid(row=row, column=column + 1, sticky="ew")

    def toggle_tabou_params(self, *args):
        if self.method_choice.get() == "Genetic Algorithm + Tabou Research":
            self.tabou_frame.grid()
        else:
            self.tabou_frame.grid_remove()

    def log_to_console(self, text):
        self.console_text.configure(state="normal")
        self.console_text.insert("end", text + "\n")
        self.console_text.configure(state="disabled")
        self.console_text.see("end")  # Auto-scroll to the latest log

    def redirect_stdout(self):
        self.original_stdout = sys.stdout
        sys.stdout = self

    def write(self, text):
        self.log_to_console(text)

    # def flush(self):
    #     pass  # Required for overriding stdout

    def restore_stdout(self):
        if self.original_stdout:
            sys.stdout = self.original_stdout

    def execute_algorithm(self):
        self.redirect_stdout()

        def run_algorithm():
            try:
                parameters = {
                    "INSTANCE_NAME": self.instance_name_var.get(),
                    "CLIENTS_NUMBER": int(self.clients_number_var.get()),
                    "AG_NB_ITERATIONS": int(self.nb_iterations_var.get()),
                    "AG_POPULATION_SIZE": int(self.population_size_var.get()),
                    "AG_WAIT_COEFF": float(self.wait_coeff_var.get()),
                    "AG_DELAY_COEFF": float(self.delay_coeff_var.get()),
                    "AG_NB_VEHICULES_COEFF": float(self.nb_vehicules_coeff_var.get()),
                    "AG_CX_PROBA": float(self.cx_proba_var.get()),
                    "AG_MUT_PROBA": float(self.mut_proba_var.get()),
                    "METHOD": self.method_choice.get(),
                }

                if self.method_choice.get() == "Genetic Algorithm + Tabou Research":
                    parameters.update({
                        "TABOU_LIST_SIZE_MAX": int(self.tabou_list_size_var.get()),
                        "TABOU_NEIGHBOURHOOD_SIZE": int(self.tabou_neighbourhood_size_var.get()),
                        "TABOU_NB_ITERATIONS": int(self.tabou_nb_iterations_var.get()),
                        "TABOU_SEARCH_ON": True,
                    })
                else:
                    parameters["TABOU_SEARCH_ON"] = False

                save_parameters_to_file(parameters)
                print("Starting execution of the algorithm...")
                main_optimize(self.root)  # Call your main algorithm here
                print("Execution is complete.")
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                self.restore_stdout()

        Thread(target=run_algorithm, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmConfigurator(root)
    root.mainloop()
