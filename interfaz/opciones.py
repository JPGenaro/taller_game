import customtkinter as ctk

class VentanaOpciones(ctk.CTkFrame):
    def __init__(self, master, al_volver):
        super().__init__(master)
        self.al_volver = al_volver
        self.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(self, text="CONFIGURACIÓN", font=("Arial", 30, "bold")).pack(pady=20)

        # --- TEMA ---
        ctk.CTkLabel(self, text="Modo de Color:").pack(pady=5)
        self.tema_btn = ctk.CTkSegmentedButton(self, values=["Dark", "Light"], 
                                               command=lambda v: ctk.set_appearance_mode(v))
        self.tema_btn.pack(pady=10)
        self.tema_btn.set(ctk.get_appearance_mode())

        # --- BOTÓN VOLVER ---
        ctk.CTkButton(self, text="⬅️ VOLVER", command=self.al_volver).pack(pady=30)