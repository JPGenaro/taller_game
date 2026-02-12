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
        self.historial = []
        # transient values for UI
        self.last_exp_gained = 0
        self.last_levels_gained = 0

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
            self.historial = []
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
        self.historial = []
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
                self.historial.append(f"Compra: {auto.marca} {auto.modelo} por ${auto.precio_compra}")
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

    def costo_reparacion_total(self, auto) -> int:
        # Costo por punto faltante (balanceado) - valores en core.config
        from core.config import REPAIR_COST_PER_POINT, REPAIR_COST_CAP_MULTIPLIER
        costo_por_punto = float(REPAIR_COST_PER_POINT)
        faltante = sum(100 - v for v in auto.partes.values())
        # Topar respecto al precio de compra mediante multiplicador
        cap = float(REPAIR_COST_CAP_MULTIPLIER)
        return min(int(max(0, faltante) * costo_por_punto), int(auto.precio_compra * cap))

    def reparar_auto_total(self, slot_index: int):
        if slot_index < 0 or slot_index >= len(self.slots):
            return False, "Slot inválido."
        auto = self.slots[slot_index]
        if not auto:
            return False, "No hay auto en ese slot."

        costo = self.costo_reparacion_total(auto)
        if self.dinero < costo:
            return False, f"Dinero insuficiente. Necesitas ${costo}."

        # calcular puntos reparados para dar EXP
        puntos_reparados = sum(100 - v for v in auto.partes.values())

        for parte in auto.partes:
            auto.partes[parte] = 100
        self.dinero -= costo

        # Dar EXP: configurable (ver core.config.DEFAULTS)
        from core.config import EXP_PER_POINT_DIVISOR
        exp_ganada = int(puntos_reparados / max(1, int(EXP_PER_POINT_DIVISOR)))
        self.exp += exp_ganada
        self.last_exp_gained = exp_ganada

        # comprobar subidas de nivel
        niveles_subidos = 0
        info_niveles = []
        while True:
            req = self.xp_para_siguiente()
            if self.exp >= req:
                self.exp -= req
                self.nivel += 1
                niveles_subidos += 1
                info_niveles.append(f"Subiste al nivel {self.nivel}!")
            else:
                break
        self.last_levels_gained = niveles_subidos

        msg = f"Auto reparado por ${costo}. EXP ganada: {exp_ganada}."
        if niveles_subidos:
            msg += " " + " ".join(info_niveles)

        self.historial.append(f"Reparación total: {auto.marca} {auto.modelo} por ${costo} (EXP +{exp_ganada})")
        return True, msg

    def vender_auto(self, slot_index: int):
        if slot_index < 0 or slot_index >= len(self.slots):
            return False, "Slot inválido."
        auto = self.slots[slot_index]
        if not auto:
            return False, "No hay auto en ese slot."

        precio_base = auto.valor_venta()
        # Aumentar significativamente según nivel del jugador
        from core.config import LEVEL_SELL_MULTIPLIER
        nivel_mult = 1.0 + float(LEVEL_SELL_MULTIPLIER) * max(0, getattr(self, 'nivel', 1) - 1)
        precio = int(precio_base * nivel_mult)
        self.dinero += precio
        self.slots[slot_index] = None
        self.historial.append(f"Venta: {auto.marca} {auto.modelo} por ${precio} (base ${precio_base})")
        return True, f"Auto vendido por ${precio}. (base ${precio_base}, nivel x{nivel_mult:.2f})"

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
            "slots": [s.to_dict() if s is not None else None for s in self.slots],
            "historial": self.historial
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
        m.historial = data.get("historial", [])
        m.slots = []
        from modelos.auto import Auto
        for s in slots_data:
            if s is None:
                m.slots.append(None)
            else:
                m.slots.append(Auto.from_dict(s))
        return m