import random
import csv
import os

class Auto:
    def __init__(self, marca, modelo, precio_compra):
        self.marca = marca
        self.modelo = modelo
        self.precio_compra = precio_compra
        
        # Estado detallado
        self.partes = {
            "Motor": random.randint(20, 60),
            "Caja": random.randint(30, 70),
            "Frenos": random.randint(40, 80),
            "Chasis": random.randint(10, 60),
            "Ruedas": random.randint(20, 90)
        }

    @staticmethod
    def cargar_modelos_desde_csv():
        modelos = []
        ruta_csv = "datos/modelos_autos.csv"
        
        # Verificamos si existe el archivo para no romper el juego
        if not os.path.exists(ruta_csv):
            # Si no existe, devolvemos una lista de emergencia
            return [("Fiat", "600", 500), ("Ford", "Falcon", 2000)]
            
        with open(ruta_csv, mode='r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                modelos.append((fila['marca'], fila['modelo'], int(fila['precio_base'])))
        return modelos