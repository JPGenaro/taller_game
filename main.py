import customtkinter as ctk
from core.database import Database
from core.motor import Motor
from modelos.auto import Auto
from interfaz.mercado import VentanaMercado
from interfaz.componentes import SlotTaller
from interfaz.opciones import VentanaOpciones
from interfaz.pausa import MenuPausa  # Asegúrate de tener este archivo creado

class Aplicacion:
    def __init__(self):
        # 1. Configuración de Ventana
        self.root = ctk.CTk()
        self.root.title("Garage Tycoon v0.3")
        self.root.geometry("1000x700")
        
        # 2. Inicialización de Núcleo (Core)
        self.db = Database()
        self.motor = Motor()
        
        # 3. Estado de la sesión actual
        self.slot_actual = None
        
        # Iniciar juego
        self.mostrar_menu_inicio()
        self.root.mainloop()

    # --- UTILIDADES ---
    def limpiar_pantalla(self):
        """Elimina todos los widgets de la ventana principal."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- FLUJO DE NAVEGACIÓN (Pantallas Principales) ---

    def mostrar_menu_inicio(self):
        """Pantalla de título y menú principal."""
        self.limpiar_pantalla()
        
        ctk.CTkLabel(self.root, text="GARAGE TYCOON", font=("Arial Bold", 50)).pack(pady=40)
        
        btn_container = ctk.CTkFrame(self.root, fg_color="transparent")
        btn_container.pack(expand=True)

        # Botones Principales
        ctk.CTkButton(btn_container, text="NUEVA PARTIDA", width=250, height=45,
                      command=lambda: self.mostrar_seleccion_slot("nueva")).pack(pady=10)
        
        # Cargar partida (solo si hay datos)
        estado_cargar = "normal" if self.db.hay_partidas_guardadas() else "disabled"
        ctk.CTkButton(btn_container, text="CARGAR PARTIDA", width=250, height=45, state=estado_cargar,
                      command=lambda: self.mostrar_seleccion_slot("cargar")).pack(pady=10)
        
        ctk.CTkButton(btn_container, text="OPCIONES", width=250, height=45,
                      command=self.mostrar_opciones).pack(pady=10)
        
        ctk.CTkButton(btn_container, text="CRÉDITOS", width=250, height=45,
                      command=self.mostrar_creditos).pack(pady=10)
        
        ctk.CTkButton(btn_container, text="SALIR", width=250, height=45, fg_color="#A83232",
                      command=self.root.quit).pack(pady=10)

    def mostrar_seleccion_slot(self, modo: str):
        """Pantalla de selección entre los 3 slots de guardado."""
        self.limpiar_pantalla()
        ctk.CTkLabel(self.root, text=f"SELECCIONAR SLOT ({modo.upper()})", font=("Arial", 25)).pack(pady=30)

        for i in range(1, 4):
            datos = self.db.obtener_partida(i)
            frame = ctk.CTkFrame(self.root)
            frame.pack(fill="x", padx=50, pady=10)

            info = f"Slot {i}: {datos[2]} (Nivel {datos[4]})" if datos else f"Slot {i}: VACÍO"
            ctk.CTkLabel(frame, text=info).pack(side="left", padx=20, pady=15)

            # Lógica de botón según modo
            btn_text = "ELEGIR" if modo == "nueva" else "CARGAR"
            btn_state = "normal" if (modo == "nueva" or datos) else "disabled"
            
            ctk.CTkButton(frame, text=btn_text, state=btn_state,
                          command=lambda s=i: self.inicializar_partida(s, modo)).pack(side="right", padx=20)

        ctk.CTkButton(self.root, text="VOLVER", command=self.mostrar_menu_inicio).pack(pady=20)

    def mostrar_creditos(self):
        """Pantalla de agradecimientos y autoría."""
        self.limpiar_pantalla()
        
        ctk.CTkLabel(self.root, text="CRÉDITOS", font=("Arial Bold", 40)).pack(pady=40)
        
        info_frame = ctk.CTkFrame(self.root)
        info_frame.pack(padx=50, pady=20, fill="both", expand=True)
        
        texto_creditos = (
            "DESARROLLADO POR:\nJP Genaro\n\n"
            "TECNOLOGÍAS:\nPython 3.12 & CustomTkinter\n\n"
            "AGRADECIMIENTOS:\nA la comunidad de dev de Pop!_OS\ny a vos por jugar."
        )
        
        ctk.CTkLabel(info_frame, text=texto_creditos, font=("Arial", 18)).pack(expand=True)
        
        ctk.CTkButton(self.root, text="VOLVER AL MENÚ", width=200,
                      command=self.mostrar_menu_inicio).pack(pady=30)
        
    # --- LÓGICA DE PARTIDA ---

    def inicializar_partida(self, slot_id, modo):
        """Configura el motor y la base de datos para la sesión."""
        self.slot_actual = slot_id
        if modo == "nueva":
            self.mostrar_registro()
        else:
            datos = self.db.obtener_partida(slot_id)
            self.motor.cargar_datos(datos) # Asegúrate de tener este método en motor.py
            self.mostrar_taller()

    def mostrar_registro(self):
        """Pantalla para nombrar personaje y taller al crear partida nueva."""
        self.limpiar_pantalla()
        ctk.CTkLabel(self.root, text="DATOS DEL PROPIETARIO", font=("Arial", 25)).pack(pady=30)
        
        ent_nombre = ctk.CTkEntry(self.root, placeholder_text="Tu Nombre", width=300)
        ent_nombre.pack(pady=10)
        ent_taller = ctk.CTkEntry(self.root, placeholder_text="Nombre del Taller", width=300)
        ent_taller.pack(pady=10)

        def confirmar():
            if ent_nombre.get() and ent_taller.get():
                self.motor.personaje = ent_nombre.get()
                self.motor.taller = ent_taller.get()
                self.db.guardar(self.slot_actual, self.motor)
                self.mostrar_taller()

        ctk.CTkButton(self.root, text="COMENZAR AVENTURA", command=confirmar).pack(pady=30)

    def mostrar_taller(self):
        """Interfaz principal del taller de reparaciones (Elevadores y Parking)."""
        self.limpiar_pantalla()
        
        # --- HEADER (Info del Jugador) ---
        header = ctk.CTkFrame(self.root, height=60)
        header.pack(fill="x", side="top", padx=10, pady=5)
        
        # Mostrar nombre de personaje y nombre del taller juntos a la izquierda
        nombre_personaje = getattr(self.motor, "personaje", "Jugador")
        nombre_taller = getattr(self.motor, "taller", "Mi Taller")
        ctk.CTkLabel(header, text=f"👤 {nombre_personaje}   |   🏠 {nombre_taller}", font=("Arial", 16, "bold")).pack(side="left", padx=20)
        
        ctk.CTkLabel(header, text=f"💰 ${self.motor.dinero}", text_color="#2ecc71", font=("Arial", 16, "bold")).pack(side="right", padx=20)
        
        # Botón de Pausa (engranaje)
        ctk.CTkButton(header, text="⚙️", width=40, command=self.abrir_pausa).pack(side="right", padx=10)

        # --- INFO DE NIVEL / XP (mantener el resto igual; agregado aquí) ---
        try:
            xp_actual, xp_req, xp_faltante, porcentaje = self.motor.progreso_nivel()
        except Exception:
            xp_actual, xp_req, xp_faltante, porcentaje = 0, 100, 100, 0.0

        info_nivel = ctk.CTkFrame(self.root, height=40)
        info_nivel.pack(fill="x", padx=12, pady=(4,10))
        ctk.CTkLabel(info_nivel, text=f"Nivel: {getattr(self.motor, 'nivel', 1)}", font=("Arial", 12, "bold")).pack(side="left", padx=8)
        ctk.CTkLabel(info_nivel, text=f"XP: {xp_actual} / {xp_req}  (faltan {xp_faltante})", font=("Arial", 11)).pack(side="left", padx=8)
        barra_xp = ctk.CTkProgressBar(info_nivel, width=300)
        barra_xp.set(porcentaje)
        barra_xp.pack(side="right", padx=12)

        # --- ZONA DE TRABAJO (Elevadores) ---
        zona_elevadores = ctk.CTkFrame(self.root, fg_color="transparent")
        zona_elevadores.pack(expand=True, fill="both", padx=20, pady=10)

        # Pasamos: master, titulo y color (como pide tu interfaz/componentes.py)
        for i in range(2): 
            slot_ui = SlotTaller(zona_elevadores, titulo=f"ELEVADOR {i+1}", color="#2b2b2b") 
            slot_ui.actualizar(self.motor.slots[i])
            slot_ui.pack(side="left", expand=True, fill="both", padx=10)

        # --- ZONA DE PARKING ---
        zona_parking = ctk.CTkFrame(self.root, height=150, fg_color="transparent")
        zona_parking.pack(fill="x", padx=20, pady=10)

        # Pasamos: master, titulo y color
        slot_parking = SlotTaller(zona_parking, titulo="ESTACIONAMIENTO", color="#1f1f1f")
        slot_parking.actualizar(self.motor.slots[2])
        slot_parking.pack(side="left", expand=True, fill="both", padx=10)
        
        # --- FOOTER (Navegación) ---
        footer = ctk.CTkFrame(self.root, height=70)
        footer.pack(fill="x", side="bottom", pady=10)
        
        ctk.CTkButton(footer, text="🛒 IR AL MERCADO", height=45, width=200,
                      command=self.abrir_mercado).pack(expand=True)
        
    # --- MODALES Y VENTANAS SECUNDARIAS ---

    def abrir_pausa(self):
        """Muestra el menú de pausa (flotante)."""
        MenuPausa(self.root, self)

    def mostrar_opciones(self):
        """Pantalla de ajustes técnicos."""
        self.limpiar_pantalla()
        VentanaOpciones(self.root, al_volver=self.mostrar_menu_inicio)

    def abrir_mercado(self):
        """Abre la ventana de compra de autos."""
        VentanaMercado(self.root, self.motor, self.mostrar_taller)

if __name__ == "__main__":
    Aplicacion()