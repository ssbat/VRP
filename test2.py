from main import main_optimize
from utils import save_parameters_to_file

import numpy as np
import itertools
import matplotlib.pyplot as plt

from CVRPTW import CVRPTW
from CVRPTW_info import CVRPTWInfo
from Parameters import Parameters
from CVRPTW_params import *
from Results.ResultsManager import ResultsManager

steps = 2

# Define the ranges for the coefficients
c1_values = np.linspace(0.0, 2.0, steps)  # For example, 5 steps: 0.0, 0.25, 0.5, 0.75, 1.0
c2_values = np.linspace(9, 15.0, steps)
c3_values = np.linspace(0.0, 200.0, steps)


def run_ga(c1, c2, c3, num_runs=3):
    parameters = {
    "INSTANCE_NAME": "R101",
    "CLIENTS_NUMBER": 25,
    "AG_NB_ITERATIONS": 10000,
    "AG_POPULATION_SIZE": 300,
    "AG_WAIT_COEFF": float(c1),
    "AG_DELAY_COEFF": float(c2),
    "AG_NB_VEHICULES_COEFF": float(c3),
    "AG_CX_PROBA": 0.8,
    "AG_MUT_PROBA": 0.5,
    "METHOD": "Genetic Algorithm",
    "TABOU_LIST_SIZE_MAX": 10,
    "TABOU_NEIGHBOURHOOD_SIZE": 200,
    "TABOU_NB_ITERATIONS": 3000,
    "TABOU_SEARCH_ON": False
    }
    save_parameters_to_file(parameters)
    
    info = CVRPTWInfo(Parameters.get(FULL_INSTANCE_NAME),Parameters.get(CLIENTS_NUMBER))  
    results = []
    for _ in range(num_runs):
        ag = CVRPTW(info)
        ag.optimize()
        best = ag.population.best_solution
        results.append((best.total_travel_distance, best.is_valid))
        
    return results

# To store results
data = []

# Iterate over all combinations of c1, c2, c3
for c1, c2, c3 in itertools.product(c1_values, c2_values, c3_values):
    results = run_ga(c1, c2, c3, num_runs=5)  # run multiple times for better average
    # Filter valid solutions
    valid_fitnesses = [r[0] for r in results if r[1]]
    if len(valid_fitnesses) > 0:
        avg_distance = np.mean(valid_fitnesses)
        max_distance = np.max(valid_fitnesses)
    else:
        # If no valid solutions, skip or mark as None
        continue
    
    # Store result
    data.append((c1, c2, c3, avg_distance, max_distance))

# Convert to numpy array for easier manipulation
data = np.array(data, dtype=[('c1', float), ('c2', float), ('c3', float), 
                             ('avg_distance', float), ('max_distance', float)])

# Example: Visualize the average fitness in 3D
# You could also pick a slice and visualize in 2D.
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Choose what you want to plot. Here, let's plot avg_distance.
x = data['c1']
y = data['c2']
z = data['c3']
c = data['avg_distance']

# Create a scatter plot in 3D
p = ax.scatter(x, y, z, c=c, cmap='viridis', s=50)
ax.set_xlabel('C1')
ax.set_ylabel('C2')
ax.set_zlabel('C3')
ax.set_title('Fitness by coefficient combinations (only valid solutions)')
fig.colorbar(p, ax=ax, label='Average Distance')

plt.tight_layout()
plt.show()

# If you prefer 2D slices, for example fixing c3 and looking at c1 vs c2:
# You could filter data for a specific c3 and plot a heatmap.
# Example:
fixed_c3 = 0.5
subdata = data[np.isclose(data['c3'], fixed_c3)]
if len(subdata) > 0:
    # build a grid for visualization
    c1_uniq = np.unique(subdata['c1'])
    c2_uniq = np.unique(subdata['c2'])
    fitness_grid = np.zeros((len(c1_uniq), len(c2_uniq)))
    for i, cc1 in enumerate(c1_uniq):
        for j, cc2 in enumerate(c2_uniq):
            val = subdata[(subdata['c1'] == cc1) & (subdata['c2'] == cc2)]['avg_distance']
            if len(val) > 0:
                fitness_grid[i, j] = val[0]
            else:
                fitness_grid[i, j] = np.nan
    
    plt.figure(figsize=(8,6))
    plt.imshow(fitness_grid, origin='lower', 
               extent=[c1_uniq.min(), c1_uniq.max(), c2_uniq.min(), c2_uniq.max()],
               aspect='auto', cmap='viridis')
    plt.xlabel('C1')
    plt.ylabel('C2')
    plt.title(f'Average Fitness Heatmap at C3={fixed_c3}')
    plt.colorbar(label='Average Distance')
    plt.show()