import random

class Auto:
    def __init__(self, marca, modelo, precio_compra):
        self.marca = marca
        self.modelo = modelo
        self.precio_compra = precio_compra
        # Atributos de estado (0 a 100)
        self.motor = random.randint(20, 60)  # Empiezan rotos para que haya que arreglar
        self.carroceria = random.randint(30, 80)
        self.limpieza = random.randint(10, 50)
        
    def obtener_valor_venta(self):
        promedio_estado = (self.motor + self.carroceria + self.limpieza) / 300
        return int(self.precio_compra * 1.8 * promedio_estado)

    def __str__(self):
        return f"{self.marca} {self.modelo} (M:{self.motor}% C:{self.carroceria}%)"