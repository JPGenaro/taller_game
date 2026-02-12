import random
import csv
import os
from core.config import ConfigManager

class Auto:
    def __init__(self, marca, modelo, precio_compra, partes=None, km=None, anio=None):
        self.marca = marca
        self.modelo = modelo
        self.precio_compra = precio_compra
        # Kilometraje
        self.km = km if km is not None else random.randint(20000, 250000)
        # Año de producción (si no se provee, elegir aleatorio entre 1990 y 2019)
        import datetime
        self.anio = anio if anio is not None else random.randint(1990, min(2019, datetime.datetime.now().year))

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
            "anio": self.anio,
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
            km=data.get("km"),
            anio=data.get("anio")
        )

    def promedio_estado(self) -> float:
        if not self.partes:
            return 0.0
        return sum(self.partes.values()) / len(self.partes)

    def valor_venta(self) -> int:
        # Valor cuando el jugador vende el auto al mercado
        # Estado promedio (0..1)
        estado = self.promedio_estado() / 100.0
        # Factor por kilometraje: autos con menos km valen más (bonus hasta +0.5)
        km_discount = max(0, (100000 - self.km) / 200000.0)  # 0..0.5
        km_multiplier = 1.0 + km_discount
        base = self.precio_compra
        # factor base según estado, desde 0.6 (muy malo) hasta 1.4 (muy bueno)
        base_factor = 0.6 + 0.8 * estado

        # Factor por año de producción: autos más nuevos valen más.
        try:
            import datetime as _dt
            current = _dt.datetime.now().year
            age = max(0, current - int(self.anio))
            # cada año reduce ~2% del multiplicador con límite
            year_factor = max(0.6, 1.0 - 0.02 * age)
            # convertir a multiplicador donde autos nuevos (anio reciente) conservan ~1.0
            # y autos viejos bajan hasta 0.6; invertimos para que año más nuevo aumente
            year_multiplier = 1.0 / year_factor
        except Exception:
            year_multiplier = 1.0

        valor = int(base * base_factor * km_multiplier * year_multiplier)
        return max(0, valor)

    def market_price(self) -> int:
        """Precio al que el mercado oferta este auto al jugador (venta del mercado).
        Este precio es mayor que el valor de venta al mercado y tiene un pequeño markup y variación.
        """
        import random
        estado = self.promedio_estado() / 100.0
        # km penaliza el precio de venta del mercado ligeramente
        km_penalty = max(0.5, 1 - (self.km / 400000.0))
        base = self.precio_compra
        # markup según estado
        price = base * (0.8 + 0.7 * estado) * km_penalty

        # aplicar influencia del año (autos recientes incrementan el precio de mercado)
        try:
            import datetime as _dt
            current = _dt.datetime.now().year
            age = max(0, current - int(self.anio))
            year_adj = max(0.7, 1.0 - 0.015 * age)  # penaliza ligeramente por antigüedad
            price = price * year_adj
        except Exception:
            pass
        # mercado aplica markup y algo de variación
        factor = random.uniform(0.9, 1.25)
        final = int(max(1, price * factor))
        return final

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
                try:
                    anio = int(fila.get('anio') or 0) if 'anio' in fila else None
                except Exception:
                    anio = None
                precio = int(fila.get('precio_base') or fila.get('precio', 0)) if ('precio_base' in fila or 'precio' in fila) else 0
                modelos.append((fila['marca'], fila['modelo'], precio, anio))
        return modelos