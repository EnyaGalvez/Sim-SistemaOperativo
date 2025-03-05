import simpy
import random
import xml.etree.ElementTree as ET
import os

class Proceso:
    def __init__(self, env, nombre, cpu, ram, archivo_xml):
        self.env = env
        self.nombre = nombre
        self.cpu = cpu
        self.ram = ram
        self.instrucciones = random.randint(1, 10)
        self.memoria = random.randint(1, 10)
        self.archivo_xml = archivo_xml

        # Verificar si el archivo XML existe y tiene contenido válido
        self.inicializar_xml()

        # Registrar evento en XML
        self.registrar_evento("NEW", self.env.now)

        env.process(self.ejecutar())

    def inicializar_xml(self): #Crea un XML vacio con la estructura inicial si el archivo no existe o está vacío
        if not os.path.exists(self.archivo_xml) or os.path.getsize(self.archivo_xml) == 0:
            root = ET.Element("simulacion")
            tree = ET.ElementTree(root)
            tree.write(self.archivo_xml)
            print(f"Archivo XML {self.archivo_xml} inicializado correctamente.")

    def registrar_evento(self, estado, tiempo): #Registra un evento dentro del XML correspondiente
        try:
            tree = ET.parse(self.archivo_xml)
            root = tree.getroot()

            proceso_node = ET.SubElement(root, "proceso", nombre=self.nombre)
            ET.SubElement(proceso_node, "estado", nombre=estado, tiempo=str(tiempo))

            tree.write(self.archivo_xml)
            print(f"[{tiempo}] {self.nombre} cambia a estado {estado} (registrado en {self.archivo_xml}).")

        except ET.ParseError:
            print(f"Error: El archivo XML {self.archivo_xml} está corrupto. Reinicializando...")
            self.inicializar_xml()

    def ejecutar(self): # Simula la ejecucion del proceso dentro del sistema operativo
        yield self.env.process(self.ram.solicitar_memoria(self.memoria, self.nombre))
        self.registrar_evento("READY", self.env.now)

        while self.instrucciones > 0:
            self.registrar_evento("RUNNING", self.env.now)
            self.instrucciones = yield self.env.process(self.cpu.ejecutar(self.nombre, self.instrucciones))

            decision = random.randint(1, 21)
            if self.instrucciones <= 0:
                self.registrar_evento("TERMINATED", self.env.now)
                yield self.env.process(self.ram.liberar_memoria(self.memoria, self.nombre))
                break
            elif decision == 1:
                self.registrar_evento("WAITING", self.env.now)
                yield self.env.timeout(1)
                self.registrar_evento("READY", self.env.now)
            else:
                self.registrar_evento("READY", self.env.now)