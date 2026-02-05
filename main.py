import customtkinter as ctk
from core.motor import MotorJuego
from core.database import Database
from modelos.auto import Auto
from interfaz.componentes import SlotTaller
from interfaz.mercado import VentanaMercado
from interfaz.pausa import MenuPausa
from interfaz.opciones import VentanaOpciones

class Aplicacion:
    def __init__(self):
        # 1. Inicializar el "cerebro" y la "memoria"
        self.motor = MotorJuego()
        self.db = Database()
        
        # 2. Configuración de la ventana principal de CTK
        self.root = ctk.CTk()
        self.root.title("Garage Tycoon Pro")
        self.root.geometry("1000x700")
        
        # Iniciar en el menú principal
        self.mostrar_menu_inicio()
        self.root.mainloop()

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_menu_inicio(self):
        self.limpiar_pantalla()
        
        ctk.CTkLabel(self.root, text="GARAGE TYCOON", font=("Arial", 45, "bold")).pack(pady=40)
        
        ctk.CTkButton(self.root, text="NUEVA PARTIDA", width=250, height=50,
                      command=lambda: self.mostrar_seleccion_slot("nueva")).pack(pady=10)
        
        estado_cargar = "normal" if self.db.hay_partidas_guardadas() else "disabled"
        ctk.CTkButton(self.root, text="CARGAR PARTIDA", width=250, height=50, state=estado_cargar,
                      command=lambda: self.mostrar_seleccion_slot("cargar")).pack(pady=10)
        
        ctk.CTkButton(self.root, text="OPCIONES", width=250, height=50, 
                      command=self.mostrar_opciones).pack(pady=10)
        
        ctk.CTkButton(self.root, text="CRÉDITOS", width=250, height=50,
                      command=self.mostrar_creditos).pack(pady=10)
        
        ctk.CTkButton(self.root, text="SALIR", width=250, height=50, fg_color="#A83232",
                      command=self.root.quit).pack(pady=10)

    def mostrar_registro(self, slot_id):
        self.limpiar_pantalla()
        self.slot_actual = slot_id
        
        ctk.CTkLabel(self.root, text="CONFIGURACIÓN INICIAL", font=("Arial", 25)).grid(row=0, pady=30)
        
        ent_personaje = ctk.CTkEntry(self.root, placeholder_text="Tu nombre", width=300)
        ent_personaje.grid(row=1, pady=10)
        
        ent_taller = ctk.CTkEntry(self.root, placeholder_text="Nombre del taller", width=300)
        ent_taller.grid(row=2, pady=10)

        def confirmar():
            self.motor.personaje = ent_personaje.get()
            self.motor.taller = ent_taller.get()
            if self.motor.personaje and self.motor.taller:
                self.db.guardar(self.slot_actual, self.motor) 
                self.mostrar_taller()

        ctk.CTkButton(self.root, text="¡ABRIR PUERTAS!", command=confirmar).grid(row=3, pady=30)

    def mostrar_seleccion_slot(self, modo="cargar"):
        self.limpiar_pantalla()
        ctk.CTkLabel(self.root, text="SELECCIONAR SLOT", font=("Arial", 25)).pack(pady=30)
        
        container = ctk.CTkFrame(self.root, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=50)

        for i in range(1, 4):
            datos = self.db.obtener_partida(i)
            slot_frame = ctk.CTkFrame(container)
            slot_frame.pack(fill="x", pady=10, padx=20)
            
            if datos:
                texto = f"Slot {i}: {datos[2]} ({datos[1]}) - Nivel {datos[4]} - ${datos[3]}"
                color_btn = "#3498db"
                cmd = lambda s=i, d=datos: self.cargar_esta_partida(s, d)
            else:
                texto = f"Slot {i}: VACÍO"
                color_btn = "#2ecc71"
                # Si estamos en modo cargar, el botón vacío se deshabilita
                estado = "normal" if modo == "nueva" else "disabled"
                cmd = lambda s=i: self.mostrar_registro(s)

            ctk.CTkLabel(slot_frame, text=texto, font=("Arial", 14)).pack(side="left", padx=20, pady=20)
            ctk.CTkButton(slot_frame, text="ELEGIR", fg_color=color_btn, width=100, 
                          command=cmd).pack(side="right", padx=20)

    def cargar_esta_partida(self, slot_id, datos):
        self.slot_actual = slot_id
        self.motor.personaje = datos[1]
        self.motor.taller = datos[2]
        self.motor.dinero = datos[3]
        self.motor.nivel = datos[4]
        self.motor.exp = datos[5]
        self.mostrar_taller()

    def mostrar_taller(self):
        self.limpiar_pantalla()
        
        # --- BARRA SUPERIOR (Stats) ---
        def abrir_pausa():
            self.limpiar_pantalla()
            VentanaOpciones(self.root, al_volver=self.mostrar_menu_inicio, 
                motor=self.motor, db=self.db, slot_id=self.slot_actual,
                juego=self)

        header = ctk.CTkFrame(self.root, height=80)
        header.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(header, text="⚙️", width=40, command=abrir_pausa).pack(side="right", padx=10)
        ctk.CTkLabel(header, text=f"💰 ${self.motor.dinero}", font=("Arial", 20, "bold"), text_color="#2ecc71").pack(side="left", padx=20)
        ctk.CTkLabel(header, text=f"Nivel {self.motor.nivel}", font=("Arial", 16)).pack(side="right", padx=20)

        # --- CONTENEDOR DE SLOTS (El diseño fachero) ---
        slots_container = ctk.CTkFrame(self.root, fg_color="transparent")
        slots_container.pack(expand=True, fill="both", padx=20, pady=20)
        slots_container.grid_columnconfigure((0, 1, 2), weight=1)

        self.widgets_slots = []
        nombres = ["🚧 ELEVADOR", "🅿️ PARKING 1", "🅿️ PARKING 2"]
        colores = ["#34495e", "#2c3e50", "#2c3e50"]

        for i in range(3):
            slot = SlotTaller(slots_container, titulo=nombres[i], color=colores[i])
            slot.grid(row=0, column=i, padx=10, sticky="nsew")
            # Actualizar el slot con la info del motor
            slot.actualizar(self.motor.slots[i])
            self.widgets_slots.append(slot)

        # --- BARRA INFERIOR (Acciones) ---
        footer = ctk.CTkFrame(self.root, height=100)
        footer.pack(fill="x", padx=10, pady=10)
        
        def abrir_mercado():
            VentanaMercado(self.root, self.motor, self.mostrar_taller)

        ctk.CTkButton(footer, text="🛒 BUSCAR AUTOS", command=abrir_mercado, 
              width=250, height=50).pack(side="left", padx=20)
        

    def pausa_taller(self):
        self.limpiar_pantalla()
        VentanaOpciones(self.root, al_volver=self.mostrar_taller, 
                        motor=self.motor, db=self.db)
    
    def mostrar_seleccion_slot(self, modo):
        self.limpiar_pantalla()
        titulo = "SELECCIONA UN SLOT PARA GUARDAR" if modo == "nueva" else "CARGAR PARTIDA"
        ctk.CTkLabel(self.root, text=titulo, font=("Arial", 20)).pack(pady=20)

        for i in range(1, 4):
            datos = self.db.obtener_partida(i)
            slot_frame = ctk.CTkFrame(self.root)
            slot_frame.pack(fill="x", padx=40, pady=10)

            if datos:
                info_texto = f"Slot {i}: {datos[2]} - Nivel {datos[4]} (${datos[3]})"
                btn_texto = "SOBRESCRIBIR" if modo == "nueva" else "CARGAR"
            else:
                info_texto = f"Slot {i}: VACÍO"
                btn_texto = "USAR SLOT" if modo == "nueva" else "VACÍO"
            
            ctk.CTkLabel(slot_frame, text=info_texto).pack(side="left", padx=20, pady=15)
            
            # Solo habilitamos el botón si hay datos (en modo cargar) o siempre (en modo nueva)
            btn_state = "normal" if (modo == "nueva" or datos) else "disabled"
            
            ctk.CTkButton(slot_frame, text=btn_texto, state=btn_state, width=100,
                          command=lambda s=i: self.manejar_seleccion_slot(s, modo)).pack(side="right", padx=20)

        ctk.CTkButton(self.root, text="VOLVER", command=self.mostrar_menu_inicio).pack(pady=20)

    def manejar_seleccion_slot(self, slot_id, modo):
        self.slot_actual = slot_id
        if modo == "nueva":
            self.mostrar_registro(slot_id)
        else:
            datos = self.db.obtener_partida(slot_id)
            self.cargar_esta_partida(slot_id, datos)

    def mostrar_creditos(self):
        self.limpiar_pantalla()
        ctk.CTkLabel(self.root, text="CRÉDITOS", font=("Arial Bold", 30)).pack(pady=30)
        ctk.CTkLabel(self.root, text="Desarrollado por: JP Genaro\nVersión: 0.2 Alpha", font=("Arial", 16)).pack(pady=20)
        ctk.CTkButton(self.root, text="VOLVER", command=self.mostrar_menu_inicio).pack(pady=20)

    def abrir_pausa(self):
        # NO usamos limpiar_pantalla aquí para que el taller se vea de fondo
        from interfaz.pausa import MenuPausa
        MenuPausa(self.root, self)

    def mostrar_opciones(self):
        self.limpiar_pantalla()
        # Solo dos argumentos: el root y la función para volver
        VentanaOpciones(self.root, al_volver=self.mostrar_menu_inicio)

    def mostrar_opciones_desde_pausa(self):
        self.limpiar_pantalla()
        VentanaOpciones(self.root, al_volver=self.abrir_pausa)

if __name__ == "__main__":
    Aplicacion()