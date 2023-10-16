import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
#from PIL import ImageTk
matplotlib.use('TkAgg') # I add this because the default backend for matplotlib doesn't work in my computer, change it or remove it if you need

# Read the CSV file into a DataFrame
df = pd.read_csv('simulation_results.csv')

# Define the variable to plot
variable_to_plot = 'system.cpu.dcache.overallMissRate::cpu.data'

# Define which experiments to plot
experiments_to_plot = range(1, 8)  # This will plot experiments 1 through 7

# Subset the DataFrame to only include the selected experiments
df_subset = df[df['experiment'].isin(experiments_to_plot)]

# Plot the selected variable against experiment number
plt.figure(figsize=(10, 6))
plt.plot(df_subset['experiment'], df_subset[variable_to_plot], marker='o')

plt.xlabel('Experiment')
plt.ylabel(variable_to_plot)
plt.grid(True)
plt.title(f'{variable_to_plot} by Experiment')
plt.show()

