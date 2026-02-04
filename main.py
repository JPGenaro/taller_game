import customtkinter as ctk
from core.motor import MotorJuego
from core.database import Database
from modelos.auto import Auto
from interfaz.componentes import SlotTaller

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
        # Destruye todos los widgets dentro de la ventana para "cambiar" de escena
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_menu_inicio(self):
        self.limpiar_pantalla()
        self.root.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.root, text="GARAGE TYCOON", font=("Arial", 45, "bold")).grid(row=0, pady=50)
        
        ctk.CTkButton(self.root, text="NUEVA PARTIDA", width=250, height=50,
                      command=self.mostrar_registro).grid(row=1, pady=10)
        
        ctk.CTkButton(self.root, text="SALIR", width=250, height=50, fg_color="#A83232",
                      command=self.root.quit).grid(row=2, pady=10)

    def mostrar_registro(self):
        self.limpiar_pantalla()
        
        ctk.CTkLabel(self.root, text="CONFIGURACIÓN INICIAL", font=("Arial", 25)).grid(row=0, pady=30)
        
        ent_personaje = ctk.CTkEntry(self.root, placeholder_text="Tu nombre", width=300)
        ent_personaje.grid(row=1, pady=10)
        
        ent_taller = ctk.CTkEntry(self.root, placeholder_text="Nombre del taller", width=300)
        ent_taller.grid(row=2, pady=10)

        def confirmar():
            self.motor.personaje = ent_personaje.get()
            self.motor.taller = ent_taller.get()
            if self.motor.personaje and self.motor.taller:
                self.db.guardar(self.motor) # Guardamos en SQLite
                self.mostrar_taller()

        ctk.CTkButton(self.root, text="¡ABRIR PUERTAS!", command=confirmar).grid(row=3, pady=30)

    def mostrar_taller(self):
        self.limpiar_pantalla()
        
        # --- BARRA SUPERIOR (Stats) ---
        header = ctk.CTkFrame(self.root, height=80)
        header.pack(fill="x", padx=10, pady=10)
        
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
        
        def comprar_algo():
            # Esto es temporal para probar
            nuevo = Auto("Fiat", "600", 500)
            exito, msg = self.motor.comprar_auto(nuevo)
            if exito: self.mostrar_taller()

        ctk.CTkButton(footer, text="🛒 BUSCAR AUTOS", command=comprar_algo, width=200, height=50).pack(side="left", padx=20)

if __name__ == "__main__":
    Aplicacion()