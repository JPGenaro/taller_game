import random

class Auto:
    def __init__(self, marca, modelo, precio_compra):
        self.marca = marca
        self.modelo = modelo
        self.precio_compra = precio_compra
        # Estados aleatorios para que el juego sea un reto
        self.motor = random.randint(10, 50)
        self.carroceria = random.randint(20, 70)
        self.limpieza = random.randint(5, 40)
        
    def obtener_valor_venta(self):
        # Un auto perfecto vale el doble de su compra
        estado_general = (self.motor + self.carroceria + self.limpieza) / 300
        return int(self.precio_compra * 2 * estado_general)

    def __str__(self):
        return f"{self.marca} {self.modelo} (M:{self.motor}% C:{self.carroceria}%)"