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

steps = 4

# Define the ranges for the coefficients
c1_values = np.linspace(0.0, 2.0, steps)
c2_values = np.linspace(0, 10, steps)
c3_values = np.linspace(0.0, 200.0, steps)

def run_ga(c1, c2, c3, num_runs=3):
    parameters = {
        "INSTANCE_NAME": "R101",
        "CLIENTS_NUMBER": 25,
        "AG_NB_ITERATIONS": 100000,
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
    
    info = CVRPTWInfo(Parameters.get(FULL_INSTANCE_NAME), Parameters.get(CLIENTS_NUMBER))  
    results = []
    for _ in range(num_runs):
        ag = CVRPTW(info)
        ag.optimize()
        best = ag.population.best_solution
        results.append((best.total_travel_distance, best.is_valid))
        
    return results

# To store results
data = []
invalid_data = []

# Iterate over all combinations of c1, c2, c3
for c1, c2, c3 in itertools.product(c1_values, c2_values, c3_values):
    results = run_ga(c1, c2, c3, num_runs=1)
    valid_fitnesses = [r[0] for r in results if r[1]]
    
    if len(valid_fitnesses) > 0:
        avg_distance = np.mean(valid_fitnesses)
        max_distance = np.max(valid_fitnesses)
        data.append((c1, c2, c3, avg_distance, max_distance))
    else:
        invalid_data.append((c1, c2, c3))

# Convert valid data to numpy array
data = np.array(data, dtype=[('c1', float), ('c2', float), ('c3', float), 
                             ('avg_distance', float), ('max_distance', float)])

# Convert invalid data to numpy array
invalid_data = np.array(invalid_data, dtype=[('c1', float), ('c2', float), ('c3', float)])

# 3D Scatter Plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot valid solutions
x_valid = data['c1']
y_valid = data['c2']
z_valid = data['c3']
c_valid = data['avg_distance']

p_valid = ax.scatter(x_valid, y_valid, z_valid, c=c_valid, cmap='viridis', s=50, label='Valid Solutions')

# Plot invalid solutions
if len(invalid_data) > 0:
    x_invalid = invalid_data['c1']
    y_invalid = invalid_data['c2']
    z_invalid = invalid_data['c3']
    ax.scatter(x_invalid, y_invalid, z_invalid, c='red', marker='x', s=50, label='Invalid Solutions')

ax.set_xlabel('C1')
ax.set_ylabel('C2')
ax.set_zlabel('C3')
ax.set_title('Fitness by Coefficient Combinations')
fig.colorbar(p_valid, ax=ax, label='Average Distance')

ax.legend()
plt.tight_layout()
plt.show()

# 2D Heatmap with Invalid Points
fixed_c3 = 0.5
subdata = data[np.isclose(data['c3'], fixed_c3)]
invalid_points = [(c1, c2) for c1, c2, c3 in invalid_data if np.isclose(c3, fixed_c3)]

if len(subdata) > 0:
    # Build a grid for valid solutions
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
    
    plt.figure(figsize=(8, 6))
    plt.imshow(fitness_grid, origin='lower', 
               extent=[c1_uniq.min(), c1_uniq.max(), c2_uniq.min(), c2_uniq.max()],
               aspect='auto', cmap='viridis')
    plt.xlabel('C1')
    plt.ylabel('C2')
    plt.title(f'Average Fitness Heatmap at C3={fixed_c3}')
    plt.colorbar(label='Average Distance')
    
    # Overlay invalid points
    if len(invalid_points) > 0:
        invalid_points = np.array(invalid_points)
        plt.scatter(invalid_points[:, 0], invalid_points[:, 1], c='red', marker='x', label='Invalid Solutions')

    plt.legend()
    plt.show()
