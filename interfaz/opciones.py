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

        # --- PANTALLA COMPLETA ---
        self.fullscreen_var = ctk.BooleanVar(value=False)
        self.check_full = ctk.CTkCheckBox(self, text="Pantalla Completa", 
                                         variable=self.fullscreen_var,
                                         command=self.toggle_full)
        self.check_full.pack(pady=15)

        ctk.CTkButton(self, text="⬅️ VOLVER", command=self.al_volver).pack(pady=30)

    def toggle_full(self):
        ventana = self.winfo_toplevel()
        ventana.attributes("-fullscreen", self.fullscreen_var.get())