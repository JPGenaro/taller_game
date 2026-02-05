class Motor:
    def __init__(self):
        self.personaje = ""
        self.taller = ""
        self.dinero = 5000
        self.nivel = 1
        self.exp = 0
        self.slots = [None, None, None] # Lista para los autos en el taller

    def cargar_datos(self, datos):
        """
        Toma la tupla de la DB y actualiza los atributos del motor.
        Asumiendo el orden: (id, slot_id, personaje, dinero, nivel, exp, taller)
        """
        if datos:
            # Los índices dependen de cómo creaste tu tabla en database.py
            self.personaje = datos[2]
            self.dinero = datos[3]
            self.nivel = datos[4]
            self.exp = datos[5]
            self.taller = datos[6] if len(datos) > 6 else "Mi Taller"
            
            # Resetear slots al cargar (podrías cargar autos aquí en el futuro)
            self.slots = [None, None, None]
            print(f"Datos cargados: {self.personaje} - ${self.dinero}")