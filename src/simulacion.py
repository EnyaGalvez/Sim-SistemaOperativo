import simpy
import random
import csv
import matplotlib.pyplot as plt

from memoria import Memoria
from procesador import Procesador
from proceso import Proceso

# Parametros de simulacion
RANDOM_SEED = 42
INTERVAL = 10
TOTAL_PROCESS = [25, 50, 100, 150, 200]

