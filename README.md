# Laboratorio 2 - Transformación de lazos, optimización del compilador y jerarquía de memoria
### EL4314 - Arquitectura de Computadoras I
### Escuela de Ingeniería Electrónica
### Tecnológico de Costa Rica

<br/><br/>

## Preámbulo
En este segundo laboratorio, usted experimentará el efecto que tienen la transformación de lazos, las optimizaciones del compilador y la jerarquía de memoria en el rendimiento de un procesador. Para la experimentación se usará un conjunto de aplicaciones de prueba, que incluye un arreglo de dos dimensiones y otras cinco aplicaciones: _matrix multiplication_, _Fast Fourier Transform_ (FFT), _Adaptive Differential Pulse Code Modulation_ (ADPCM), _Advanced Encryption Standard_ (AES) y JPEG, las cuales provienen, mayoritariamente, del _benchmark CHStone_ [1].

Para esta experimentación se utilizará el simulador [*gem5*](https://www.gem5.org). gem5 es una plataforma modular para la investigación de arquitectura de sistemas informáticos, que abarca tanto la arquitectura a nivel de sistema como la microarquitectura del procesador.

## Uso del simulador

Puede ir a la siguiente [wiki](https://github.com/DanielG1010/gem5/wiki) para preparar el simulador de gem5 en su sistema, ya sea en en directamente en su sistema, de forma nativa, usando docker, o mediante una máquina virutal.

Si ya realizó la instalación de gem5, puede comprobar que todo funciona apropiadamente, esto mediante una simulación sencilla de un `hello world` en un sistema x86 con dos niveles de cache, esto en la carpeta `gem5`:

```bash
build/X86/gem5.opt configs/learning_gem5/part1/two_level.py 
```

La cual tiene el siguiente resultado: 

```
gem5 Simulator System.  https://www.gem5.org
gem5 is copyrighted software; use the --copyright option for details.

gem5 version 23.0.1.0
gem5 compiled Sep 25 2023 06:50:43
gem5 started Sep 25 2023 20:31:20
gem5 executing on 36c4aed7f767, pid 15
command line: build/X86/gem5.opt configs/learning_gem5/part1/two_level.py

/root/lab2/gem5/configs/learning_gem5/part1/../../../tests/test-progs/hello/bin/x86/linux/hello
/root/lab2/gem5/configs/learning_gem5/part1/../../../tests/test-progs/hello/bin/x86/linux/hello
Global frequency set at 1000000000000 ticks per second
src/mem/dram_interface.cc:690: warn: DRAM device capacity (8192 Mbytes) does not match the address range assigned (512 Mbytes)
src/base/statistics.hh:279: warn: One of the stats is a legacy stat. Legacy stat is a stat that does not belong to any statistics::Group. Legacy stat is deprecated.
system.remote_gdb: Listening for connections on port 7000
Beginning simulation!
src/sim/simulate.cc:194: info: Entering event queue @ 0.  Starting simulation...
Hello world!
Exiting @ tick 57562000 because exiting with last active thread context
```

El sistema utilizado se muestra en el siguiente driagrama:

![simple_config](simple_config.png)

### Actualizar el nombre del repo en el archivo `gem5-sims.py`

El archivo `gem5-sims.py` puede ser utilizado para realizar varias simulaciones con gem5, con distintas configuraciones de cache para el sistema que se mencionó anteriormente. Sin embargo, es necesario actualizar el nombre del repositorio (o directorio), el cual está definido al inicio del script. También debe actualizar al ruta al repo de gem5, si está usando docker, no debería requerir actualizar esa ruta.

```
import subprocess
import os
import pandas as pd

nombre_repo = "Laboratorio2_2Sem23"
ruta_gem5 = "root/gem5"
```
 

En este script usted puede definir varias configuraciones para su simulacion, los resultados son recabados en un archivo de datos `.csv`, el cual luego puede utilizar para analizar sus resultados.

```python
# List of configurations
cache_configs = [
    {
        "binary": f"{ruta_gem5}/tests/test-progs/hello/bin/x86/linux/hello",
        "l1i_size": '16kB',
        "l1i_assoc": 2,
        "l1d_size": '64kB',
        "l1d_assoc": 2,
        "l2_size": '256kB',
        "l2_assoc": 8,
        "cache_line_size": '64',
        "l1i_rp": 'FIFO',
        "l1d_rp": 'FIFO',
        "l2_rp": 'FIFO'
    },
    {
        "binary": f"{ruta_gem5}/tests/test-progs/hello/bin/x86/linux/hello",
        "l1i_size": '32kB',
        "l1i_assoc": 4,
        "l1d_size": '128kB',
        "l1d_assoc": 4,
        "l2_size": '512kB',
        "l2_assoc": 16,
        "cache_line_size": '128',
        "l1i_rp": 'FIFO',
        "l1d_rp": 'FIFO',
        "l2_rp": 'FIFO'
    },
    # Add more configurations here
]

```

Para probar este script puede hacerlo estando dentro de su contenedor con `python3 gem5-sims.py` o desde su host con `docker exec arqui_gem5 python3 root/lab2/Laboratorio2_2Sem23/gem5/gem5-sims.py`.

Finalmente, si su simulación corrió exitosamente, a la par de `gem5-sims.py` debería generarse un archivo `.cvs`, este contiene los resultados de los experimentos simulados.

El script `plot_variable_vs_experiments.py` es un primer borrador para realizar plots de sus resultados. Puede ejecutarlo con python una vez que se generó el archivo `.csv` (requiere instalar matplotlib y pandas en su host).  

### Configuración de la caché

La configuración base que usted utilizará en este laboratorio es:

|                     | L1 Inst | L1 Data | L2 Unified |
|---------------------|---------|---------|------------|
| Tamaño (KB)         | 8       | 8       | 128        |
| Número de conjuntos | 256     | 256     | 4096       |
| Asociatividad       | 1       | 1       | 1          |
| Línea de cache (B)  | 32      | 32      | 32         |


## Parte 1: Arreglo 2D

Usted empleará un pequeño programa en C que llenará una matriz de dos dimensiones, el mismo se realiza con dos lazos. Para asignar los datos a la matriz, se utiliza la suma del índice del lazo interno y externo actual, i.e., `A[i][j]=i+j`.

```c
    for (i = 0; i < SIZE; i++)
        for (j = 0; j < SIZE; j++)
            A[i][j] = i + j;
```

En esta sección del laboratorio, usted analizará el rendimiento y el consumo de potencia, de este sencillo programa, esto desde dos puntos de vista de:

-   El efecto de las transformaciones de lazo.
-   El efecto de la optmizacion del compilador.

### Transformación de lazos

Usted realizará la transformación de lazos al código de arreglo 2D, utilizando distintas dimensiones para la variable `SIZE`: 16x16, 32x23, 64x64, 128x128. Para este experimento utilice la configuración de la caché presentada anteriomente.

La siguiente lista presenta posibles [transformaciones de lazo](https://tecnube1-my.sharepoint.com/:b:/g/personal/jocastro_itcr_ac_cr/EcnKvkGM_XdFmy0fuHxgxecBVO4s_YqyxplXeqCuH0X5JA?e=88hV0w) a realizar. 

-   Loop permutation
-   Loop unrrolling
-   Loop tiling


Note que se pueden implementar y analizar las transformaciones de manera independente o bien combinadas para cada tamaño del arreglo, además algunas transformaciones, como loop tiling, sólo tienen sentido para tamaños especificos.

Reporte y analice brevemente para cada uno de los tipos de trasformación utilizados. Agregue los archivos generados, a partir de `array.c`, en su repositorio.

### Niveles de optimización del compilador

Para generar archivos binarios ejecutables con distintos niveles de optimización se utilizará el compilador `clang`, el mismo se encuentra en el contenedor de docker, sin embargo es posible utilizarlo desde su sistema host, en unix se instala con `sudo apt update && sudo apt install clang`.

Se muestra en la siguiente tabla como generar los binarios con clang con diferentes niveles de optimización. 

| Nivel de Optimización | Comando Clang | Descripción |
|-----------------------|---------------|-------------|
| Sin optimización      | `clang -O0`   | Compila tu programa sin realizar ninguna optimización en el código. |
| 1  | `clang -O1`   | Realiza optimizaciones básicas que no requieren un tiempo de compilación significativo. |
| 2  | `clang -O2`   | Realiza todas las optimizaciones que no involucran un compromiso de espacio-tiempo. |
| 3  | `clang -O3`   | Realiza todas las optimizaciones de `-O2` y adicionales que pueden aumentar el tamaño del código. |

 Compila el archivo source.c sin optimizaciones y genera el binario 'program':
```
clang -O0 source.c -o program
```

## Parte 2: _Benchmark_

### Optimización del compilador 
Usted ejecutará las 5 aplicaciones con los cuatro diferentes niveles de optimización del compilador y la configuración de la caché base descrita. Reporte y discuta brevemente el efecto de las diferentes optimizaciones. Además de emplear `clang` como compilador, utilice `gcc`. Compare los resultados que obtiene para ambos compiladores empleando el mismo nivel de optimización.


### Configuración de la caché
Considere además el efecto de modificar la jerarquía de memoria, particularmente el nivel L1 de la caché de datos. Proponga al menos 5 diferentes escenarios para esta memoria caché en donde varíe el nivel de asociatividad (y por lo tanto la cantidad de conjuntos), el tamaño de la línea de caché y la estrategia de reemplazo de bloque (LRU, FIFO o random). En todo caso, el tamaño de esta memoria caché no debe cambiar y el nivel de optimización en la compilación debe ser `O0`.

Reporte y discuta brevemente los resultados obtenidos para los diferentes escenarios y para las 5 aplicaciones. Para el caso de las modifiaciones de la caché L1 de datos, utilice la media geométrica para determinar cuál es la mejor configuración tomando en cuenta el rendimiento de la caché y el tiempo de ejecución.

## Mediciones y análisis

Para todas las experimentaciones que realizará en este laboratorio, extraiga los siguientes datos de los reportes generados por el simulador:

-   Número de instrucciones ejecutadas, tiempo de ejecución, CPI/IPC
-   Rendimiento de caché: cache misses, hits, etc.


## Evaluación
Este laboratorio se evaluará con la siguiente rúbrica


| Rubro | % | C | EP | D | NP |
|-------|---|---|----|---|----|
|Transformaciones manuales| 40|   |    |   |    |
|Optimización del compilador| 20|   |    |   |    |
|Experimentación con _benchmark_| 20|   |    |   |    |
|Uso de repositorio|20|   |    |   |    |

C: Completo,
EP: En progreso ($\times 0,8$),
D: Deficiente ($\times 0,5$),
NP: No presenta ($\times 0$)

- El uso del repositorio implica que existan contribuciones de todos los miembros del equipo. El último _commit_ debe registrarte antes de las 23:59 del viernes 13 de octubre de 2023.



# Resultados Parte 1
## Número de instrucciones ejecutadas
...
### tiempo de ejecución
...
### CPI/IPC

# Resultados Parte 2
...
### Rendimiento de caché: cache misses, hits, etc.
...
## Resultados de optimización del compilador.

A partir del arreglo tiling, con un tamaño de 128, se realizaron las pruebas para cada optimización.
Las pruebas fuerons exportadas a un CSV, de este se extrajeron los datos y se realizó un plot o gráfico de cada resultado comparando cada optimización

En los siguientes resultados o hubo diferencia o una gran diferencia como para realizar las comparaciones. En caso quere conocer el resultado, puede ir a la carpeta  Graficas optimizaciones en la ruta: gem5/Part1_optimizations. \
	-CPU.OverallMisses: cpu.data \
	-CPU.OverallMisses: Cpu.inst \
	-L2Cache.overallHits: Tot. \
	-L2cache.overallMisses: CPU.Data \
	-L2cache.overallMisses: CPU.Inst \
	-L2cache.overallMisses: Tot \
	-L2cache.overallMissRate: Tot 
	
Mientras que otros parámetros mostraron resultados mas interesantes:


![simInsts.png](gem5/Part1_optimizations/Graficas_Optimizaciones/simInsts.png)

En el número de instrucciones simuladas, se observa como con la optimización O0, la cantidad de instrucciones se reduce casi a la mitad y se reduce a menos de la mitad con las optimizaciones O2 y O3. El cambio es muy significativo al comparar la simulación sin optimizar con las optimización O1, con una diferencia de 147 851. Las optimización O2 y O3 no tuvieron cambio entre sí. Mientras que O2 y O3 con respecto a la optimización 01, la diferencia de instrucciones fue de 28 672

![simOps.png](gem5/Part1_optimizations/Graficas_Optimizaciones/simOps.png)

Con la cantidad de operaciones realizadas, se mantiene la tendencia, los operaciones se reducen considerablemente al aumentar la optimización, sin embargo, se observa que no hay diferencia entre la optimización O2 y O3 para este caso.
Las diferencia de entre O0 y O1 es de 263 710 (se reduce por encima de la mitad) y la diferencia entre O0 y O2 es de 333 342 (reduce a menos de la mitad).

![system.cpu.cpi.png](gem5/Part1_optimizations/Graficas_Optimizaciones/system.cpu.cpi.png)


![system.cpu.dcache.overallHits::cpu.data.png](gem5/Part1_optimizations/Graficas_Optimizaciones/system.cpu.dcache.overallHits::cpu.data.pngsimInsts.png)

![system.cpu.dcache.overallMissRate::cpu.data.png](gem5/Part1_optimizations/Graficas_Optimizaciones/system.cpu.dcache.overallMissRate::cpu.data.png)

![system.cpu.icache.overallHits::cpu.inst.png](gem5/Part1_optimizations/Graficas_Optimizaciones/system.cpu.icache.overallHits::cpu.inst.png)

![system.cpu.icache.overallMissRate::cpu.inst.png](gem5/Part1_optimizations/Graficas_Optimizaciones/system.cpu.icache.overallMissRate::cpu.inst.png)

![system.cpu.ipc.png](gem5/Part1_optimizations/Graficas_Optimizaciones/system.cpu.ipc.png)

![system.cpu.numCycles.png](gem5/Part1_optimizations/Graficas_Optimizaciones/system.cpu.numCycles.png)







#Resultados Parte 2
