import customtkinter as ctk

class VentanaOpciones(ctk.CTkFrame):
    def __init__(self, master, al_volver):
        super().__init__(master)
        self.al_volver = al_volver
        self.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(self, text="CONFIGURACIÓN", font=("Arial", 30, "bold")).pack(pady=20)

        # MODO OSCURO/CLARO
        ctk.CTkLabel(self, text="Tema:").pack(pady=5)
        self.tema = ctk.CTkSegmentedButton(self, values=["Dark", "Light"], 
                                           command=lambda v: ctk.set_appearance_mode(v))
        self.tema.pack(pady=10)
        self.tema.set(ctk.get_appearance_mode())

        # PANTALLA COMPLETA
        self.full_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(self, text="Pantalla Completa", variable=self.full_var,
                        command=self.toggle_full).pack(pady=20)

        ctk.CTkButton(self, text="⬅️ VOLVER", command=self.al_volver).pack(pady=20)

    def toggle_full(self):
        ventana = self.winfo_toplevel()
        ventana.attributes("-fullscreen", self.full_var.get())