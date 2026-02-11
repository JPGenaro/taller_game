import json
import datetime

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
        Carga datos desde distintas formas que puede devolver la Database:
        - dict (json guardado)
        - tupla/list (compatibilidad con obtener_partida)
        - None (inicializa valores por defecto)
        """
        # Valores por defecto
        if not datos:
            self.personaje = ""
            self.taller = ""
            self.dinero = 5000
            self.nivel = 1
            self.exp = 0
            self.slots = [None, None, None]
            print("Datos cargados: (vacío)")
            return

        # Si nos pasan un dict (p. ej. json guardado), delegamos a from_dict
        if isinstance(datos, dict):
            m = Motor.from_dict(datos) if hasattr(Motor, "from_dict") else None
            if m:
                self.personaje = m.personaje
                self.taller = m.taller
                self.dinero = m.dinero
                self.nivel = m.nivel
                self.exp = m.exp
                self.slots = m.slots
                print(f"Datos cargados: {self.personaje} - ${self.dinero}")
                return

        # Compatibilidad con tuplas/arrays antiguas devueltas por obtener_partida
        if isinstance(datos, (list, tuple)):
            # esperar formatos variables; asignar con checks de longitud
            try:
                self.personaje = datos[2] if len(datos) > 2 else getattr(self, "personaje", "")
                self.taller = datos[3] if len(datos) > 3 else getattr(self, "taller", "")
                self.nivel = int(datos[4]) if len(datos) > 4 else getattr(self, "nivel", 1)
                # exp y dinero pueden no estar presentes en versiones antiguas
                self.exp = int(datos[5]) if len(datos) > 5 else getattr(self, "exp", 0)
                self.dinero = int(datos[6]) if len(datos) > 6 else getattr(self, "dinero", 5000)
            except Exception:
                # en caso de formato inesperado, mantener valores actuales/por defecto
                self.personaje = getattr(self, "personaje", "")
                self.taller = getattr(self, "taller", "")
                self.dinero = getattr(self, "dinero", 5000)
                self.nivel = getattr(self, "nivel", 1)
                self.exp = getattr(self, "exp", 0)

            # Asegurar slots inicializados
            if not hasattr(self, "slots") or self.slots is None:
                self.slots = [None, None, None]
            print(f"Datos cargados: {self.personaje} - ${self.dinero}")
            return

        # Si llega algo inesperado, inicializar por seguridad
        self.personaje = ""
        self.taller = ""
        self.dinero = 5000
        self.nivel = 1
        self.exp = 0
        self.slots = [None, None, None]
        print("Datos cargados: formato desconocido, se usaron valores por defecto.")

    def comprar_auto(self, auto):
        """
        Intenta comprar un auto:
        - Verifica dinero
        - Busca primer slot vacío y coloca el auto
        - Deduce el dinero y devuelve (True, mensaje) o (False, mensaje)
        """
        if self.dinero < auto.precio_compra:
            return False, f"No tienes suficiente dinero (${self.dinero}) para comprar este auto (${auto.precio_compra})."

        # Buscar primer slot vacío
        for idx, slot in enumerate(self.slots):
            if slot is None:
                self.slots[idx] = auto
                self.dinero -= auto.precio_compra
                return True, f"Auto comprado y colocado en el slot {idx+1}."

        return False, "No hay espacio en el taller (todos los slots están ocupados)."

    def xp_para_siguiente(self) -> int:
        """Devuelve la XP necesaria para subir del nivel actual al siguiente."""
        # Fórmula simple: 100 * nivel (puedes ajustar a exponencial si querés)
        return 100 * max(1, getattr(self, "nivel", 1))
    
    def progreso_nivel(self):
        """Devuelve (xp_actual, xp_requerida, xp_faltante, porcentaje)."""
        xp_actual = getattr(self, "exp", 0)
        xp_req = self.xp_para_siguiente()
        xp_faltante = max(0, xp_req - xp_actual)
        porcentaje = min(1.0, xp_actual / xp_req) if xp_req > 0 else 1.0
        return xp_actual, xp_req, xp_faltante, porcentaje

    # Serialización para guardar/cargar
    def to_dict(self) -> dict:
        """Convierte el estado del Motor a un dict serializable."""
        return {
            "personaje": self.personaje,
            "taller": self.taller,
            "dinero": self.dinero,
            "nivel": self.nivel,
            "exp": self.exp,
            # Guardamos los autos en slots como dicts (o None)
            "slots": [s.to_dict() if s is not None else None for s in self.slots]
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Crea un Motor a partir de un dict (útil al cargar desde DB)."""
        m = cls()
        m.personaje = data.get("personaje", "")
        m.taller = data.get("taller", "")
        m.dinero = data.get("dinero", 0)
        m.nivel = data.get("nivel", 1)
        m.exp = data.get("exp", 0)
        slots_data = data.get("slots", [None, None, None])
        m.slots = []
        from modelos.auto import Auto
        for s in slots_data:
            if s is None:
                m.slots.append(None)
            else:
                m.slots.append(Auto.from_dict(s))
        return m