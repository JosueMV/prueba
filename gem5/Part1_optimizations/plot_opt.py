import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargar los datos desde el archivo CSV en la misma carpeta que el script
data = pd.read_csv('Sim_Res_Opt.csv', usecols=list(range(11, 27)))

# Crear una paleta de colores pastel
colores_pastel = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#c2c2f0', '#ffb3e6', '#c2f0c2']

# Obtener el número de columnas en el DataFrame
num_columns = len(data.columns)

# Crear la carpeta para almacenar las imágenes si no existe
if not os.path.exists('Graficas_Optimizaciones'):
    os.makedirs('Graficas_Optimizaciones')

# Crear un subplot individual para cada columna y exportar la imagen
for i, column in enumerate(data.columns):
    plt.figure()  # Crear una nueva figura para cada subplot
    data[column].plot(kind='bar', figsize=(8, 6), color=colores_pastel[i % len(colores_pastel)])
    plt.title(column)  # Establecer el título como el nombre de la columna
    plt.xlabel('Optimización')
    plt.ylabel('Valores')

    # Agregar etiquetas con valores numéricos en cada barra
    for index, value in enumerate(data[column]):
        plt.text(index, value, str(value), ha='center', va='bottom')

    # Guardar la imagen en la carpeta con el nombre del título
    plt.savefig(os.path.join('Graficas_Optimizaciones', f'{column}.png'))
    plt.close()

# Mostrar todos los subplots
plt.show()
