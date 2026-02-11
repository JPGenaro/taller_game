import random
import csv
import os
from core.config import ConfigManager

class Auto:
    def __init__(self, marca, modelo, precio_compra, partes=None):
        self.marca = marca
        self.modelo = modelo
        self.precio_compra = precio_compra

        # Estado detallado
        self.partes = partes or {
            "Motor": random.randint(20, 60),
            "Caja": random.randint(30, 70),
            "Frenos": random.randint(40, 80),
            "Chasis": random.randint(10, 60),
            "Ruedas": random.randint(20, 90),
            "Suspensión": random.randint(20, 80),
            "Dirección": random.randint(30, 80),
            "Escape": random.randint(20, 75),
            "Sistema Eléctrico": random.randint(25, 85),
            "Batería": random.randint(30, 90),
            "Radiador": random.randint(20, 70),
            "Aire Acondicionado": random.randint(30, 85),
            "Luces": random.randint(40, 95),
            "Pintura": random.randint(10, 100),
            "Interior": random.randint(10, 100)
        }

    def to_dict(self) -> dict:
        return {
            "marca": self.marca,
            "modelo": self.modelo,
            "precio_compra": self.precio_compra,
            "partes": self.partes
        }

    @classmethod
    def from_dict(cls, data: dict):
        if not data:
            return None
        return cls(
            data.get("marca", "Desconocida"),
            data.get("modelo", "X"),
            data.get("precio_compra", 0),
            partes=data.get("partes")
        )

    @staticmethod
    def cargar_modelos_desde_csv():
        modelos = []
        ruta_csv = ConfigManager.data_path("modelos_autos.csv")
        
        # Verificamos si existe el archivo para no romper el juego
        if not os.path.exists(ruta_csv):
            # Si no existe, devolvemos una lista de emergencia
            return [("Fiat", "600", 500), ("Ford", "Falcon", 2000)]
            
        with open(ruta_csv, mode='r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            for fila in lector:
                modelos.append((fila['marca'], fila['modelo'], int(fila['precio_base'])))
        return modelos