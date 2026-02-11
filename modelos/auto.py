import random
import csv
import os
from core.config import ConfigManager

class Auto:
    def __init__(self, marca, modelo, precio_compra, partes=None, km=None):
        self.marca = marca
        self.modelo = modelo
        self.precio_compra = precio_compra
        self.km = km if km is not None else random.randint(20000, 250000)

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
            "km": self.km,
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
            partes=data.get("partes"),
            km=data.get("km")
        )

    def promedio_estado(self) -> float:
        if not self.partes:
            return 0.0
        return sum(self.partes.values()) / len(self.partes)

    def valor_venta(self) -> int:
        # Estado promedio (0..1)
        estado = self.promedio_estado() / 100.0
        # Factor por kilometraje (degrada hasta 40%)
        km_factor = max(0.6, 1 - (self.km / 400000))
        base = self.precio_compra
        # Nunca vender por menos del 60% del precio base ajustado por km
        return max(0, int(base * max(0.6, (0.6 + 0.4 * estado)) * km_factor))

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