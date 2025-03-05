import simpy
import random
import os
from procesador import Procesador
from memoria import Memoria
from proceso import Proceso
import xml.etree.ElementTree as ET

# Parámetros de simulación
RANDOM_SEED = 42
INTERVALO_LLEGADA = [10, 5, 1] # Intervalos
TOTAL_PROCESOS = [25, 50, 100, 150, 200] #Procesos
DIRECTORIO_DATOS = "../datos/"

# Verificar si la carpeta de datos existe
if not os.path.exists(DIRECTORIO_DATOS):
    os.makedirs(DIRECTORIO_DATOS)

# Crear archivos XML vacíos si no existen
def inicializar_archivos_xml():
    for num_procesos in TOTAL_PROCESOS:
        archivo_xml = os.path.join(DIRECTORIO_DATOS, f"procesos{num_procesos}.xml")
        if not os.path.exists(archivo_xml):
            root = ET.Element("simulacion", num_procesos=str(num_procesos))
            tree = ET.ElementTree(root)
            tree.write(archivo_xml)
            print(f"Archivo {archivo_xml} creado.")

# Inicializar los archivos XML si no existen
inicializar_archivos_xml()

def ejecutar_simulacion(num_procesos, intervalo_llegada):
    print(f"\n--- EJECUTANDO SIMULACIÓN PARA {num_procesos} PROCESOS con INTERVALO {intervalo_llegada} ---\n")

    random.seed(RANDOM_SEED)
    env = simpy.Environment()

    cpu = Procesador(env, velocidad=3, num_cpus=1)
    ram = Memoria(env, capacidad=100)

    archivo_xml = os.path.join(DIRECTORIO_DATOS, f"procesos{num_procesos}_intervalo{intervalo_llegada}.xml")

    for i in range(num_procesos):
        Proceso(env, f"Proceso-{i+1}", cpu, ram, archivo_xml)

    env.run()

# Ejecutar simulaciones para cada proceso segun intervalo
for intervalo in INTERVALOS_LLEGADA:
    for procesos in TOTAL_PROCESOS:
        ejecutar_simulacion(procesos, intervalo)

print("\nSimulación completada. Se actualizaron los archivos XML en la carpeta 'datos/'.")
