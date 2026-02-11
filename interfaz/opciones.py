import customtkinter as ctk
from core.ui_theme import COLORS, FONTS

class VentanaOpciones(ctk.CTkFrame):
    def __init__(self, master, al_volver, db=None):
        super().__init__(master)
        self.al_volver = al_volver
        self.db = db
        self.configure(fg_color=COLORS["bg"])
        self.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(self, text="CONFIGURACIÓN", font=FONTS["title"], text_color=COLORS["text"]).pack(pady=20)

        # MODO OSCURO/CLARO
        ctk.CTkLabel(self, text="Tema:", text_color=COLORS["muted"], font=FONTS["small"]).pack(pady=5)
        self.tema = ctk.CTkSegmentedButton(self, values=["Dark", "Light"], 
                                           command=self.cambiar_tema)
        self.tema.pack(pady=10)
        if self.db:
            self.tema.set(self.db.get_config("tema", ctk.get_appearance_mode()))
        else:
            self.tema.set(ctk.get_appearance_mode())

        # PANTALLA COMPLETA
        full_default = False
        if self.db:
            full_default = str(self.db.get_config("fullscreen", "false")).lower() == "true"
        self.full_var = ctk.BooleanVar(value=full_default)
        ctk.CTkCheckBox(self, text="Pantalla Completa", variable=self.full_var,
                        command=self.toggle_full).pack(pady=20)

        ctk.CTkButton(self, text="⬅️ VOLVER", fg_color=COLORS["panel_alt"], hover_color="#253041",
                  command=self.al_volver).pack(pady=20)

    def toggle_full(self):
        ventana = self.winfo_toplevel()
        ventana.attributes("-fullscreen", self.full_var.get())
        if self.db:
            self.db.set_config("fullscreen", "true" if self.full_var.get() else "false")

    def cambiar_tema(self, valor):
        ctk.set_appearance_mode(valor)
        if self.db:
            self.db.set_config("tema", valor)