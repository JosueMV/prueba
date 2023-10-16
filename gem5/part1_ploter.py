import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos desde el archivo CSV en la misma carpeta que el script
data = pd.read_csv('simulation_results.csv',usecols=list(range(11,27)))
# Crear una paleta de colores pastel
colores_pastel = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#c2c2f0', '#ffb3e6', '#c2f0c2']

# Obtener el número de columnas en el DataFrame
num_columns = len(data.columns)

# Crear un subplot individual para cada columna
for i, column in enumerate(data.columns):
    plt.figure()  # Crear una nueva figura para cada subplot
    data[column].plot(kind='bar', figsize=(8, 6), color=colores_pastel[i % len(colores_pastel)])
    plt.title(column)  # Establecer el título como el nombre de la columna
    plt.xlabel('Experimentos')
    plt.ylabel('Valores')

# Mostrar todos los subplots
plt.show()


