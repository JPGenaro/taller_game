import customtkinter as ctk

class VentanaOpciones(ctk.CTkFrame):
    def __init__(self, master, al_volver, motor=None, db=None, slot_id=None):
        super().__init__(master)
        self.al_volver = al_volver
        self.motor = motor
        self.db = db
        self.slot_id = slot_id
        self.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(self, text="⚙️ CONFIGURACIÓN", font=("Arial", 30, "bold")).pack(pady=20)

        # --- TEMA ---
        ctk.CTkLabel(self, text="Modo de Color:").pack(pady=5)
        self.tema_btn = ctk.CTkSegmentedButton(self, values=["Dark", "Light"], 
                                               command=self.cambiar_tema)
        self.tema_btn.pack(pady=10)
        self.tema_btn.set(ctk.get_appearance_mode())

        # --- PANTALLA ---
        self.fullscreen_var = ctk.BooleanVar(value=False)
        self.check_full = ctk.CTkCheckBox(self, text="Pantalla Completa", 
                                         variable=self.fullscreen_var,
                                         command=self.toggle_full)
        self.check_full.pack(pady=15)

        # --- BOTONES DINÁMICOS (PAUSA) ---
        if self.motor and self.db:
            ctk.CTkButton(self, text="💾 GUARDAR PARTIDA", fg_color="#2ecc71",
                          command=self.guardar_partida).pack(pady=10)

        ctk.CTkButton(self, text="⬅️ VOLVER", command=self.al_volver).pack(pady=10)

        if self.motor:
            ctk.CTkButton(self, text="🚪 SALIR AL MENÚ", fg_color="#e74c3c",
                          command=self.ir_al_inicio_desde_pausa).pack(pady=10)

    def cambiar_tema(self, seleccion):
        ctk.set_appearance_mode(seleccion)

    def toggle_full(self):
        if self.fullscreen_var.get():
            self.master.attributes("-fullscreen", True)
        else:
            self.master.attributes("-fullscreen", False)

    def guardar_partida(self):
        self.db.guardar(self.slot_id, self.motor)
        print(f"Partida guardada en slot {self.slot_id}")

    def ir_al_inicio_desde_pausa(self):
        # Necesitamos que la Aplicación (master) tenga este método
        self.master.mostrar_menu_inicio_desde_clase()