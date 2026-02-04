class MotorJuego:
    def __init__(self):
        # Datos iniciales
        self.personaje = ""
        self.taller = ""
        self.dinero = 5000
        self.nivel = 1
        self.exp = 0
        self.exp_para_nivel = 100
        
        # Slots del taller: [Elevador, Parking 1, Parking 2]
        self.slots = [None, None, None]

    def agregar_experiencia(self, cantidad):
        self.exp += cantidad
        if self.exp >= self.exp_para_nivel:
            self.nivel += 1
            self.exp -= self.exp_para_nivel
            self.exp_para_nivel = int(self.exp_para_nivel * 1.5)
            return True # Subió de nivel
        return False

    def comprar_auto(self, auto):
        if self.dinero >= auto.precio_compra:
            # Buscar primer slot vacío
            for i in range(len(self.slots)):
                if self.slots[i] is None:
                    self.slots[i] = auto
                    self.dinero -= auto.precio_compra
                    return True, "Auto comprado con éxito."
            return False, "No hay espacio en el taller."
        return False, "No tienes suficiente dinero."

    def reparar_motor(self, slot_index):
        auto = self.slots[slot_index]
        if auto and self.dinero >= 100:
            self.dinero -= 100
            auto.motor = 100
            self.agregar_experiencia(25)
            return True
        return False