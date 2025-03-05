import simpy

class Procesador:
    def __init__(self, env, velocidad, num_cpus=1):
        self.env = env
        self.velocidad = velocidad  # Instrucciones que puede ejecutar por unidad de tiempo
        self.cpu = simpy.Resource(env, capacity=num_cpus)

    def ejecutar(self, proceso, instrucciones_restantes):
        with self.cpu.request() as req:
            yield req
            instrucciones_ejecutadas = min(self.velocidad, instrucciones_restantes)
            tiempo_proceso = 1  # Cada ciclo dura una unidad de tiempo

            print(f"[{self.env.now}] {proceso} ejecuta {instrucciones_ejecutadas} instrucciones en el CPU.")
            yield self.env.timeout(tiempo_proceso)

            return instrucciones_restantes - instrucciones_ejecutadas
