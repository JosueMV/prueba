# Usar la imagen base con todas las dependencias
FROM gcr.io/gem5-test/ubuntu-22.04_all-dependencies:v22-1

# Definir el directorio de trabajo
WORKDIR /root

# Actualizar los paquetes del sistema e instalar Clang y pandas
RUN apt-get update && apt-get install -y clang && pip3 install pandas && cd && git clone https://github.com/DanielG1010/gem5.git

# Comando por defecto al iniciar el contenedor
CMD ["/bin/bash"]

