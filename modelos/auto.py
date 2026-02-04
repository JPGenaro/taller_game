import random

class Auto:
    def __init__(self, marca, modelo, precio_compra):
        self.marca = marca
        self.modelo = modelo
        self.precio_compra = precio_compra
        
        # El "Estado Mecánico" detallado
        self.partes = {
            "Motor": random.randint(20, 60),
            "Caja de Cambios": random.randint(30, 70),
            "Frenos": random.randint(40, 80),
            "Suspension": random.randint(30, 75),
            "Neumaticos": random.randint(20, 90),
            "Cristales": random.randint(50, 100),
            "Chapa": random.randint(10, 60)
        }

    def obtener_promedio_estado(self):
        # Calcula el promedio de todas las partes
        return sum(self.partes.values()) / len(self.partes)

    def obtener_valor_reventa(self):
        promedio = self.obtener_promedio_estado() / 100
        return int(self.precio_compra * 1.5 * promedio)