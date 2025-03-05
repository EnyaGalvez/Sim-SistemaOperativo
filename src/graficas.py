import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# Rutas de archivos
DIRECTORIO_DATOS = "../data/"
DIRECTORIO_REPORTES = "../reportes/"

# Parámetros de simulación
TOTAL_PROCESOS = [25, 50, 100, 150, 200]
INTERVALOS_LLEGADA = [10, 5, 1]

# Verificar si la carpeta de reportes existe, si no, crearla
if not os.path.exists(DIRECTORIO_REPORTES):
    os.makedirs(DIRECTORIO_REPORTES)


def extraer_tiempos_finalizacion(archivo_xml):
    """ Lee un archivo XML y extrae los tiempos de finalización (TERMINATED) de cada proceso. """
    tiempos_finalizacion = []

    if not os.path.exists(archivo_xml) or os.path.getsize(archivo_xml) == 0:
        print(f"⚠️ Archivo {archivo_xml} no encontrado o vacío. Se omitirá.")
        return tiempos_finalizacion

    try:
        tree = ET.parse(archivo_xml)
        root = tree.getroot()

        for proceso in root.findall("proceso"):
            estado_terminado = proceso.find("estado[@nombre='TERMINATED']")
            if estado_terminado is not None:
                tiempo = float(estado_terminado.get("tiempo"))
                tiempos_finalizacion.append(tiempo)

    except ET.ParseError:
        print(f"⚠️ Error al leer el archivo {archivo_xml}. Puede estar corrupto.")

    return tiempos_finalizacion


def graficar_resultados():
    """ Genera gráficos de tiempo de finalización para cada combinación de número de procesos e intervalo de llegada. """
    for intervalo in INTERVALOS_LLEGADA:
        for num_procesos in TOTAL_PROCESOS:
            archivo_xml = os.path.join(DIRECTORIO_DATOS, f"procesos{num_procesos}_intervalo{intervalo}.xml")
            tiempos = extraer_tiempos_finalizacion(archivo_xml)

            if not tiempos:
                continue  # Si no hay datos en el XML, pasar al siguiente

            # Generar la gráfica
            plt.figure(figsize=(10, 5))
            plt.hist(tiempos, bins=10, color="blue", alpha=0.7, edgecolor="black")
            plt.xlabel("Tiempo de finalización")
            plt.ylabel("Cantidad de procesos")
            plt.title(f"Distribución de Tiempos de Finalización\n{num_procesos} Procesos, Intervalo {intervalo}")
            plt.grid(True)

            # Guardar la gráfica en reportes
            nombre_grafico = f"grafica_procesos{num_procesos}_intervalo{intervalo}.png"
            ruta_grafico = os.path.join(DIRECTORIO_REPORTES, nombre_grafico)
            plt.savefig(ruta_grafico)
            plt.show()

            print(f"✅ Gráfico guardado en {ruta_grafico}")


# Ejecutar la función para generar los gráficos
if __name__ == "__main__":
    graficar_resultados()
