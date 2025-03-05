import simpy

class Memoria:
    def __init__(self, env, capacidad):
        self.env = env
        self.ram = simpy.Container(env, init=capacidad, capacity=capacidad)

    def solicitar_memoria(self, cantidad, proceso):
        print(f"[{self.env.now}] {proceso} solicita {cantidad} de memoria.")
        yield self.ram.get(cantidad)

    def liberar_memoria(self, cantidad, proceso):
        print(f"[{self.env.now}] {proceso} libera {cantidad} de memoria.")
        yield self.ram.put(cantidad)
