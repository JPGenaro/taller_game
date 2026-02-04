import customtkinter as ctk
from core.config import ConfigManager

class VentanaOpciones(ctk.CTkFrame):
    def __init__(self, master, al_volver, motor=None, db=None):
        super().__init__(master)
        self.al_volver = al_volver # Función para regresar
        self.motor = motor
        self.db = db
        self.pack(expand=True, fill="both")

        ctk.CTkLabel(self, text="OPCIONES / PAUSA", font=("Arial", 25, "bold")).pack(pady=30)

        # --- SECCIÓN APARIENCIA ---
        ctk.CTkLabel(self, text="Apariencia").pack()
        self.switch_tema = ctk.CTkSegmentedButton(self, values=["Dark", "Light"], 
                                                 command=ConfigManager.cambiar_tema)
        self.switch_tema.pack(pady=10)
        self.switch_tema.set(ctk.get_appearance_mode())

        # --- SECCIÓN PANTALLA ---
        self.full_screen_var = ctk.BooleanVar(value=False)
        self.check_full = ctk.CTkCheckBox(self, text="Pantalla Completa", variable=self.full_screen_var,
                                         command=lambda: ConfigManager.toggle_pantalla_completa(master, self.full_screen_var.get()))
        self.check_full.pack(pady=10)

        ctk.CTkFrame(self, height=2, fg_color="gray").pack(fill="x", padx=50, pady=20)

        # --- BOTONES DE ACCIÓN (DINÁMICOS) ---
        if self.motor: # Si hay un motor activo, estamos dentro del juego
            ctk.CTkButton(self, text="Guardar Partida", fg_color="#2ecc71", 
                          command=self.guardar_actual).pack(pady=5)
            
        ctk.CTkButton(self, text="Volver", command=self.al_volver).pack(pady=5)
        
        if self.motor:
            ctk.CTkButton(self, text="Salir al Menú Principal", fg_color="#e74c3c", 
                          command=self.salir_al_menu).pack(pady=5)

    def guardar_actual(self):
        # Aquí llamaríamos a la lógica de DB para guardar el slot_actual
        pass

    def salir_al_menu(self):
        # Lógica para cerrar todo y volver al inicio
        pass